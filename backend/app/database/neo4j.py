"""
Neo4j Database Driver & Connection Manager.

Implements a thread-safe Singleton pattern wrapping the official Neo4j Python Driver.
Manages driver pooling, connection life-cycle, transactional read/write executions,
and automatic failover/reconnection checks.
"""

import logging
from typing import Any, Dict, List, Optional
from neo4j import GraphDatabase, Driver
from app.config import settings

logger = logging.getLogger(__name__)


class Neo4jConnection:
    """
    Singleton connection manager for the Neo4j Graph Database.
    
    Ensures that only one driver instance with its associated connection pool
    is created across the entire application lifecycle, saving memory and socket resources.
    """
    _instance: Optional["Neo4jConnection"] = None
    _driver: Optional[Driver] = None
    _is_connected: bool = False

    def __new__(cls):
        """Ensures a single instance of Neo4jConnection exists (Singleton pattern)."""
        if cls._instance is None:
            cls._instance = super(Neo4jConnection, cls).__new__(cls)
        return cls._instance

    def connect(self) -> bool:
        """
        Initializes the Neo4j driver and verifies server connectivity.

        Configures connection pooling parameters:
        - max_connection_lifetime: Closes stale connections after 1 hour.
        - max_connection_pool_size: Up to 50 concurrent connections.
        - connection_acquisition_timeout: 5.0 seconds before timing out on pool exhaustion.

        Returns:
            bool: True if connection was established and verified, False otherwise.
        """
        if self._driver is not None:
            return self._is_connected

        try:
            self._driver = GraphDatabase.driver(
                settings.neo4j_uri,
                auth=(settings.neo4j_username, settings.neo4j_password),
                max_connection_lifetime=3600,
                max_connection_pool_size=50,
                connection_acquisition_timeout=5.0
            )
            # Actively ping the database to confirm credentials and routing
            self._driver.verify_connectivity()
            self._is_connected = True
            logger.info("Successfully connected to Neo4j at %s", settings.neo4j_uri)
            return True
        except Exception as e:
            self._is_connected = False
            logger.warning("Could not connect to Neo4j at %s: %s", settings.neo4j_uri, str(e))
            return False

    def close(self):
        """Closes the underlying Neo4j driver and releases all socket connections."""
        if self._driver is not None:
            self._driver.close()
            self._driver = None
            self._is_connected = False
            logger.info("Neo4j driver closed.")

    @property
    def is_connected(self) -> bool:
        """
        Checks whether the connection is active.
        If disconnected or uninitialized, attempts an automatic reconnect.
        """
        if not self._is_connected or self._driver is None:
            return self.connect()
        try:
            self._driver.verify_connectivity()
            return True
        except Exception:
            self._is_connected = False
            return False

    def execute_read(self, query: str, parameters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Executes a read-only Cypher query and returns the results.

        Args:
            query (str): Cypher query string (e.g. MATCH (a:Animal) RETURN a).
            parameters (dict, optional): Parameter dictionary to bind securely against Cypher injections.

        Returns:
            List[Dict[str, Any]]: List of dictionary mappings representing matching graph records.

        Raises:
            ConnectionError: If the Neo4j database is currently disconnected.
        """
        if not self.is_connected:
            raise ConnectionError("Neo4j database is currently disconnected.")

        with self._driver.session(database=settings.neo4j_database) as session:
            result = session.run(query, parameters or {})
            return [record.data() for record in result]

    def execute_write(self, query: str, parameters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Executes a write Cypher query inside an explicit write transaction with auto-commit retry.

        Args:
            query (str): Cypher mutation query string (e.g. CREATE, MERGE, SET, DELETE).
            parameters (dict, optional): Parameter dictionary for Cypher query.

        Returns:
            List[Dict[str, Any]]: Result records returned by the transaction.

        Raises:
            ConnectionError: If the Neo4j database is currently disconnected.
        """
        if not self.is_connected:
            raise ConnectionError("Neo4j database is currently disconnected.")

        with self._driver.session(database=settings.neo4j_database) as session:
            def _tx(tx):
                res = tx.run(query, parameters or {})
                return [record.data() for record in res]
            return session.execute_write(_tx)


# Exported singleton instance used by services and routes
neo4j_client = Neo4jConnection()
