from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from src.models.ai import AIProject, AIDataset, AIModel, AITutorial

ai_bp = Blueprint('ai', __name__)

@ai_bp.route('/')
@login_required
def index():
    """iKhaya AI hub home page"""
    projects = AIProject.query.filter_by(user_id=current_user.id).all()
    tutorials = AITutorial.query.order_by(AITutorial.difficulty).all()
    return render_template('ai/index.html', projects=projects, tutorials=tutorials)

@ai_bp.route('/projects')
@login_required
def projects():
    """AI projects listing page"""
    projects = AIProject.query.filter_by(user_id=current_user.id).all()
    return render_template('ai/projects.html', projects=projects)

@ai_bp.route('/project/<int:project_id>')
@login_required
def project_details(project_id):
    """AI project details page"""
    project = AIProject.query.get_or_404(project_id)
    # Ensure user owns this project
    if project.user_id != current_user.id:
        flash('You do not have permission to view this project.', 'danger')
        return redirect(url_for('ai.projects'))
    datasets = AIDataset.query.filter_by(project_id=project_id).all()
    models = AIModel.query.filter_by(project_id=project_id).all()
    return render_template('ai/project_details.html', project=project, datasets=datasets, models=models)

@ai_bp.route('/tutorials')
@login_required
def tutorials():
    """AI tutorials listing page"""
    difficulty = request.args.get('difficulty')
    category = request.args.get('category')
    
    query = AITutorial.query
    if difficulty:
        query = query.filter_by(difficulty=difficulty)
    if category:
        query = query.filter_by(category=category)
        
    tutorials = query.all()
    return render_template('ai/tutorials.html', tutorials=tutorials, selected_difficulty=difficulty, selected_category=category)

@ai_bp.route('/tutorial/<int:tutorial_id>')
@login_required
def tutorial_details(tutorial_id):
    """AI tutorial details page"""
    tutorial = AITutorial.query.get_or_404(tutorial_id)
    return render_template('ai/tutorial_details.html', tutorial=tutorial)

@ai_bp.route('/playground')
@login_required
def playground():
    """AI playground for experimenting with models"""
    return render_template('ai/playground.html')

@ai_bp.route('/resources')
@login_required
def resources():
    """AI learning resources page"""
    return render_template('ai/resources.html')
