from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Landing page route"""
    return render_template('index.html')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    """User dashboard route"""
    return render_template('dashboard.html')

@main_bp.route('/about')
def about():
    """About page route"""
    return render_template('about.html')

@main_bp.route('/contact')
def contact():
    """Contact page route"""
    return render_template('contact.html')

@main_bp.route('/profile')
@login_required
def profile():
    """User profile route"""
    return render_template('profile.html')
