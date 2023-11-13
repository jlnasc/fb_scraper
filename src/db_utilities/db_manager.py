import psycopg2
from psycopg2 import pool
import logging

logging.basicConfig(level=logging.INFO, filename='db_manager.log', filemode='w', format='%(asctime)s - %(levelname)s - %(message)s - %(pathname)s:%(lineno)d')

class DatabaseConnectionError(Exception):
    pass


class DatabaseManager:
    """
    DatabaseManager class responsible for managing database connections.
    """

    def __init__(self, host, dbname, user, password, min_connections=1, max_connections=10):
        """
        Constructs a new DatabaseManager object.
        """

        logging.info("Initializing database manager")

        self.host = host
        self.dbname = dbname
        self.user = user
        self.password = password
        self.min_con = min_connections
        self.max_con = max_connections
        self.connection_pool = None

    def configure_connection_pool(self):
        """
        Configures the connection pool for database operations.

        Raises:
            DatabaseConnectionError: If an error occurs during connection pool configuration.
        """

        logging.info("Configuring connection pool")

        try:
            self.connection_pool = psycopg2.pool.SimpleConnectionPool(minconn=self.min_con,
                                                                        maxconn=self.max_con,
                                                                        host=self.host,
                                                                        dbname=self.dbname,
                                                                        user=self.user,
                                                                        password=self.password,
                                                                        port=5432)
            logging.info("Connection pool configured successfully")
        except Exception as e:
            logging.exception(f"Error configuring connection pool: {e}")
            raise DatabaseConnectionError(f"Failed to configure database connection pool: {e}") from e

    def get_connection(self):
        """
        Attempts to retrieve a connection from the connection pool.

        Raises:
            DatabaseConnectionError: If an error occurs during connection acquisition.
        """

        logging.info("Getting connection from pool")

        try:
            connection = self.connection_pool.getconn()
            logging.info("Connection obtained successfully")
            return connection
        except Exception as e:
            logging.exception(f"Error getting connection from pool: {e}")
            raise DatabaseConnectionError(f"Failed to obtain database connection: {e}") from e

    def release_idle_connections(self):
        """
        Releases idle connections back to the connection pool.
        """

        logging.info("Releasing idle connections from pool")

        try:
            self.connection_pool.release_idle()
            logging.info("Idle connections released successfully")
        except Exception as e:
            logging.exception(f"Error releasing idle connections: {e}")

    def return_connection(self, connection):
        """
        Returns the specified connection back to the connection pool.

        Args:
            connection (psycopg2.connection): The connection to return to the pool.
        """

        logging.info("Returning connection to pool")

        self.connection_pool.putconn(connection)

    def close_all_connections(self):
        """
        Closes all connections in the connection pool.
        """

        logging.info("Closing all connections")

        self.connection_pool.close()
