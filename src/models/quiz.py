"""
Quiz models for The Golden Hand Learning Platform.

This module defines the models for quizzes, questions, and quiz results.
"""

from src.models.base import db
from datetime import datetime

class Quiz(db.Model):
    __tablename__ = 'quizzes'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.Text)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'))
    grade_level = db.Column(db.Integer)
    difficulty = db.Column(db.String(20))  # beginner, intermediate, advanced
    time_limit_minutes = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    questions = db.relationship('Question', backref='quiz', lazy='dynamic')
    results = db.relationship('QuizResult', backref='quiz', lazy='dynamic')
    attempts = db.relationship('QuizAttempt', backref='quiz', lazy='dynamic')
    
    def __repr__(self):
        return f'<Quiz {self.title}>'


class Question(db.Model):
    __tablename__ = 'questions'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'))
    question_text = db.Column(db.Text)
    question_type = db.Column(db.String(20))  # multiple_choice, true_false, short_answer
    points = db.Column(db.Integer, default=1)
    
    # Relationships
    options = db.relationship('QuestionOption', backref='question', lazy='dynamic')
    
    def __repr__(self):
        return f'<Question {self.id}>'


class QuestionOption(db.Model):
    __tablename__ = 'question_options'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'))
    option_text = db.Column(db.Text)
    is_correct = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return f'<QuestionOption {self.id}>'


class QuizAttempt(db.Model):
    __tablename__ = 'quiz_attempts'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'))
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime, nullable=True)
    is_completed = db.Column(db.Boolean, default=False)
    
    # Relationships
    result = db.relationship('QuizResult', backref='attempt', uselist=False)
    
    def __repr__(self):
        return f'<QuizAttempt {self.id}>'


class QuizResult(db.Model):
    __tablename__ = 'quiz_results'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'))
    attempt_id = db.Column(db.Integer, db.ForeignKey('quiz_attempts.id'), nullable=True)
    score = db.Column(db.Float)
    max_score = db.Column(db.Float)
    percentage = db.Column(db.Float)
    completion_time = db.Column(db.DateTime, default=datetime.utcnow)
    answers = db.Column(db.Text)  # JSON string of answers
    
    def __repr__(self):
        return f'<QuizResult {self.id}>'
