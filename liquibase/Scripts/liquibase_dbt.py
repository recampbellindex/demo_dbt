import json
import re
import subprocess
import getpass

# Configuration
database_name = "PRODDB"
label_filter = "dbt-schema-changes"
profile = "liquibase"
username = getpass.getuser()

# Paths
project_dir = r"C:\Liquibase\Tests\Customers\2025\Voya\Demo_DBT"
output_file = r"C:\Liquibase\Tests\Customers\2025\Voya\Demo_DBT\liquibase\Scripts\liquibase.extracted.sql"

# List of SQL keywords to look for (case insensitive)
sql_keywords = ['create', 'alter', 'drop', 'truncate', 'rename', 'replace', 'grant', 'revoke', 'comment', 'use', 'set']

# Regex pattern to strip comments
comment_pattern = r'/\*.*?\*/'

# Function to run DBT and capture the output
def run_dbt(profile, project_dir):
    command = [
        'dbt', 'build',
        '--profile', profile,
        '--project-dir', project_dir,
        '--debug', '--log-format=json', '--full-refresh'
    ]

    try:
        result = subprocess.run(command, capture_output=True, text=True)

        errors_found = False
        for line in result.stdout.splitlines():
            try:
                log = json.loads(line.strip())
                if log.get("levelname", "").lower() == "error":
                    print("Error log entry:")
                    print(log.get("msg"))
                    errors_found = True
                elif log.get("data", {}).get("status", "").lower() in {"error", "fail"}:
                    print("Failed node log:")
                    print(json.dumps(log, indent=2))
                    errors_found = True
            except json.JSONDecodeError:
                continue

        if result.returncode != 0 or errors_found:
            raise Exception("DBT run failed (based on return code or log contents)")

        return result.stdout

    except Exception as e:
        print(f"Error running DBT: {str(e)}")
        return None

# Function to extract SQL statements based on keywords
def extract_sql(db_output, output_file):
    changeset_id = 1000
    sql_statements = []

    if isinstance(db_output, str):
        db_output = db_output.splitlines()

    for i, line in enumerate(db_output):
        try:
            if not line.strip():
                continue

            line_no_comments = re.sub(comment_pattern, '', line).strip()
            if not line_no_comments:
                continue

            log_entry = json.loads(line_no_comments)

            # Safe level filter: only skip known bad levels
            level = log_entry.get("levelname", "") or log_entry.get("level", "")
            if level and level.lower() in {"warning", "error", "critical"}:
                continue

            # Extract from data.sql
            extracted_sql = log_entry.get("data", {}).get("sql", "")
            sql = process_sql(extracted_sql, database_name, sql_keywords)
            if sql:
                sql_statements.append(sql)

            # Also extract from msg (some SQL is only there)
            msg = log_entry.get("msg", "")
            if isinstance(msg, str) and "Executing SQL" in msg:
                extracted_sql = msg.replace("Executing SQL:", "").strip()
                sql = process_sql(extracted_sql, database_name, sql_keywords)
                if sql:
                    sql_statements.append(sql)

        except json.JSONDecodeError as e:
            print(f"[Line {i}] JSON Decode Error: {e}\nContent: {line.strip()}")
        except Exception as e:
            print(f"[Line {i}] Unexpected error: {e}\nContent: {line.strip()}")

    # Write to output
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("--liquibase formatted sql\n\n")
        for statement in sql_statements:
            f.write(f"--changeset {username}:{changeset_id} labels:{label_filter}\n")
            f.write(statement + '\n--rollback empty\n\n')
            changeset_id += 1

# Function to clean and normalize extracted SQL
def process_sql(raw_sql, database_name, sql_keywords):
    sql = raw_sql.replace(f"{database_name}.", "")
    sql = " ".join(sql.split())
    if not sql.endswith(';'):
        sql += ';'

    # Exclude unwanted patterns
    if "alter session" in sql.lower():
        return None

    # Match against keywords
    for keyword in sql_keywords:
        if keyword in sql.lower():
            return sql

    return None

# Run DBT and capture the output
db_output = run_dbt(profile, project_dir)

# If DBT run is successful, extract and write SQL statements
if db_output:
    extract_sql(db_output, output_file)
    print(f"SQL statements extracted to {output_file}")