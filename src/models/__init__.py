"""
Models package for The Golden Hand Learning Platform.

This module centralizes all database model definitions to avoid
duplicate model registration issues with SQLAlchemy.
"""

# Import all models here to ensure they are only defined once
from src.models.base import db
from src.models.user import User
from src.models.lesson import (
    Subject, Topic, Lesson, LessonSection, 
    LessonActivity, LessonResource, LessonProgress, 
    CurriculumStandard
)
from src.models.quiz import (
    Quiz, Question, QuestionOption, 
    QuizAttempt, QuizResult
)
from src.models.audio import (
    AudioLesson, AudioResource, 
    AudioProgress, AudioPlayback
)
from src.models.community import (
    Community, CommunityPost, Comment, 
    UserConnection, CommunityMembership, 
    Startup, StartupTeam, PostComment
)
from src.models.ai import (
    AIProject, AIResource, AIProgress, 
    AIDataset, AIModel, AITutorial
)

# Export all models for easy importing
__all__ = [
    'db',
    'User',
    'Subject', 'Topic', 'Lesson', 'LessonSection', 
    'LessonActivity', 'LessonResource', 'LessonProgress', 
    'CurriculumStandard',
    'Quiz', 'Question', 'QuestionOption', 
    'QuizAttempt', 'QuizResult',
    'AudioLesson', 'AudioResource', 
    'AudioProgress', 'AudioPlayback',
    'Community', 'CommunityPost', 'Comment', 
    'UserConnection', 'CommunityMembership', 
    'Startup', 'StartupTeam', 'PostComment',
    'AIProject', 'AIResource', 'AIProgress', 
    'AIDataset', 'AIModel', 'AITutorial'
]
