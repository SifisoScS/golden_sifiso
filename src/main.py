"""
Initialization module for The Golden Hand Learning Platform.

This module initializes the Flask application and sets up the database connection.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))  # DON'T CHANGE THIS !!!

from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager
from flask_migrate import Migrate
import os

# Initialize Flask app
app = Flask(__name__)

# Configure app
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_key_for_golden_hand')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.dirname(os.path.dirname(__file__)), 'golden_hand.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Import database from base
from src.models.base import db

# Initialize database with app
db.init_app(app)

# Initialize login manager
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'

# Initialize migrations
migrate = Migrate(app, db)

# Import all models from centralized models package
from src.models import *

# Register blueprints after all models are imported
def register_blueprints():
    # Import routes (after models to avoid circular imports)
    from src.routes.main import main_bp
    from src.routes.auth import auth_bp
    from src.routes.lessons import lessons_bp
    from src.routes.quiz import quiz_bp
    from src.routes.audio import audio_bp
    from src.routes.community import community_bp
    from src.routes.ai import ai_bp

    # Register blueprints
    app.register_blueprint(main_bp, url_prefix='/')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(lessons_bp, url_prefix='/lessons')
    app.register_blueprint(quiz_bp, url_prefix='/quiz')
    app.register_blueprint(audio_bp, url_prefix='/audio')
    app.register_blueprint(community_bp, url_prefix='/community')
    app.register_blueprint(ai_bp, url_prefix='/ai')

# Register blueprints
register_blueprints()

# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('errors/500.html'), 500

# Load user
@login_manager.user_loader
def load_user(user_id):
    from src.models import User
    return User.query.get(int(user_id))

# Run the app
if __name__ == '__main__':
    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()
    
    # Run the app
    app.run(debug=True, host='0.0.0.0')
