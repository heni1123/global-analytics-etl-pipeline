import logging
import psycopg2
from psycopg2 import sql
from datetime import datetime
from typing import Any, Dict

class AuditLogger:
    def __init__(self, db_config: Dict[str, Any]):
        self.connection = self.create_connection(db_config)
        self.logger = self.setup_logger()

    def create_connection(self, db_config: Dict[str, Any]) -> psycopg2.extensions.connection:
        try:
            connection = psycopg2.connect(
                dbname=db_config['dbname'],
                user=db_config['user'],
                password=db_config['password'],
                host=db_config['host'],
                port=db_config['port']
            )
            return connection
        except Exception as e:
            self.logger.error(f"Error connecting to the database: {e}")
            raise

    def setup_logger(self) -> logging.Logger:
        logger = logging.getLogger("PipelineAuditLogger")
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler("pipeline_audit.log")
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def log_pipeline_run(self, pipeline_name: str, status: str, error_message: str = None) -> None:
        try:
            with self.connection.cursor() as cursor:
                insert_query = sql.SQL("""
                    INSERT INTO pipeline_runs (pipeline_name, run_date, status, error_message)
                    VALUES (%s, %s, %s, %s)
                """)
                cursor.execute(insert_query, (pipeline_name, datetime.now(), status, error_message))
                self.connection.commit()
                self.logger.info(f"Logged pipeline run: {pipeline_name}, Status: {status}")
        except Exception as e:
            self.logger.error(f"Error logging pipeline run: {e}")
            self.connection.rollback()

    def close_connection(self) -> None:
        if self.connection:
            self.connection.close()
            self.logger.info("Database connection closed.")

# Usage example (to be called in the main pipeline execution logic):
# db_config = {
#     'dbname': 'your_db_name',
#     'user': 'your_user',
#     'password': 'your_password',
#     'host': 'your_host',
#     'port': 'your_port'
# }
# audit_logger = AuditLogger(db_config)
# audit_logger.log_pipeline_run("Global Data Analytics Pipeline", "SUCCESS")
# audit_logger.close_connection()