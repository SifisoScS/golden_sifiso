"""
Base Agent Interface for The Golden Hand Learning Platform.

This module defines the abstract base class that all specialized learning agents
must implement. It provides the foundation for subject-specific agents to deliver
personalized learning experiences.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, Tuple
from enum import Enum


class LearningLevel(Enum):
    """Enumeration of learning difficulty levels."""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class ContentType(Enum):
    """Enumeration of content types that agents can generate."""
    LESSON = "lesson"
    EXERCISE = "exercise"
    QUIZ = "quiz"
    PROJECT = "project"
    ASSESSMENT = "assessment"


class BaseAgent(ABC):
    """
    Abstract base class for all specialized learning agents.
    
    All subject-specific agents must inherit from this class and implement
    its abstract methods to provide consistent functionality across the platform.
    """
    
    def __init__(self, name: str, description: str):
        """
        Initialize the base agent with name and description.
        
        Args:
            name: The name of the agent
            description: A brief description of the agent's capabilities
        """
        self.name = name
        self.description = description
        self.initialized = False
    
    def initialize(self) -> bool:
        """
        Initialize the agent with any required resources or data.
        
        Returns:
            bool: True if initialization was successful, False otherwise
        """
        self.initialized = True
        return True
    
    @abstractmethod
    def generate_learning_path(self, 
                              student_id: int, 
                              grade_level: int, 
                              prior_knowledge: Dict[str, float] = None) -> List[Dict[str, Any]]:
        """
        Generate a personalized learning path for a student.
        
        Args:
            student_id: The unique identifier for the student
            grade_level: The student's current grade level (1-12)
            prior_knowledge: Dictionary mapping topics to proficiency levels (0.0-1.0)
            
        Returns:
            A list of learning activities in recommended sequence
        """
        pass
    
    @abstractmethod
    def generate_content(self, 
                        topic: str, 
                        content_type: ContentType, 
                        difficulty: LearningLevel, 
                        grade_level: int) -> Dict[str, Any]:
        """
        Generate subject-specific content for a given topic.
        
        Args:
            topic: The specific topic to generate content for
            content_type: The type of content to generate (lesson, exercise, etc.)
            difficulty: The difficulty level of the content
            grade_level: The target grade level (1-12)
            
        Returns:
            A dictionary containing the generated content
        """
        pass
    
    @abstractmethod
    def analyze_performance(self, 
                           student_id: int, 
                           activity_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze a student's performance and provide feedback.
        
        Args:
            student_id: The unique identifier for the student
            activity_results: Results from a learning activity
            
        Returns:
            Analysis results with feedback and recommendations
        """
        pass
    
    @abstractmethod
    def answer_question(self, 
                       question: str, 
                       context: Dict[str, Any] = None) -> Tuple[str, float]:
        """
        Answer a subject-specific question from a student.
        
        Args:
            question: The question text
            context: Additional context about the question
            
        Returns:
            A tuple containing (answer, confidence_score)
        """
        pass
    
    @abstractmethod
    def suggest_resources(self, 
                         topic: str, 
                         learning_style: str = None, 
                         difficulty: LearningLevel = None) -> List[Dict[str, Any]]:
        """
        Suggest external resources for further learning.
        
        Args:
            topic: The topic to find resources for
            learning_style: The student's preferred learning style
            difficulty: The preferred difficulty level
            
        Returns:
            A list of resource recommendations
        """
        pass
    
    @abstractmethod
    def get_entrepreneurship_connection(self, 
                                       topic: str, 
                                       grade_level: int) -> Dict[str, Any]:
        """
        Connect subject knowledge to entrepreneurship opportunities.
        
        This method specifically supports The Golden Hand's vision of preparing
        students to build startups after grade 12.
        
        Args:
            topic: The academic topic to connect to entrepreneurship
            grade_level: The student's grade level
            
        Returns:
            Information connecting the topic to business opportunities
        """
        pass
    
    def get_agent_info(self) -> Dict[str, Any]:
        """
        Get information about this agent.
        
        Returns:
            A dictionary with agent metadata
        """
        return {
            "name": self.name,
            "description": self.description,
            "initialized": self.initialized,
            "type": self.__class__.__name__
        }
