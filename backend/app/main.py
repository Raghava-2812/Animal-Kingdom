import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import settings
from app.database.neo4j import neo4j_client
from app.database.schema import init_schema
from app.routes import animals, dashboard, graph, habitats, queries, search

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("animal_kg_app")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Try connecting to Neo4j and initializing schema
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
    yield
    # Shutdown: Close database driver
    logger.info("Shutting down Animal Kingdom Knowledge Graph backend...")
    neo4j_client.close()

app = FastAPI(
    title="Animal Kingdom Knowledge Graph API",
    description="Knowledge Graph backend powered by FastAPI, Cypher, and Neo4j.",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API Routers
app.include_router(dashboard.router)
app.include_router(animals.router)
app.include_router(search.router)
app.include_router(habitats.router)
app.include_router(queries.router)
app.include_router(graph.router)

@app.get("/api/health", tags=["Health"])
def health_check():
    """Health check endpoint displaying Neo4j connectivity status."""
    is_neo4j_connected = neo4j_client.is_connected
    return {
        "status": "online",
        "neo4jConnected": is_neo4j_connected,
        "databaseUri": settings.neo4j_uri,
        "environment": settings.environment
    }

# Global safe error handling
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error("Unhandled exception for request %s: %s", request.url.path, str(exc))
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal server error occurred. Please try again later."}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=settings.app_host, port=settings.app_port, reload=True)
