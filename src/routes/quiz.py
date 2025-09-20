from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from src.models.quiz import Quiz, Question, QuestionOption

quiz_bp = Blueprint('quiz', __name__)

@quiz_bp.route('/')
@login_required
def index():
    """Quiz app home page"""
    quizzes = Quiz.query.all()
    return render_template('quiz/index.html', quizzes=quizzes)

@quiz_bp.route('/<int:quiz_id>')
@login_required
def quiz_details(quiz_id):
    """Quiz details page"""
    quiz = Quiz.query.get_or_404(quiz_id)
    return render_template('quiz/details.html', quiz=quiz)

@quiz_bp.route('/<int:quiz_id>/start')
@login_required
def start_quiz(quiz_id):
    """Start quiz page"""
    quiz = Quiz.query.get_or_404(quiz_id)
    return render_template('quiz/start.html', quiz=quiz)

@quiz_bp.route('/<int:quiz_id>/question/<int:question_id>')
@login_required
def question(quiz_id, question_id):
    """Individual question page"""
    quiz = Quiz.query.get_or_404(quiz_id)
    question = Question.query.get_or_404(question_id)
    return render_template('quiz/question.html', quiz=quiz, question=question)

@quiz_bp.route('/<int:quiz_id>/results')
@login_required
def results(quiz_id):
    """Quiz results page"""
    quiz = Quiz.query.get_or_404(quiz_id)
    return render_template('quiz/results.html', quiz=quiz)
