"""
Main Entry Point for the Animal Kingdom Knowledge Graph FastAPI Backend.

This module initializes the FastAPI application instance, configures CORS middleware,
manages database lifecycle hooks (connecting to Neo4j on startup and gracefully closing
connections on shutdown), registers all API routers, and provides global error handling.
"""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import settings
from app.database.neo4j import neo4j_client
from app.database.schema import init_schema
from app.routes import animals, dashboard, graph, habitats, queries, search

# Configure Standard Application Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("animal_kg_app")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI Lifespan Context Manager.
    
    Executes startup and shutdown tasks:
    - On Startup: Establishes the Neo4j driver connection and initializes
      uniqueness constraints and indexes. If the database is temporarily unreachable,
      it logs a warning while allowing the API to run with dataset fallbacks.
    - On Shutdown: Closes all active connection pools in the Neo4j driver cleanly.
    """
    # ------------------ Startup Phase ------------------
    logger.info("Starting Animal Kingdom Knowledge Graph backend...")
    connected = neo4j_client.connect()
    if connected:
        logger.info("Connected to Neo4j. Initializing schema constraints & indexes...")
        try:
            init_schema()
        except Exception as e:
            logger.warning("Schema initialization notice: %s", str(e))
    else:
        logger.warning(
            "Neo4j database is not reachable at %s. Running in high-availability mode with dataset fallback.",
            settings.neo4j_uri
        )
    
    yield  # Application serves incoming HTTP requests

    # ------------------ Shutdown Phase ------------------
    logger.info("Shutting down Animal Kingdom Knowledge Graph backend...")
    neo4j_client.close()


# Instantiate FastAPI Application with OpenAPI metadata
app = FastAPI(
    title="Animal Kingdom Knowledge Graph API",
    description="Knowledge Graph backend powered by FastAPI, Cypher, and Neo4j.",
    version="1.0.0",
    lifespan=lifespan
)

# ---------------------------------------------------------
# Cross-Origin Resource Sharing (CORS) Configuration
# ---------------------------------------------------------
# Starlette/FastAPI does not allow allow_credentials=True when allow_origins=["*"].
# We dynamically toggle allow_credentials to False if a wildcard '*' is provided.
is_wildcard = "*" in settings.cors_origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=not is_wildcard,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------
# Route Registrations
# ---------------------------------------------------------
# Modular routers grouped by functional domain
app.include_router(dashboard.router)  # /api/dashboard - Summary statistics
app.include_router(animals.router)    # /api/animals   - Animal queries & graph profiles
app.include_router(search.router)     # /api/search    - Faceted search & auto-complete
app.include_router(habitats.router)   # /api/habitats  - Habitat biomes & resident fauna
app.include_router(queries.router)    # /api/queries   - Natural language Cypher engine
app.include_router(graph.router)      # /api/graph     - Graph visualization payloads


@app.get("/api/health", tags=["Health"])
def health_check():
    """
    System Health & Database Connectivity Endpoint.
    
    Returns:
        dict: Operational status, Neo4j connectivity flag, active database URI,
              and runtime environment. Useful for Docker, Kubernetes, and Render health probes.
    """
    is_neo4j_connected = neo4j_client.is_connected
    return {
        "status": "online",
        "neo4jConnected": is_neo4j_connected,
        "databaseUri": settings.neo4j_uri,
        "environment": settings.environment
    }


# ---------------------------------------------------------
# Global Safe Exception Handler
# ---------------------------------------------------------
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Catches all unhandled exceptions across route handlers.
    Logs the error with traceback context and returns a sanitized JSON 500 response.
    """
    logger.error("Unhandled exception for request %s: %s", request.url.path, str(exc))
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal server error occurred. Please try again later."}
    )


# Entry point for direct script execution (e.g. `python app/main.py`)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=settings.app_host, port=settings.app_port, reload=True)
