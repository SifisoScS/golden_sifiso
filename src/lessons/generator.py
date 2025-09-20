"""
Lesson Content Generator for The Golden Hand Learning Platform.

This module implements the dynamic content generation pipeline using specialized agents
to create curriculum-aligned lesson content for grades 4-9.
"""

from typing import Dict, List, Any, Optional, Tuple
import json
from datetime import datetime

from src.specialized_agents.agent_integrator import integrator
from src.specialized_agents.base_agent import ContentType, LearningLevel
from src.models.lesson import (
    Subject, Topic, Lesson, LessonSection, LessonActivity, 
    LessonResource, CurriculumStandard
)
from src.main import db


class LessonContentGenerator:
    """
    Generates dynamic lesson content using specialized agents.
    
    This class coordinates with the specialized agents to generate
    curriculum-aligned lesson content for different subjects and grade levels.
    """
    
    def __init__(self):
        """Initialize the lesson content generator."""
        # Ensure the agent integrator is initialized
        self.integrator = integrator
        if not self.integrator.initialized:
            self.integrator.initialize()
    
    def generate_subject_curriculum(self, subject_name: str, grade_levels: List[int]) -> Dict[str, Any]:
        """
        Generate a curriculum structure for a subject across multiple grade levels.
        
        Args:
            subject_name: The name of the subject
            grade_levels: List of grade levels to generate curriculum for
            
        Returns:
            Dictionary containing the curriculum structure
        """
        # Map subject name to agent subject
        agent_subject = self._map_subject_to_agent_subject(subject_name)
        
        curriculum = {
            "subject": subject_name,
            "grade_levels": {}
        }
        
        for grade in grade_levels:
            # Get the appropriate agent for this subject
            agent = self.integrator.get_agent_for_subject(agent_subject)
            if not agent:
                continue
                
            # Get topics for this grade level from the agent
            if hasattr(agent, 'topics_by_grade') and grade in agent.topics_by_grade:
                topics = agent.topics_by_grade[grade]
            else:
                # Fallback to generating topics
                topics = self._generate_topics_for_grade(agent_subject, grade)
            
            curriculum["grade_levels"][grade] = {
                "topics": topics
            }
            
            # Save topics to database
            self._save_topics_to_database(subject_name, topics, grade)
        
        return curriculum
    
    def _save_topics_to_database(self, subject_name: str, topics: List[str], grade: int) -> None:
        """
        Save generated topics to the database.
        
        Args:
            subject_name: The name of the subject
            topics: List of topic names
            grade: The grade level
        """
        # Get the subject
        subject = Subject.query.filter_by(name=subject_name, grade_level=grade).first()
        if not subject:
            print(f"Subject {subject_name} for grade {grade} not found, skipping topic creation")
            return
        
        # Create topics
        for topic_name in topics:
            # Check if topic already exists
            topic = Topic.query.filter_by(name=topic_name, subject_id=subject.id).first()
            if not topic:
                topic = Topic(
                    name=topic_name,
                    description=f"Topic in {subject_name} for Grade {grade}",
                    subject_id=subject.id,
                    grade_level=grade
                )
                db.session.add(topic)
                print(f"Created topic: {topic_name}")
            else:
                print(f"Topic already exists: {topic_name}")
        
        db.session.commit()
    
    def _generate_topics_for_grade(self, subject: str, grade: int) -> List[str]:
        """
        Generate a list of topics for a subject at a specific grade level.
        
        Args:
            subject: The subject name
            grade: The grade level
            
        Returns:
            List of topic names
        """
        # This is a fallback method if the agent doesn't have predefined topics
        
        # Mathematics topics by grade
        math_topics = {
            4: ["Whole Numbers", "Fractions", "Decimals", "Measurement", "Geometry", "Data Handling"],
            5: ["Number Concepts", "Operations", "Fractions and Decimals", "Measurement", "Geometry", "Data Analysis"],
            6: ["Number Theory", "Ratios and Proportions", "Algebra Introduction", "Geometry", "Statistics", "Probability"],
            7: ["Integers", "Rational Numbers", "Algebraic Expressions", "Equations", "Geometry", "Statistics"],
            8: ["Real Numbers", "Exponents", "Scientific Notation", "Linear Equations", "Geometry", "Data Analysis"],
            9: ["Number Systems", "Algebraic Expressions", "Linear Equations and Inequalities", "Functions", "Geometry", "Statistics and Probability"]
        }
        
        # Science topics by grade
        science_topics = {
            4: ["Living Things", "Materials and Matter", "Energy and Change", "Planet Earth and Beyond"],
            5: ["Life Cycles", "Ecosystems", "Matter and Materials", "Energy and Movement", "Earth and Space"],
            6: ["Biodiversity", "Nutrition", "Matter and Materials", "Energy and Change", "Earth and Beyond"],
            7: ["The Biosphere", "Biodiversity", "Properties of Materials", "Energy Transfer", "Earth Systems"],
            8: ["Cells and Systems", "Photosynthesis", "Chemical Reactions", "Electricity", "The Solar System"],
            9: ["Cell Division", "Human Systems", "Compounds and Reactions", "Forces and Energy", "Earth's Spheres"]
        }
        
        # Technology topics by grade
        technology_topics = {
            4: ["Basic Computer Skills", "Digital Storytelling", "Introduction to Coding", "Online Safety"],
            5: ["Word Processing", "Digital Art", "Block Coding", "Digital Citizenship"],
            6: ["Spreadsheet Basics", "Animation", "Computational Thinking", "Digital Research"],
            7: ["Digital Design", "Web Development", "Programming with Python", "Data Collection"],
            8: ["App Design", "Advanced Web Development", "Programming Projects", "Digital Solutions"],
            9: ["Computer Science Principles", "Web Applications", "Python Programming", "Database Basics"]
        }
        
        # Select topics based on subject and grade
        if subject.lower() in ["mathematics", "math", "maths"]:
            return math_topics.get(grade, ["Arithmetic", "Algebra", "Geometry", "Data Analysis"])
        elif subject.lower() in ["science", "natural science"]:
            return science_topics.get(grade, ["Life Sciences", "Physical Sciences", "Earth Sciences"])
        elif subject.lower() in ["technology", "computer science", "computing"]:
            return technology_topics.get(grade, ["Computer Skills", "Programming", "Digital Literacy"])
        else:
            # Generic topics for other subjects
            return ["Topic 1", "Topic 2", "Topic 3", "Topic 4"]
    
    def _map_subject_to_agent_subject(self, subject_name: str) -> str:
        """
        Map a subject name to the corresponding agent subject.
        
        Args:
            subject_name: The name of the subject
            
        Returns:
            The corresponding agent subject name
        """
        subject_mapping = {
            "mathematics": "mathematics",
            "maths": "mathematics",
            "math": "mathematics",
            
            "science": "science",
            "natural science": "science",
            "physical science": "science",
            "life science": "science",
            
            "technology": "technology",
            "computer science": "technology",
            "computing": "technology",
            "digital literacy": "technology",
            "information technology": "technology"
        }
        
        return subject_mapping.get(subject_name.lower(), subject_name.lower())
    
    def generate_lesson(self, 
                       subject_name: str, 
                       topic: str, 
                       grade_level: int, 
                       difficulty: str = "intermediate") -> Dict[str, Any]:
        """
        Generate a complete lesson for a specific subject, topic, and grade level.
        
        Args:
            subject_name: The name of the subject
            topic: The specific topic
            grade_level: The target grade level
            difficulty: The difficulty level (beginner, intermediate, advanced)
            
        Returns:
            Dictionary containing the generated lesson content
        """
        # Map subject name to agent subject
        agent_subject = self._map_subject_to_agent_subject(subject_name)
        
        # Generate the lesson content using the appropriate agent
        content = self.integrator.generate_content(
            subject=agent_subject,
            topic=topic,
            content_type=ContentType.LESSON.value,
            difficulty=difficulty,
            grade_level=grade_level
        )
        
        # Get entrepreneurship connection
        entrepreneurship_connection = self.integrator.get_entrepreneurship_connection(
            subject=agent_subject,
            topic=topic,
            grade_level=grade_level
        )
        
        # Format the lesson content
        lesson = {
            "title": content.get("title", f"{topic} - Grade {grade_level}"),
            "subject": subject_name,
            "topic": topic,
            "grade_level": grade_level,
            "difficulty": difficulty,
            "learning_objectives": content.get("objectives", []),
            "introduction": content.get("introduction", ""),
            "sections": content.get("sections", []),
            "summary": content.get("summary", ""),
            "activities": [],
            "resources": [],
            "entrepreneurship_connection": entrepreneurship_connection,
            "is_generated": True,
            "generator_agent": agent_subject,
            "created_at": datetime.utcnow().isoformat()
        }
        
        # Generate activities for the lesson
        activities = self._generate_lesson_activities(agent_subject, topic, grade_level, difficulty)
        lesson["activities"] = activities
        
        # Generate resources for the lesson
        resources = self.integrator.suggest_resources(
            subject=agent_subject,
            topic=topic,
            learning_style=None,
            difficulty=difficulty
        )
        lesson["resources"] = resources
        
        return lesson
    
    def _generate_lesson_activities(self, 
                                  subject: str, 
                                  topic: str, 
                                  grade_level: int, 
                                  difficulty: str) -> List[Dict[str, Any]]:
        """
        Generate activities for a lesson.
        
        Args:
            subject: The subject name
            topic: The specific topic
            grade_level: The target grade level
            difficulty: The difficulty level
            
        Returns:
            List of activity dictionaries
        """
        activities = []
        
        # Generate an exercise
        exercise = self.integrator.generate_content(
            subject=subject,
            topic=topic,
            content_type=ContentType.EXERCISE.value,
            difficulty=difficulty,
            grade_level=grade_level
        )
        
        if exercise and "error" not in exercise:
            activities.append({
                "title": exercise.get("title", f"{topic} Exercise"),
                "activity_type": "exercise",
                "instructions": exercise.get("instructions", ""),
                "problems": exercise.get("problems", []),
                "duration_minutes": 15
            })
        
        # Generate a quiz
        quiz = self.integrator.generate_content(
            subject=subject,
            topic=topic,
            content_type=ContentType.QUIZ.value,
            difficulty=difficulty,
            grade_level=grade_level
        )
        
        if quiz and "error" not in quiz:
            activities.append({
                "title": quiz.get("title", f"{topic} Quiz"),
                "activity_type": "quiz",
                "instructions": quiz.get("instructions", ""),
                "questions": quiz.get("questions", []),
                "duration_minutes": 10
            })
        
        # For higher grades, add a project
        if grade_level >= 6:
            project = self.integrator.generate_content(
                subject=subject,
                topic=topic,
                content_type=ContentType.PROJECT.value,
                difficulty=difficulty,
                grade_level=grade_level
            )
            
            if project and "error" not in project:
                activities.append({
                    "title": project.get("title", f"{topic} Project"),
                    "activity_type": "project",
                    "instructions": project.get("description", ""),
                    "tasks": project.get("tasks", []),
                    "duration_minutes": 45
                })
        
        return activities
    
    def save_lesson_to_database(self, lesson_data: Dict[str, Any]) -> Lesson:
        """
        Save a generated lesson to the database.
        
        Args:
            lesson_data: The generated lesson data
            
        Returns:
            The created Lesson object
        """
        # Get or create the subject
        subject = Subject.query.filter_by(
            name=lesson_data["subject"],
            grade_level=lesson_data["grade_level"]
        ).first()
        
        if not subject:
            subject = Subject(
                name=lesson_data["subject"],
                description=f"{lesson_data['subject']} for Grade {lesson_data['grade_level']}",
                grade_level=lesson_data["grade_level"]
            )
            db.session.add(subject)
            db.session.flush()
        
        # Get or create the topic
        topic = Topic.query.filter_by(
            name=lesson_data["topic"],
            subject_id=subject.id,
            grade_level=lesson_data["grade_level"]
        ).first()
        
        if not topic:
            topic = Topic(
                name=lesson_data["topic"],
                description=f"Topic in {lesson_data['subject']} for Grade {lesson_data['grade_level']}",
                subject_id=subject.id,
                grade_level=lesson_data["grade_level"]
            )
            db.session.add(topic)
            db.session.flush()
        
        # Create the lesson
        lesson = Lesson(
            title=lesson_data["title"],
            content=lesson_data.get("introduction", "") + "\n\n" + lesson_data.get("summary", ""),
            subject_id=subject.id,
            topic_id=topic.id,
            grade_level=lesson_data["grade_level"],
            difficulty=lesson_data["difficulty"],
            duration_minutes=60,  # Default duration
            learning_objectives=json.dumps(lesson_data.get("learning_objectives", [])),
            is_generated=True,
            generator_agent=lesson_data.get("generator_agent", ""),
            entrepreneurship_connection=json.dumps(lesson_data.get("entrepreneurship_connection", {}))
        )
        db.session.add(lesson)
        db.session.flush()
        
        # Add sections
        for i, section_data in enumerate(lesson_data.get("sections", [])):
            section = LessonSection(
                lesson_id=lesson.id,
                title=section_data.get("title", f"Section {i+1}"),
                content=section_data.get("content", ""),
                order=i
            )
            db.session.add(section)
        
        # Add activities
        for activity_data in lesson_data.get("activities", []):
            activity = LessonActivity(
                lesson_id=lesson.id,
                title=activity_data.get("title", "Activity"),
                activity_type=activity_data.get("activity_type", "exercise"),
                instructions=activity_data.get("instructions", ""),
                content=json.dumps(activity_data),
                duration_minutes=activity_data.get("duration_minutes", 15)
            )
            db.session.add(activity)
        
        # Add resources
        for resource_data in lesson_data.get("resources", []):
            resource = LessonResource(
                lesson_id=lesson.id,
                title=resource_data.get("title", "Resource"),
                resource_type=resource_data.get("type", "link"),
                url=resource_data.get("url", ""),
                content=json.dumps(resource_data),
                is_generated=True
            )
            db.session.add(resource)
        
        db.session.commit()
        return lesson
    
    def generate_and_save_curriculum(self, 
                                   subject_name: str, 
                                   grade_levels: List[int]) -> Dict[str, Any]:
        """
        Generate and save a complete curriculum for a subject across multiple grade levels.
        
        Args:
            subject_name: The name of the subject
            grade_levels: List of grade levels to generate curriculum for
            
        Returns:
            Dictionary containing the results of the curriculum generation
        """
        results = {
            "subject": subject_name,
            "grade_levels": {},
            "total_lessons": 0
        }
        
        # Generate curriculum structure
        curriculum = self.generate_subject_curriculum(subject_name, grade_levels)
        
        # For each grade level, generate lessons for each topic
        for grade, grade_data in curriculum.get("grade_levels", {}).items():
            topics = grade_data.get("topics", [])
            
            grade_results = {
                "topics": [],
                "lessons_generated": 0
            }
            
            for topic in topics:
                try:
                    # Generate and save lesson
                    lesson_data = self.generate_lesson(
                        subject_name=subject_name,
                        topic=topic,
                        grade_level=grade,
                        difficulty="intermediate"
                    )
                    
                    lesson = self.save_lesson_to_database(lesson_data)
                    
                    # Record results
                    grade_results["topics"].append({
                        "name": topic,
                        "lesson_id": lesson.id,
                        "lesson_title": lesson.title
                    })
                    
                    grade_results["lessons_generated"] += 1
                    results["total_lessons"] += 1
                    
                except Exception as e:
                    print(f"Error generating lesson for {subject_name}, {topic}, Grade {grade}: {str(e)}")
            
            results["grade_levels"][grade] = grade_results
        
        return results


# Create a singleton instance
lesson_generator = LessonContentGenerator()
