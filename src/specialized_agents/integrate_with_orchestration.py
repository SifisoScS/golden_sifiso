"""
Integration script for connecting specialized agents with the main Flask application.

This module provides functions to integrate the specialized agents system
with the main Golden Hand Flask application.
"""

from typing import Dict, List, Any
from flask import Blueprint, request, jsonify, render_template, current_app
from src.specialized_agents.agent_integrator import integrator
from src.specialized_agents.agent_registry import registry
from src.specialized_agents.agent_factory import AgentFactory
from src.specialized_agents.mathematics_navigator.math_agent import MathematicsAgent
from src.specialized_agents.science_illuminator.science_agent import ScienceAgent
from src.specialized_agents.technology_architect.tech_agent import TechnologyAgent


def initialize_agents():
    """
    Initialize and register all specialized agents.
    
    This function should be called during application startup to ensure
    all agents are registered and ready to use.
    
    Returns:
        bool: True if initialization was successful
    """
    # Register the specialized agents
    registry.register_agent("math_agent", MathematicsAgent)
    registry.register_agent("science_agent", ScienceAgent)
    registry.register_agent("tech_agent", TechnologyAgent)
    
    # Initialize the integrator
    success = integrator.initialize()
    
    return success


def create_specialized_agents_blueprint():
    """
    Create a Flask Blueprint for the specialized agents API.
    
    This function creates a Blueprint with routes for interacting with
    the specialized agents system.
    
    Returns:
        Blueprint: Flask Blueprint for specialized agents
    """
    specialized_agents_bp = Blueprint('specialized_agents', __name__, url_prefix='/api/specialized-agents')
    
    @specialized_agents_bp.route('/info', methods=['GET'])
    def get_agents_info():
        """Get information about all available agents."""
        return jsonify(integrator.get_agent_info())
    
    @specialized_agents_bp.route('/learning-path', methods=['POST'])
    def generate_learning_path():
        """Generate a learning path for a student."""
        data = request.json
        student_id = data.get('student_id', 0)
        grade_level = data.get('grade_level', 10)
        subjects = data.get('subjects', [])
        prior_knowledge = data.get('prior_knowledge', {})
        
        learning_path = integrator.generate_learning_path(
            student_id, grade_level, subjects, prior_knowledge
        )
        
        return jsonify(learning_path)
    
    @specialized_agents_bp.route('/content', methods=['POST'])
    def generate_content():
        """Generate content for a specific subject and topic."""
        data = request.json
        subject = data.get('subject', '')
        topic = data.get('topic', '')
        content_type = data.get('content_type', 'lesson')
        difficulty = data.get('difficulty', 'intermediate')
        grade_level = data.get('grade_level', 10)
        
        content = integrator.generate_content(
            subject, topic, content_type, difficulty, grade_level
        )
        
        return jsonify(content)
    
    @specialized_agents_bp.route('/analyze-performance', methods=['POST'])
    def analyze_performance():
        """Analyze a student's performance."""
        data = request.json
        student_id = data.get('student_id', 0)
        subject = data.get('subject', '')
        activity_results = data.get('activity_results', {})
        
        analysis = integrator.analyze_performance(
            student_id, subject, activity_results
        )
        
        return jsonify(analysis)
    
    @specialized_agents_bp.route('/answer-question', methods=['POST'])
    def answer_question():
        """Answer a student's question."""
        data = request.json
        question = data.get('question', '')
        subject = data.get('subject', None)
        context = data.get('context', {})
        
        answer = integrator.answer_question(
            question, subject, context
        )
        
        return jsonify(answer)
    
    @specialized_agents_bp.route('/suggest-resources', methods=['POST'])
    def suggest_resources():
        """Suggest learning resources."""
        data = request.json
        subject = data.get('subject', '')
        topic = data.get('topic', '')
        learning_style = data.get('learning_style', None)
        difficulty = data.get('difficulty', None)
        
        resources = integrator.suggest_resources(
            subject, topic, learning_style, difficulty
        )
        
        return jsonify(resources)
    
    @specialized_agents_bp.route('/entrepreneurship-connection', methods=['POST'])
    def get_entrepreneurship_connection():
        """Get entrepreneurship connections for a topic."""
        data = request.json
        subject = data.get('subject', '')
        topic = data.get('topic', '')
        grade_level = data.get('grade_level', 10)
        
        connection = integrator.get_entrepreneurship_connection(
            subject, topic, grade_level
        )
        
        return jsonify(connection)
    
    return specialized_agents_bp


def create_specialized_agents_ui_blueprint():
    """
    Create a Flask Blueprint for the specialized agents UI.
    
    This function creates a Blueprint with routes for the user interface
    of the specialized agents system.
    
    Returns:
        Blueprint: Flask Blueprint for specialized agents UI
    """
    specialized_agents_ui_bp = Blueprint(
        'specialized_agents_ui', 
        __name__, 
        url_prefix='/learning-platform',
        template_folder='../templates/specialized_agents'
    )
    
    @specialized_agents_ui_bp.route('/', methods=['GET'])
    def learning_platform_home():
        """Render the learning platform home page."""
        agent_info = integrator.get_agent_info()
        return render_template(
            'learning_platform.html',
            agent_info=agent_info
        )
    
    @specialized_agents_ui_bp.route('/subject/<subject>', methods=['GET'])
    def subject_page(subject):
        """Render the subject-specific page."""
        agent = integrator.get_agent_for_subject(subject)
        if agent is None:
            return render_template('subject_not_found.html', subject=subject)
        
        agent_info = agent.get_agent_info()
        return render_template(
            'subject.html',
            subject=subject,
            agent_info=agent_info
        )
    
    @specialized_agents_ui_bp.route('/learning-path', methods=['GET', 'POST'])
    def learning_path_page():
        """Render the learning path generation page."""
        if request.method == 'POST':
            # Process form submission
            student_id = int(request.form.get('student_id', 0))
            grade_level = int(request.form.get('grade_level', 10))
            subjects = request.form.getlist('subjects')
            
            learning_path = integrator.generate_learning_path(
                student_id, grade_level, subjects
            )
            
            return render_template(
                'learning_path_result.html',
                learning_path=learning_path
            )
        
        # GET request - show the form
        return render_template('learning_path_form.html')
    
    @specialized_agents_ui_bp.route('/entrepreneurship', methods=['GET'])
    def entrepreneurship_page():
        """Render the entrepreneurship connections page."""
        return render_template('entrepreneurship.html')
    
    return specialized_agents_ui_bp


def integrate_with_main_app(app):
    """
    Integrate the specialized agents system with the main Flask application.
    
    Args:
        app: The Flask application instance
        
    Returns:
        bool: True if integration was successful
    """
    # Initialize the agents
    success = initialize_agents()
    if not success:
        app.logger.error("Failed to initialize specialized agents")
        return False
    
    # Register the blueprints
    app.register_blueprint(create_specialized_agents_blueprint())
    app.register_blueprint(create_specialized_agents_ui_blueprint())
    
    # Add the integrator to the app context for easy access
    app.extensions['specialized_agents_integrator'] = integrator
    
    app.logger.info("Specialized agents system integrated successfully")
    return True
