"""
Audio models for The Golden Hand Learning Platform.

This module defines the models for audio lessons and related functionality.
"""

from src.models.base import db
from datetime import datetime

class AudioLesson(db.Model):
    __tablename__ = 'audio_lessons'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.Text)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'))
    grade_level = db.Column(db.Integer)
    duration_minutes = db.Column(db.Integer)
    file_path = db.Column(db.String(255))
    language = db.Column(db.String(50), default='English')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    resources = db.relationship('AudioResource', backref='lesson', lazy='dynamic')
    progress = db.relationship('AudioProgress', backref='lesson', lazy='dynamic')
    
    def __repr__(self):
        return f'<AudioLesson {self.title}>'


class AudioResource(db.Model):
    __tablename__ = 'audio_resources'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    audio_lesson_id = db.Column(db.Integer, db.ForeignKey('audio_lessons.id'))
    title = db.Column(db.String(100))
    resource_type = db.Column(db.String(50))  # transcript, notes, supplementary_audio
    file_path = db.Column(db.String(255), nullable=True)
    content = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<AudioResource {self.title}>'


class AudioProgress(db.Model):
    __tablename__ = 'audio_progress'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    audio_lesson_id = db.Column(db.Integer, db.ForeignKey('audio_lessons.id'))
    progress_seconds = db.Column(db.Integer, default=0)
    total_seconds = db.Column(db.Integer)
    progress_percentage = db.Column(db.Float, default=0.0)
    completed = db.Column(db.Boolean, default=False)
    last_played = db.Column(db.DateTime, default=datetime.utcnow)
    completion_date = db.Column(db.DateTime, nullable=True)
    
    def __repr__(self):
        return f'<AudioProgress {self.id}>'


class AudioPlayback(db.Model):
    __tablename__ = 'audio_playbacks'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    audio_lesson_id = db.Column(db.Integer, db.ForeignKey('audio_lessons.id'))
    progress_seconds = db.Column(db.Integer, default=0)
    completed = db.Column(db.Boolean, default=False)
    last_played = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<AudioPlayback {self.id}>'
