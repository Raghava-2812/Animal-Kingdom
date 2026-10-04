import logging
from typing import Any, Dict, List, Optional
from neo4j import GraphDatabase, Driver
from app.config import settings

logger = logging.getLogger(__name__)

class Neo4jConnection:
    _instance: Optional["Neo4jConnection"] = None
    _driver: Optional[Driver] = None
    _is_connected: bool = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Neo4jConnection, cls).__new__(cls)
        return cls._instance

    def connect(self) -> bool:
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
            # Verify connectivity
            self._driver.verify_connectivity()
            self._is_connected = True
            logger.info("Successfully connected to Neo4j at %s", settings.neo4j_uri)
            return True
        except Exception as e:
            self._is_connected = False
            logger.warning("Could not connect to Neo4j at %s: %s", settings.neo4j_uri, str(e))
            return False

    def close(self):
        if self._driver is not None:
            self._driver.close()
            self._driver = None
            self._is_connected = False
            logger.info("Neo4j driver closed.")

    @property
    def is_connected(self) -> bool:
        if not self._is_connected or self._driver is None:
            # Attempt reconnect if not connected
            return self.connect()
        try:
            self._driver.verify_connectivity()
            return True
        except Exception:
            self._is_connected = False
            return False

    def execute_read(self, query: str, parameters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Execute a read Cypher query and return results as a list of dicts."""
        if not self.is_connected:
            raise ConnectionError("Neo4j database is currently disconnected.")

        with self._driver.session(database=settings.neo4j_database) as session:
            result = session.run(query, parameters or {})
            return [record.data() for record in result]

    def execute_write(self, query: str, parameters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Execute a write Cypher query in a write transaction."""
        if not self.is_connected:
            raise ConnectionError("Neo4j database is currently disconnected.")

        with self._driver.session(database=settings.neo4j_database) as session:
            def _tx(tx):
                res = tx.run(query, parameters or {})
                return [record.data() for record in res]
            return session.execute_write(_tx)

neo4j_client = Neo4jConnection()
