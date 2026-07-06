import os
import mysql.connector

def db_logging_enabled() -> bool:
    required = (
        os.getenv("MYSQL_HOST"),
        os.getenv("MYSQL_USER"),
        os.getenv("MYSQL_DATABASE"),
    )
    return (
        os.getenv("ENABLE_DB_LOGGING", "false").lower() == "true"
        and all(required)
    )

def get_db():
    if not db_logging_enabled():
        raise RuntimeError("Database logging disabled.")

    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        port=int(os.getenv("MYSQL_PORT", "3306")),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD", ""),
        database=os.getenv("MYSQL_DATABASE"),
        ssl_disabled=False,
    )


