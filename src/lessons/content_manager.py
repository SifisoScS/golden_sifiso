"""
Lessons Platform Content Manager for The Golden Hand Learning Platform.

This module implements the content storage and retrieval system for
dynamically generated lessons, ensuring efficient access and persistence.
"""

from typing import Dict, List, Any, Optional, Tuple
import json
import os
from datetime import datetime
import threading
import time

from src.models.lesson import (
    Subject, Topic, Lesson, LessonSection, LessonActivity, 
    LessonResource, CurriculumStandard, LessonProgress
)
from src.main import db, app
from src.lessons.generator import lesson_generator


class LessonContentManager:
    """
    Manages storage and retrieval of lesson content.
    
    This class provides methods for storing, retrieving, and caching
    dynamically generated lesson content, ensuring efficient access
    and persistence.
    """
    
    def __init__(self):
        """Initialize the lesson content manager."""
        self.cache = {}
        self.cache_lock = threading.Lock()
        self.cache_expiry = 3600  # Cache expiry in seconds (1 hour)
        
        # Create cache directory if it doesn't exist
        self.cache_dir = os.path.join(app.instance_path, 'lesson_cache')
        os.makedirs(self.cache_dir, exist_ok=True)
    
    def get_subject(self, subject_id: int) -> Optional[Subject]:
        """
        Get a subject by ID.
        
        Args:
            subject_id: The subject ID
            
        Returns:
            Subject object or None if not found
        """
        return Subject.query.get(subject_id)
    
    def get_subjects_by_grade(self, grade_level: int) -> List[Subject]:
        """
        Get all subjects for a specific grade level.
        
        Args:
            grade_level: The grade level
            
        Returns:
            List of Subject objects
        """
        return Subject.query.filter_by(grade_level=grade_level).all()
    
    def get_or_create_subject(self, name: str, grade_level: int) -> Subject:
        """
        Get a subject by name and grade level, or create it if it doesn't exist.
        
        Args:
            name: The subject name
            grade_level: The grade level
            
        Returns:
            Subject object
        """
        subject = Subject.query.filter_by(name=name, grade_level=grade_level).first()
        
        if not subject:
            subject = Subject(
                name=name,
                description=f"{name} for Grade {grade_level}",
                grade_level=grade_level
            )
            db.session.add(subject)
            db.session.commit()
        
        return subject
    
    def get_topic(self, topic_id: int) -> Optional[Topic]:
        """
        Get a topic by ID.
        
        Args:
            topic_id: The topic ID
            
        Returns:
            Topic object or None if not found
        """
        return Topic.query.get(topic_id)
    
    def get_topics_by_subject(self, subject_id: int) -> List[Topic]:
        """
        Get all topics for a specific subject.
        
        Args:
            subject_id: The subject ID
            
        Returns:
            List of Topic objects
        """
        return Topic.query.filter_by(subject_id=subject_id).all()
    
    def get_or_create_topic(self, name: str, subject_id: int, grade_level: int) -> Topic:
        """
        Get a topic by name and subject, or create it if it doesn't exist.
        
        Args:
            name: The topic name
            subject_id: The subject ID
            grade_level: The grade level
            
        Returns:
            Topic object
        """
        topic = Topic.query.filter_by(name=name, subject_id=subject_id).first()
        
        if not topic:
            subject = Subject.query.get(subject_id)
            topic = Topic(
                name=name,
                description=f"Topic in {subject.name} for Grade {grade_level}",
                subject_id=subject_id,
                grade_level=grade_level
            )
            db.session.add(topic)
            db.session.commit()
        
        return topic
    
    def get_lesson(self, lesson_id: int) -> Optional[Lesson]:
        """
        Get a lesson by ID.
        
        Args:
            lesson_id: The lesson ID
            
        Returns:
            Lesson object or None if not found
        """
        return Lesson.query.get(lesson_id)
    
    def get_lessons_by_topic(self, topic_id: int) -> List[Lesson]:
        """
        Get all lessons for a specific topic.
        
        Args:
            topic_id: The topic ID
            
        Returns:
            List of Lesson objects
        """
        return Lesson.query.filter_by(topic_id=topic_id).all()
    
    def get_lessons_by_subject(self, subject_id: int) -> List[Lesson]:
        """
        Get all lessons for a specific subject.
        
        Args:
            subject_id: The subject ID
            
        Returns:
            List of Lesson objects
        """
        return Lesson.query.filter_by(subject_id=subject_id).all()
    
    def get_lessons_by_grade(self, grade_level: int) -> List[Lesson]:
        """
        Get all lessons for a specific grade level.
        
        Args:
            grade_level: The grade level
            
        Returns:
            List of Lesson objects
        """
        return Lesson.query.filter_by(grade_level=grade_level).all()
    
    def get_lesson_sections(self, lesson_id: int) -> List[LessonSection]:
        """
        Get all sections for a specific lesson.
        
        Args:
            lesson_id: The lesson ID
            
        Returns:
            List of LessonSection objects
        """
        return LessonSection.query.filter_by(lesson_id=lesson_id).order_by(LessonSection.order).all()
    
    def get_lesson_activities(self, lesson_id: int) -> List[LessonActivity]:
        """
        Get all activities for a specific lesson.
        
        Args:
            lesson_id: The lesson ID
            
        Returns:
            List of LessonActivity objects
        """
        return LessonActivity.query.filter_by(lesson_id=lesson_id).all()
    
    def get_lesson_resources(self, lesson_id: int) -> List[LessonResource]:
        """
        Get all resources for a specific lesson.
        
        Args:
            lesson_id: The lesson ID
            
        Returns:
            List of LessonResource objects
        """
        return LessonResource.query.filter_by(lesson_id=lesson_id).all()
    
    def get_or_generate_lesson(self, 
                              subject_name: str, 
                              topic_name: str, 
                              grade_level: int, 
                              difficulty: str = "intermediate") -> Lesson:
        """
        Get a lesson by subject, topic, and grade level, or generate it if it doesn't exist.
        
        Args:
            subject_name: The subject name
            topic_name: The topic name
            grade_level: The grade level
            difficulty: The difficulty level
            
        Returns:
            Lesson object
        """
        # Get or create subject
        subject = self.get_or_create_subject(subject_name, grade_level)
        
        # Get or create topic
        topic = self.get_or_create_topic(topic_name, subject.id, grade_level)
        
        # Check if lesson exists
        lesson = Lesson.query.filter_by(topic_id=topic.id, difficulty=difficulty).first()
        
        if not lesson:
            # Generate lesson
            lesson_data = lesson_generator.generate_lesson(
                subject_name=subject_name,
                topic=topic_name,
                grade_level=grade_level,
                difficulty=difficulty
            )
            
            # Save to database
            lesson = lesson_generator.save_lesson_to_database(lesson_data)
        
        return lesson
    
    def get_lesson_progress(self, user_id: int, lesson_id: int) -> Optional[LessonProgress]:
        """
        Get a user's progress for a specific lesson.
        
        Args:
            user_id: The user ID
            lesson_id: The lesson ID
            
        Returns:
            LessonProgress object or None if not found
        """
        return LessonProgress.query.filter_by(user_id=user_id, lesson_id=lesson_id).first()
    
    def update_lesson_progress(self, 
                              user_id: int, 
                              lesson_id: int, 
                              status: str, 
                              progress_percentage: float) -> LessonProgress:
        """
        Update a user's progress for a specific lesson.
        
        Args:
            user_id: The user ID
            lesson_id: The lesson ID
            status: The status (not_started, in_progress, completed)
            progress_percentage: The progress percentage
            
        Returns:
            LessonProgress object
        """
        progress = self.get_lesson_progress(user_id, lesson_id)
        
        if not progress:
            progress = LessonProgress(
                user_id=user_id,
                lesson_id=lesson_id,
                status=status,
                progress_percentage=progress_percentage,
                last_activity_date=datetime.utcnow()
            )
            db.session.add(progress)
        else:
            progress.status = status
            progress.progress_percentage = progress_percentage
            progress.last_activity_date = datetime.utcnow()
            
            if status == "completed" and not progress.completion_date:
                progress.completion_date = datetime.utcnow()
        
        db.session.commit()
        return progress
    
    def get_user_progress_summary(self, user_id: int) -> Dict[str, Any]:
        """
        Get a summary of a user's progress across all lessons.
        
        Args:
            user_id: The user ID
            
        Returns:
            Dictionary containing progress summary
        """
        # Get all progress records for this user
        progress_records = LessonProgress.query.filter_by(user_id=user_id).all()
        
        # Calculate summary statistics
        total_lessons = len(progress_records)
        completed_lessons = sum(1 for p in progress_records if p.status == "completed")
        in_progress_lessons = sum(1 for p in progress_records if p.status == "in_progress")
        not_started_lessons = sum(1 for p in progress_records if p.status == "not_started")
        
        # Calculate average progress
        if total_lessons > 0:
            average_progress = sum(p.progress_percentage for p in progress_records) / total_lessons
        else:
            average_progress = 0.0
        
        # Get progress by subject
        progress_by_subject = {}
        for progress in progress_records:
            lesson = self.get_lesson(progress.lesson_id)
            if not lesson:
                continue
                
            subject = self.get_subject(lesson.subject_id)
            if not subject:
                continue
                
            if subject.name not in progress_by_subject:
                progress_by_subject[subject.name] = {
                    "total": 0,
                    "completed": 0,
                    "in_progress": 0,
                    "not_started": 0,
                    "average_progress": 0.0
                }
            
            progress_by_subject[subject.name]["total"] += 1
            
            if progress.status == "completed":
                progress_by_subject[subject.name]["completed"] += 1
            elif progress.status == "in_progress":
                progress_by_subject[subject.name]["in_progress"] += 1
            else:
                progress_by_subject[subject.name]["not_started"] += 1
            
            # Update average progress
            current_total = progress_by_subject[subject.name]["total"]
            current_avg = progress_by_subject[subject.name]["average_progress"]
            new_avg = ((current_avg * (current_total - 1)) + progress.progress_percentage) / current_total
            progress_by_subject[subject.name]["average_progress"] = new_avg
        
        # Get progress by grade
        progress_by_grade = {}
        for progress in progress_records:
            lesson = self.get_lesson(progress.lesson_id)
            if not lesson:
                continue
                
            grade = lesson.grade_level
            if grade not in progress_by_grade:
                progress_by_grade[grade] = {
                    "total": 0,
                    "completed": 0,
                    "in_progress": 0,
                    "not_started": 0,
                    "average_progress": 0.0
                }
            
            progress_by_grade[grade]["total"] += 1
            
            if progress.status == "completed":
                progress_by_grade[grade]["completed"] += 1
            elif progress.status == "in_progress":
                progress_by_grade[grade]["in_progress"] += 1
            else:
                progress_by_grade[grade]["not_started"] += 1
            
            # Update average progress
            current_total = progress_by_grade[grade]["total"]
            current_avg = progress_by_grade[grade]["average_progress"]
            new_avg = ((current_avg * (current_total - 1)) + progress.progress_percentage) / current_total
            progress_by_grade[grade]["average_progress"] = new_avg
        
        return {
            "total_lessons": total_lessons,
            "completed_lessons": completed_lessons,
            "in_progress_lessons": in_progress_lessons,
            "not_started_lessons": not_started_lessons,
            "average_progress": average_progress,
            "progress_by_subject": progress_by_subject,
            "progress_by_grade": progress_by_grade
        }
    
    def cache_lesson(self, lesson_id: int) -> None:
        """
        Cache a lesson for faster retrieval.
        
        Args:
            lesson_id: The lesson ID
        """
        lesson = self.get_lesson(lesson_id)
        if not lesson:
            return
        
        # Get all related data
        subject = self.get_subject(lesson.subject_id)
        topic = self.get_topic(lesson.topic_id) if lesson.topic_id else None
        sections = self.get_lesson_sections(lesson_id)
        activities = self.get_lesson_activities(lesson_id)
        resources = self.get_lesson_resources(lesson_id)
        
        # Format data for caching
        lesson_data = {
            "id": lesson.id,
            "title": lesson.title,
            "content": lesson.content,
            "subject": {
                "id": subject.id,
                "name": subject.name,
                "description": subject.description,
                "grade_level": subject.grade_level
            },
            "topic": None if not topic else {
                "id": topic.id,
                "name": topic.name,
                "description": topic.description
            },
            "grade_level": lesson.grade_level,
            "difficulty": lesson.difficulty,
            "duration_minutes": lesson.duration_minutes,
            "learning_objectives": json.loads(lesson.learning_objectives) if lesson.learning_objectives else [],
            "entrepreneurship_connection": json.loads(lesson.entrepreneurship_connection) if lesson.entrepreneurship_connection else {},
            "is_generated": lesson.is_generated,
            "generator_agent": lesson.generator_agent,
            "sections": [
                {
                    "id": section.id,
                    "title": section.title,
                    "content": section.content,
                    "order": section.order
                }
                for section in sections
            ],
            "activities": [
                {
                    "id": activity.id,
                    "title": activity.title,
                    "activity_type": activity.activity_type,
                    "instructions": activity.instructions,
                    "content": json.loads(activity.content) if activity.content else {},
                    "duration_minutes": activity.duration_minutes
                }
                for activity in activities
            ],
            "resources": [
                {
                    "id": resource.id,
                    "title": resource.title,
                    "resource_type": resource.resource_type,
                    "url": resource.url,
                    "content": json.loads(resource.content) if resource.content else {},
                    "is_generated": resource.is_generated
                }
                for resource in resources
            ],
            "cache_time": time.time()
        }
        
        # Store in memory cache
        with self.cache_lock:
            self.cache[lesson_id] = lesson_data
        
        # Store in file cache
        cache_file = os.path.join(self.cache_dir, f"lesson_{lesson_id}.json")
        with open(cache_file, 'w') as f:
            json.dump(lesson_data, f)
    
    def get_cached_lesson(self, lesson_id: int) -> Optional[Dict[str, Any]]:
        """
        Get a cached lesson.
        
        Args:
            lesson_id: The lesson ID
            
        Returns:
            Dictionary containing lesson data or None if not cached
        """
        # Check memory cache first
        with self.cache_lock:
            if lesson_id in self.cache:
                cache_time = self.cache[lesson_id].get("cache_time", 0)
                if time.time() - cache_time < self.cache_expiry:
                    return self.cache[lesson_id]
        
        # Check file cache
        cache_file = os.path.join(self.cache_dir, f"lesson_{lesson_id}.json")
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'r') as f:
                    lesson_data = json.load(f)
                
                cache_time = lesson_data.get("cache_time", 0)
                if time.time() - cache_time < self.cache_expiry:
                    # Update memory cache
                    with self.cache_lock:
                        self.cache[lesson_id] = lesson_data
                    return lesson_data
            except:
                pass
        
        return None
    
    def get_lesson_with_details(self, lesson_id: int) -> Dict[str, Any]:
        """
        Get a lesson with all related details, using cache if available.
        
        Args:
            lesson_id: The lesson ID
            
        Returns:
            Dictionary containing lesson data
        """
        # Check cache first
        cached_lesson = self.get_cached_lesson(lesson_id)
        if cached_lesson:
            return cached_lesson
        
        # If not cached, fetch from database and cache
        lesson = self.get_lesson(lesson_id)
        if not lesson:
            return {}
        
        # Cache the lesson
        self.cache_lesson(lesson_id)
        
        # Return the cached version
        return self.get_cached_lesson(lesson_id) or {}
    
    def invalidate_cache(self, lesson_id: int) -> None:
        """
        Invalidate the cache for a specific lesson.
        
        Args:
            lesson_id: The lesson ID
        """
        # Remove from memory cache
        with self.cache_lock:
            if lesson_id in self.cache:
                del self.cache[lesson_id]
        
        # Remove from file cache
        cache_file = os.path.join(self.cache_dir, f"lesson_{lesson_id}.json")
        if os.path.exists(cache_file):
            os.remove(cache_file)
    
    def clear_cache(self) -> None:
        """Clear all cached lessons."""
        # Clear memory cache
        with self.cache_lock:
            self.cache.clear()
        
        # Clear file cache
        for filename in os.listdir(self.cache_dir):
            if filename.startswith("lesson_") and filename.endswith(".json"):
                os.remove(os.path.join(self.cache_dir, filename))


# Create a global content manager instance
content_manager = LessonContentManager()
