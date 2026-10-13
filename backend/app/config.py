"""
Configuration Module for Animal Kingdom Knowledge Graph Backend.

This module centralizes application settings, loading environment variables
from the local `.env` file (if present) and providing safe defaults suitable
for local development or cloud deployment (e.g. Render, Neo4j Aura).
"""

import os
from pathlib import Path
from pydantic import BaseModel
from dotenv import load_dotenv

# Locate and load the .env file situated in the backend root directory
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)


class Settings(BaseModel):
    """
    Application Settings schema.

    Validates and holds runtime configuration values including Neo4j connection
    credentials, server host/port binding, runtime environment, and CORS policies.
    """
    # Neo4j Database Connection settings
    # Supports Bolt (bolt://) and encrypted Aura protocol (neo4j+s://)
    neo4j_uri: str = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    neo4j_username: str = os.getenv("NEO4J_USERNAME", "neo4j")
    neo4j_password: str = os.getenv("NEO4J_PASSWORD", "password123")
    neo4j_database: str = os.getenv("NEO4J_DATABASE", "neo4j")

    # FastAPI Web Server configuration
    app_host: str = os.getenv("APP_HOST", "0.0.0.0")
    app_port: int = int(os.getenv("APP_PORT", "8000"))
    environment: str = os.getenv("ENVIRONMENT", "development")

    # Cross-Origin Resource Sharing (CORS) allowed origins
    # Parsed from a comma-separated string (e.g., 'http://localhost:5173,http://localhost:3000' or '*')
    cors_origins: list[str] = [
        origin.strip()
        for origin in os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:3000").split(",")
        if origin.strip()
    ]


# Global settings singleton instance used across the FastAPI application
settings = Settings()
