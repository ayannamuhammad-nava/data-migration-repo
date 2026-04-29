"""
DM Bootstrap — One-command project setup from COBOL data files.

Scans a data directory for SQL files and COBOL copybooks, creates databases,
loads data, registers tables in OpenMetadata, and configures the project.

Usage:
    dm bootstrap my-project --data /path/to/cobol/files
"""

import json
import logging
import os
import re
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import requests
import yaml

logger = logging.getLogger(__name__)


def scan_data_directory(data_path: str) -> Dict:
    """Scan a directory for COBOL data files.

    Looks for:
    - *.sql files (CREATE TABLE, INSERT statements)
    - *.cpy files (COBOL copybooks with field descriptions)
    - *.dat files (flat data files)

    Returns:
        Dict with categorized file lists and parsed metadata.
    """
    data_dir = Path(data_path)
    if not data_dir.exists():
        raise FileNotFoundError(f"Data directory not found: {data_path}")

    result = {
        "sql_files": [],
        "copybooks": [],
        "data_files": [],
        "tables": {},       # table_name -> {columns: [{name, type, description}]}
        "legacy_ddl": [],   # SQL files with CREATE TABLE
        "legacy_data": [],  # SQL files with INSERT
        "modern_ddl": [],   # SQL files with 'modern' in name
    }

    for f in sorted(data_dir.iterdir()):
        if f.suffix == ".sql":
            result["sql_files"].append(f)
            content = f.read_text()
            if "modern" in f.name.lower():
                result["modern_ddl"].append(f)
            elif "CREATE TABLE" in content.upper():
                if "INSERT" in content.upper():
                    result["legacy_data"].append(f)
                else:
                    result["legacy_ddl"].append(f)
            elif "INSERT" in content.upper():
                result["legacy_data"].append(f)

        elif f.suffix == ".cpy":
            result["copybooks"].append(f)

        elif f.suffix == ".dat":
            result["data_files"].append(f)

    # Parse tables from SQL files
    for sql_file in result["legacy_ddl"]:
        tables = parse_create_tables(sql_file.read_text())
        result["tables"].update(tables)

    # If no tables found from DDL, try data files
    if not result["tables"]:
        for sql_file in result["legacy_data"]:
            tables = parse_create_tables(sql_file.read_text())
            result["tables"].update(tables)

    # Enrich with copybook descriptions
    for cpy_file in result["copybooks"]:
        descriptions = parse_copybook(cpy_file.read_text())
        for table_name, table_info in result["tables"].items():
            for col in table_info.get("columns", []):
                col_name = col["name"].lower()
                if col_name in descriptions:
                    col["description"] = descriptions[col_name]

    logger.info(f"Scanned {data_path}: {len(result['sql_files'])} SQL, "
                f"{len(result['copybooks'])} copybooks, {len(result['tables'])} tables")

    return result


def parse_create_tables(sql: str) -> Dict:
    """Parse CREATE TABLE statements from SQL to extract table and column definitions.

    Returns:
        Dict of {table_name: {columns: [{name, type, description}]}}
    """
    tables = {}
    # Match CREATE TABLE statements
    pattern = re.compile(
        r'CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?(\w+)\s*\((.*?)\);',
        re.IGNORECASE | re.DOTALL
    )

    for match in pattern.finditer(sql):
        table_name = match.group(1).lower()
        body = match.group(2)

        columns = []
        for line in body.split("\n"):
            line = line.strip()
            if not line or line.startswith("--") or line.upper().startswith("CONSTRAINT"):
                continue

            # Split on -- to separate SQL from comment
            description = ""
            if "--" in line:
                sql_part, comment_part = line.split("--", 1)
                description = comment_part.strip()
                line = sql_part.strip()
            else:
                line = line.strip()

            # Remove trailing comma
            line = line.rstrip(",").strip()

            # Parse: column_name TYPE [constraints]
            col_match = re.match(
                r'(\w+)\s+([\w()]+(?:\s*\(\s*\d+\s*(?:,\s*\d+)?\s*\))?)',
                line, re.IGNORECASE
            )
            if col_match:
                col_name = col_match.group(1).lower()
                col_type = col_match.group(2).strip()

                # Skip SQL keywords
                if col_name.upper() in ("PRIMARY", "CONSTRAINT", "FOREIGN", "UNIQUE", "CHECK", "INDEX", "CREATE", "GRANT"):
                    continue

                columns.append({
                    "name": col_name,
                    "type": col_type,
                    "description": description,
                })

        if columns:
            tables[table_name] = {"columns": columns}
            logger.info(f"Parsed table '{table_name}': {len(columns)} columns")

    return tables


def parse_copybook(cpy_content: str) -> Dict[str, str]:
    """Parse a COBOL copybook to extract field name -> description mappings.

    Looks for patterns like:
        05  CT-FNAM    PIC X(25).   or   05 CT-FNAM PIC X(25)

    Converts COBOL field names to SQL column names:
        CT-FNAM -> ct_fnam

    Returns:
        Dict of {sql_column_name: COBOL_DESCRIPTION}
    """
    descriptions = {}

    # Match COBOL field definitions: level  NAME  PIC ...
    pattern = re.compile(
        r'^\s*\d{2}\s+([\w-]+)\s+PIC\s+([^\s.]+)',
        re.MULTILINE
    )

    for match in pattern.finditer(cpy_content):
        cobol_name = match.group(1)  # e.g., CT-FNAM

        # Convert to SQL name: CT-FNAM -> ct_fnam
        sql_name = cobol_name.lower().replace("-", "_")

        # The COBOL name IS the description (e.g., CONTACT-FIRST-NAME)
        # But we need the parent record name stripped
        # For now, use the COBOL name directly as the description
        descriptions[sql_name] = cobol_name.upper()

    # Also look for comment-based descriptions: -- PIC ... DESCRIPTION
    comment_pattern = re.compile(
        r'^\s*\d{2}\s+([\w-]+)\s+PIC\s+\S+\s+(.+?)$',
        re.MULTILINE
    )
    for match in comment_pattern.finditer(cpy_content):
        cobol_name = match.group(1)
        sql_name = cobol_name.lower().replace("-", "_")
        desc_text = match.group(2).strip().rstrip(".")
        if desc_text:
            descriptions[sql_name] = desc_text

    logger.info(f"Parsed copybook: {len(descriptions)} field descriptions")
    return descriptions


def _find_postgres_container() -> str:
    """Auto-detect the running PostgreSQL container name.

    Checks for containers with port 5432 exposed, preferring:
    1. dm_postgres (from our docker-compose)
    2. Any container with 'database' in name (common in app stacks)
    3. Any container with 'postgres' in name (excluding OM's internal postgres)
    """
    try:
        result = subprocess.run(
            ["docker", "ps", "--format", "{{.Names}}\t{{.Ports}}"],
            capture_output=True, text=True, timeout=10
        )
        lines = result.stdout.strip().splitlines()

        # Parse into (name, ports) tuples
        containers = []
        for line in lines:
            parts = line.split("\t")
            if len(parts) >= 2:
                containers.append((parts[0], parts[1]))
            elif parts:
                containers.append((parts[0], ""))

        # Priority 1: dm_postgres
        for name, ports in containers:
            if name == "dm_postgres":
                return name

        # Priority 2: Container exposing port 5432 (not OM's on 5433)
        for name, ports in containers:
            if "5432->5432" in ports and "openmetadata" not in name.lower():
                return name

        # Priority 3: Any container with database/postgres in name (not OM)
        for name, ports in containers:
            if ("database" in name.lower() or "postgres" in name.lower()) \
                    and "openmetadata" not in name.lower() and "om_" not in name.lower() and "dm_om" not in name.lower():
                return name

        return "dm_postgres"
    except Exception:
        return "dm_postgres"


def load_data_to_postgres(
    scan_result: Dict,
    host: str = "localhost",
    port: int = 5432,
    user: str = "app",
    password: str = "secret123",
    container: str = "",
) -> None:
    """Load SQL files into PostgreSQL.

    Auto-detects the PostgreSQL Docker container if not specified.
    """
    if not container:
        container = _find_postgres_container()
        logger.info(f"Using PostgreSQL container: {container}")
    # Create databases if needed
    _exec_sql(container, user, password, "postgres",
              "SELECT 1 FROM pg_database WHERE datname='legacy_db'",
              create_if_missing="CREATE DATABASE legacy_db;")
    _exec_sql(container, user, password, "postgres",
              "SELECT 1 FROM pg_database WHERE datname='modern_db'",
              create_if_missing="CREATE DATABASE modern_db;")

    # Load legacy DDL
    for sql_file in scan_result.get("legacy_ddl", []):
        logger.info(f"Loading legacy DDL: {sql_file.name}")
        _exec_sql_file(container, user, password, "legacy_db", sql_file)

    # Load legacy data
    for sql_file in scan_result.get("legacy_data", []):
        logger.info(f"Loading legacy data: {sql_file.name}")
        _exec_sql_file(container, user, password, "legacy_db", sql_file)

    # Load modern DDL
    for sql_file in scan_result.get("modern_ddl", []):
        logger.info(f"Loading modern DDL: {sql_file.name}")
        _exec_sql_file(container, user, password, "modern_db", sql_file)


def _exec_sql(container, user, password, database, check_sql, create_if_missing=None):
    """Execute a SQL command via docker exec."""
    try:
        result = subprocess.run(
            ["docker", "exec", "-e", f"PGPASSWORD={password}", container,
             "psql", "-U", user, "-d", database, "-tAc", check_sql],
            capture_output=True, text=True, timeout=30
        )
        if create_if_missing and "1" not in result.stdout:
            subprocess.run(
                ["docker", "exec", "-e", f"PGPASSWORD={password}", container,
                 "psql", "-U", user, "-d", database, "-c", create_if_missing],
                capture_output=True, text=True, timeout=30
            )
            logger.info(f"Created: {create_if_missing}")
    except Exception as e:
        logger.warning(f"SQL exec failed: {e}")


def _exec_sql_file(container, user, password, database, sql_file):
    """Copy and execute a SQL file via docker exec."""
    try:
        # Copy file into container (use absolute path)
        abs_path = str(Path(sql_file).resolve())
        subprocess.run(
            ["docker", "cp", abs_path, f"{container}:/tmp/{sql_file.name}"],
            check=True, capture_output=True, timeout=30
        )
        # Execute
        result = subprocess.run(
            ["docker", "exec", "-e", f"PGPASSWORD={password}", container,
             "psql", "-U", user, "-d", database, "-f", f"/tmp/{sql_file.name}"],
            capture_output=True, text=True, timeout=60
        )
        if result.returncode != 0 and result.stderr:
            # Check for non-fatal errors
            errors = [l for l in result.stderr.splitlines() if "ERROR" in l]
            if errors:
                logger.warning(f"Errors loading {sql_file.name}: {errors[0]}")
        else:
            logger.info(f"Loaded {sql_file.name} into {database}")
    except Exception as e:
        logger.error(f"Failed to load {sql_file.name}: {e}")


def register_in_openmetadata(
    scan_result: Dict,
    service_name: str,
    database_name: str,
    schema_name: str = "public",
    om_host: str = "http://localhost:8585",
) -> Optional[str]:
    """Register tables in OpenMetadata.

    Creates the service, database, schema, and table entities.

    Returns:
        JWT auth token, or None on failure.
    """
    # Get auth token
    try:
        import base64
        b64_pass = base64.b64encode(b"admin").decode()
        resp = requests.post(
            f"{om_host}/api/v1/users/login",
            json={"email": "admin@open-metadata.org", "password": b64_pass},
            timeout=10,
        )
        resp.raise_for_status()
        token = resp.json()["accessToken"]
    except Exception as e:
        logger.error(f"Could not get OM auth token: {e}")
        return None

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    # Create service
    try:
        requests.put(
            f"{om_host}/api/v1/services/databaseServices",
            headers=headers,
            json={
                "name": service_name,
                "serviceType": "Postgres",
                "connection": {
                    "config": {
                        "type": "Postgres",
                        "hostPort": "host.docker.internal:5432",
                        "username": "app",
                        "authType": {"password": "secret123"},
                        "database": "legacy_db",
                    }
                },
            },
            timeout=10,
        )
        logger.info(f"Registered service: {service_name}")
    except Exception as e:
        logger.warning(f"Service registration: {e}")

    # Create database
    fqn_db = f"{service_name}.{database_name}"
    try:
        requests.put(
            f"{om_host}/api/v1/databases",
            headers=headers,
            json={"name": database_name, "service": service_name},
            timeout=10,
        )
        logger.info(f"Registered database: {fqn_db}")
    except Exception as e:
        logger.warning(f"Database registration: {e}")

    # Create schema
    fqn_schema = f"{fqn_db}.{schema_name}"
    try:
        requests.put(
            f"{om_host}/api/v1/databaseSchemas",
            headers=headers,
            json={"name": schema_name, "database": fqn_db},
            timeout=10,
        )
        logger.info(f"Registered schema: {fqn_schema}")
    except Exception as e:
        logger.warning(f"Schema registration: {e}")

    # Register tables
    TYPE_MAP = {
        "integer": "INT", "int": "INT", "serial": "INT",
        "bigint": "BIGINT", "smallint": "SMALLINT",
        "varchar": "VARCHAR", "character varying": "VARCHAR",
        "char": "CHAR", "character": "CHAR", "text": "VARCHAR",
        "numeric": "DECIMAL", "decimal": "DECIMAL",
        "boolean": "BOOLEAN", "bool": "BOOLEAN",
        "date": "DATE", "timestamp": "TIMESTAMP", "timestamptz": "TIMESTAMP",
    }

    for table_name, table_info in scan_result.get("tables", {}).items():
        om_columns = []
        for col in table_info.get("columns", []):
            # Map SQL type to OM type
            raw_type = col["type"].lower().split("(")[0].strip()
            om_type = TYPE_MAP.get(raw_type, "VARCHAR")

            # Extract length if present
            length_match = re.search(r'\((\d+)', col["type"])
            # Clean description for OM API
            desc = col.get("description", "")
            # Remove PIC type info and special chars
            desc = re.sub(r'PIC\s+\S+', '', desc).strip()
            desc = re.sub(r'[^\w\s\-./(),]', '', desc).strip()

            om_col = {
                "name": col["name"],
                "dataType": om_type,
                "description": desc,
            }
            if length_match:
                om_col["dataLength"] = int(length_match.group(1))

            om_columns.append(om_col)

        try:
            resp = requests.put(
                f"{om_host}/api/v1/tables",
                headers=headers,
                json={
                    "name": table_name,
                    "databaseSchema": fqn_schema,
                    "columns": om_columns,
                },
                timeout=10,
            )
            resp.raise_for_status()
            logger.info(f"Registered table: {fqn_schema}.{table_name} ({len(om_columns)} columns)")
        except Exception as e:
            logger.warning(f"Table registration for {table_name}: {e}")

    return token


def configure_project(
    project_dir: str,
    tables: Dict,
    service_name: str,
    database_name: str,
    token: str,
    project_name: str = "",
) -> None:
    """Update project.yaml with discovered tables and OM configuration."""
    project_path = Path(project_dir) / "project.yaml"
    if not project_path.exists():
        logger.error(f"project.yaml not found at {project_path}")
        return

    config = yaml.safe_load(project_path.read_text()) or {}

    # Update project name
    if project_name:
        config.setdefault("project", {})["name"] = project_name

    # Update connections
    config.setdefault("connections", {})
    config["connections"]["legacy"] = {
        "type": "postgres",
        "host": "${DB_LEGACY_HOST:localhost}",
        "port": 5432,
        "database": "${DB_LEGACY_NAME:legacy_db}",
        "user": "${DB_LEGACY_USER:app}",
        "password": "${DB_LEGACY_PASSWORD:secret123}",
    }
    config["connections"]["modern"] = {
        "type": "postgres",
        "host": "${DB_MODERN_HOST:localhost}",
        "port": 5432,
        "database": "${DB_MODERN_NAME:modern_db}",
        "user": "${DB_MODERN_USER:app}",
        "password": "${DB_MODERN_PASSWORD:secret123}",
    }

    # Update datasets
    datasets = []
    for table_name in tables:
        datasets.append({
            "name": table_name,
            "legacy_table": table_name,
            "modern_table": table_name,
        })
    config["datasets"] = datasets

    # Update validation required_fields and aggregates
    validation = config.setdefault("validation", {})
    gov = validation.setdefault("governance", {})
    required_fields = {}
    aggregates = {}
    for table_name in tables:
        required_fields[table_name] = []
        aggregates[table_name] = []
    gov["required_fields"] = required_fields
    validation["aggregates"] = aggregates

    # Update OpenMetadata config
    config["openmetadata"] = {
        "host": "${OM_HOST:http://localhost:8585}",
        "auth_token": f"${{OM_AUTH_TOKEN:{token}}}",
        "legacy_service": service_name,
        "legacy_database": database_name,
        "legacy_schema": "public",
    }

    project_path.write_text(yaml.dump(config, default_flow_style=False, sort_keys=False))
    logger.info(f"Updated project.yaml with {len(datasets)} dataset(s)")


def run_bootstrap(
    project_name: str,
    data_path: str,
    om_host: str = "http://localhost:8585",
) -> Dict:
    """Run the full bootstrap process.

    Args:
        project_name: Name for the new project.
        data_path: Path to directory containing COBOL data files.
        om_host: OpenMetadata server URL.

    Returns:
        Dict with bootstrap results.
    """
    # Derive service/database names from project
    safe_name = re.sub(r'[^a-z0-9_]', '_', project_name.lower())
    service_name = f"{safe_name}_legacy"
    database_name = f"{safe_name}_db"

    # Step 1: Scan data directory
    logger.info(f"Scanning data directory: {data_path}")
    scan_result = scan_data_directory(data_path)

    if not scan_result["tables"]:
        raise ValueError(f"No tables found in {data_path}. Need SQL files with CREATE TABLE statements.")

    # Step 2: Load into PostgreSQL
    logger.info("Loading data into PostgreSQL...")
    load_data_to_postgres(scan_result)

    # Step 3: Register in OpenMetadata
    logger.info("Registering in OpenMetadata...")
    token = register_in_openmetadata(
        scan_result, service_name, database_name, om_host=om_host,
    )

    # Step 4: Configure project
    project_dir = Path("projects") / project_name
    if token:
        logger.info("Configuring project...")
        configure_project(
            str(project_dir), scan_result["tables"],
            service_name, database_name, token,
            project_name=project_name,
        )

    return {
        "project_dir": str(project_dir),
        "tables": list(scan_result["tables"].keys()),
        "table_count": len(scan_result["tables"]),
        "sql_files": len(scan_result["sql_files"]),
        "copybooks": len(scan_result["copybooks"]),
        "service_name": service_name,
        "database_name": database_name,
        "om_registered": token is not None,
    }
