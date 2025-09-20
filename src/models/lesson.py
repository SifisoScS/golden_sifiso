"""
Lesson models for The Golden Hand Learning Platform.

This module defines the models for lessons, subjects, topics, and related functionality.
"""

from src.models.base import db
from datetime import datetime

class Subject(db.Model):
    __tablename__ = 'subjects'
    __table_args__ = {
        'extend_existing': True,
        'sqlite_autoincrement': True,
        'unique_together': (('name', 'grade_level'),)
    }
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))  # No longer unique by itself
    description = db.Column(db.Text)
    grade_level = db.Column(db.Integer)  # 1-12 for grades, 13+ for tertiary
    curriculum_code = db.Column(db.String(50), nullable=True)  # For curriculum alignment tracking
    
    # Define a composite unique constraint for name and grade_level
    __table_args__ = (
        db.UniqueConstraint('name', 'grade_level', name='uix_subject_name_grade'),
        {'extend_existing': True}
    )
    
    # Relationships
    lessons = db.relationship('Lesson', backref='subject', lazy='dynamic')
    topics = db.relationship('Topic', backref='subject', lazy='dynamic')
    
    def __repr__(self):
        return f'<Subject {self.name} (Grade {self.grade_level})>'


class Topic(db.Model):
    __tablename__ = 'topics'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.Text)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'))
    grade_level = db.Column(db.Integer)
    curriculum_code = db.Column(db.String(50), nullable=True)  # For curriculum alignment tracking
    
    # Relationships
    lessons = db.relationship('Lesson', backref='topic', lazy='dynamic')
    
    def __repr__(self):
        return f'<Topic {self.name}>'


class Lesson(db.Model):
    __tablename__ = 'lessons'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'))
    topic_id = db.Column(db.Integer, db.ForeignKey('topics.id'), nullable=True)
    grade_level = db.Column(db.Integer)
    difficulty = db.Column(db.String(20))  # beginner, intermediate, advanced
    duration_minutes = db.Column(db.Integer)
    learning_objectives = db.Column(db.Text, nullable=True)
    prerequisites = db.Column(db.Text, nullable=True)
    is_generated = db.Column(db.Boolean, default=False)  # Flag for agent-generated content
    generator_agent = db.Column(db.String(50), nullable=True)  # Which agent generated this
    curriculum_alignment = db.Column(db.Text, nullable=True)  # Details on curriculum standards alignment
    entrepreneurship_connection = db.Column(db.Text, nullable=True)  # Connection to entrepreneurship
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    progress = db.relationship('LessonProgress', backref='lesson', lazy='dynamic')
    resources = db.relationship('LessonResource', backref='lesson', lazy='dynamic')
    sections = db.relationship('LessonSection', backref='lesson', lazy='dynamic', order_by='LessonSection.order')
    activities = db.relationship('LessonActivity', backref='lesson', lazy='dynamic')
    
    def __repr__(self):
        return f'<Lesson {self.title}>'


class LessonSection(db.Model):
    __tablename__ = 'lesson_sections'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lessons.id'))
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    order = db.Column(db.Integer)  # For ordering sections within a lesson
    
    def __repr__(self):
        return f'<LessonSection {self.title}>'


class LessonActivity(db.Model):
    __tablename__ = 'lesson_activities'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lessons.id'))
    title = db.Column(db.String(100))
    activity_type = db.Column(db.String(50))  # exercise, quiz, project, discussion
    instructions = db.Column(db.Text)
    content = db.Column(db.Text, nullable=True)  # JSON content for interactive activities
    duration_minutes = db.Column(db.Integer)
    
    def __repr__(self):
        return f'<LessonActivity {self.title}>'


class LessonResource(db.Model):
    __tablename__ = 'lesson_resources'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lessons.id'))
    title = db.Column(db.String(100))
    resource_type = db.Column(db.String(50))  # video, document, link, code, image
    url = db.Column(db.String(255), nullable=True)
    content = db.Column(db.Text, nullable=True)  # For embedded content
    is_generated = db.Column(db.Boolean, default=False)  # Flag for agent-generated resources
    
    def __repr__(self):
        return f'<LessonResource {self.title}>'


class LessonProgress(db.Model):
    __tablename__ = 'lesson_progress'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    lesson_id = db.Column(db.Integer, db.ForeignKey('lessons.id'))
    status = db.Column(db.String(20))  # not_started, in_progress, completed
    progress_percentage = db.Column(db.Float, default=0.0)
    last_activity_date = db.Column(db.DateTime, default=datetime.utcnow)
    completion_date = db.Column(db.DateTime, nullable=True)
    
    def __repr__(self):
        return f'<LessonProgress {self.user_id}:{self.lesson_id}>'


class CurriculumStandard(db.Model):
    __tablename__ = 'curriculum_standards'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True)
    description = db.Column(db.Text)
    subject_area = db.Column(db.String(100))
    grade_level = db.Column(db.Integer)
    category = db.Column(db.String(100))  # e.g., "Number Operations", "Scientific Method"
    
    def __repr__(self):
        return f'<CurriculumStandard {self.code}>'
