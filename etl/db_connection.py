import psycopg2
from psycopg2 import pool
import logging

class DatabaseConnectionPool:
    def __init__(self, dbname: str, user: str, password: str, host: str, port: str, minconn: int = 1, maxconn: int = 10):
        self.connection_pool = None
        self._initialize_pool(dbname, user, password, host, port, minconn, maxconn)

    def _initialize_pool(self, dbname: str, user: str, password: str, host: str, port: str, minconn: int, maxconn: int):
        try:
            self.connection_pool = psycopg2.pool.SimpleConnectionPool(
                minconn,
                maxconn,
                dbname=dbname,
                user=user,
                password=password,
                host=host,
                port=port
            )
            logging.info("PostgreSQL connection pool created successfully")
        except Exception as e:
            logging.error(f"Error creating connection pool: {e}")
            raise

    def get_connection(self):
        try:
            connection = self.connection_pool.getconn()
            logging.info("Connection retrieved from pool")
            return connection
        except Exception as e:
            logging.error(f"Error getting connection from pool: {e}")
            raise

    def release_connection(self, connection):
        try:
            self.connection_pool.putconn(connection)
            logging.info("Connection returned to pool")
        except Exception as e:
            logging.error(f"Error returning connection to pool: {e}")
            raise

    def close_all_connections(self):
        try:
            self.connection_pool.closeall()
            logging.info("All connections in the pool have been closed")
        except Exception as e:
            logging.error(f"Error closing all connections: {e}")
            raise

# Example usage:
# db_pool = DatabaseConnectionPool(dbname='global_analytics_dw', user='your_user', password='your_password', host='localhost', port='5432')