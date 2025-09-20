"""
AI models for The Golden Hand Learning Platform.

This module defines the models for AI projects, resources, and related functionality.
"""

from src.models.base import db
from datetime import datetime

class AIProject(db.Model):
    __tablename__ = 'ai_projects'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    project_type = db.Column(db.String(50))  # chatbot, image_recognition, nlp, etc.
    status = db.Column(db.String(20))  # draft, in_progress, completed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    datasets = db.relationship('AIDataset', backref='project', lazy='dynamic')
    models = db.relationship('AIModel', backref='project', lazy='dynamic')
    resources = db.relationship('AIResource', backref='project', lazy='dynamic')
    progress = db.relationship('AIProgress', backref='project', lazy='dynamic')
    
    def __repr__(self):
        return f'<AIProject {self.title}>'


class AIDataset(db.Model):
    __tablename__ = 'ai_datasets'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('ai_projects.id'))
    name = db.Column(db.String(100))
    description = db.Column(db.Text)
    file_path = db.Column(db.String(255))
    data_type = db.Column(db.String(50))  # text, image, audio, tabular
    size_mb = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<AIDataset {self.name}>'


class AIModel(db.Model):
    __tablename__ = 'ai_models'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('ai_projects.id'))
    name = db.Column(db.String(100))
    description = db.Column(db.Text)
    model_type = db.Column(db.String(50))  # classification, regression, generative
    architecture = db.Column(db.String(100))  # cnn, rnn, transformer, etc.
    accuracy = db.Column(db.Float)
    file_path = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<AIModel {self.name}>'


class AIResource(db.Model):
    __tablename__ = 'ai_resources'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('ai_projects.id'))
    title = db.Column(db.String(100))
    description = db.Column(db.Text)
    resource_type = db.Column(db.String(50))  # tutorial, documentation, code_sample, dataset
    content = db.Column(db.Text, nullable=True)
    file_path = db.Column(db.String(255), nullable=True)
    url = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<AIResource {self.title}>'


class AIProgress(db.Model):
    __tablename__ = 'ai_progress'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    project_id = db.Column(db.Integer, db.ForeignKey('ai_projects.id'))
    status = db.Column(db.String(20))  # not_started, in_progress, completed
    progress_percentage = db.Column(db.Float, default=0.0)
    last_activity_date = db.Column(db.DateTime, default=datetime.utcnow)
    completion_date = db.Column(db.DateTime, nullable=True)
    
    def __repr__(self):
        return f'<AIProgress {self.id}>'


class AITutorial(db.Model):
    __tablename__ = 'ai_tutorials'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.Text)
    content = db.Column(db.Text)
    difficulty = db.Column(db.String(20))  # beginner, intermediate, advanced
    category = db.Column(db.String(50))  # machine_learning, deep_learning, nlp, etc.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<AITutorial {self.title}>'
