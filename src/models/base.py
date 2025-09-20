"""
Base module for database initialization.

This module initializes the SQLAlchemy database object to be used
across all models, preventing circular imports.
"""

from flask_sqlalchemy import SQLAlchemy

# Initialize database object
db = SQLAlchemy()
