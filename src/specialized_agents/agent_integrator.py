"""
Agent Integrator for The Golden Hand Learning Platform.

This module provides the orchestration layer for specialized learning agents,
coordinating their activities and integrating them with the main application.
"""

from typing import Dict, List, Any, Optional, Tuple
from src.specialized_agents.base_agent import BaseAgent, ContentType, LearningLevel
from src.specialized_agents.agent_registry import registry
from src.specialized_agents.agent_factory import AgentFactory


class AgentIntegrator:
    """
    Orchestration layer for specialized learning agents.
    
    This class coordinates the activities of different subject-specific agents,
    routes requests to the appropriate agent, and manages agent collaboration
    for interdisciplinary topics.
    """
    
    def __init__(self):
        """Initialize the agent integrator."""
        self.agents = {}
        self.initialized = False
    
    def initialize(self) -> bool:
        """
        Initialize the integrator and all registered agents.
        
        Returns:
            bool: True if initialization was successful, False otherwise
        """
        # Create instances of all registered agents
        self.agents = AgentFactory.create_all_agents()
        
        # Check if we have the core agents
        required_agents = ["math_agent", "science_agent", "tech_agent"]
        for agent_id in required_agents:
            if agent_id not in self.agents:
                return False
        
        self.initialized = True
        return True
    
    def get_agent_for_subject(self, subject: str) -> Optional[BaseAgent]:
        """
        Get the appropriate agent for a given subject.
        
        Args:
            subject: The academic subject
            
        Returns:
            The appropriate agent or None if no suitable agent is found
        """
        # Use the factory's subject mapping
        return AgentFactory.create_subject_agent(subject)
    
    def generate_learning_path(self, 
                              student_id: int, 
                              grade_level: int, 
                              subjects: List[str],
                              prior_knowledge: Dict[str, Dict[str, float]] = None) -> Dict[str, Any]:
        """
        Generate a comprehensive learning path across multiple subjects.
        
        Args:
            student_id: The unique identifier for the student
            grade_level: The student's current grade level (1-12)
            subjects: List of subjects to include in the learning path
            prior_knowledge: Dictionary mapping subjects to topics and proficiency levels
            
        Returns:
            A comprehensive learning path with activities from all requested subjects
        """
        if not self.initialized:
            self.initialize()
        
        # Default prior knowledge if none provided
        if prior_knowledge is None:
            prior_knowledge = {}
        
        # Generate learning paths for each subject
        subject_paths = {}
        for subject in subjects:
            agent = self.get_agent_for_subject(subject)
            if agent is None:
                continue
            
            # Get prior knowledge for this subject
            subject_prior_knowledge = prior_knowledge.get(subject, {})
            
            # Generate path for this subject
            path = agent.generate_learning_path(student_id, grade_level, subject_prior_knowledge)
            subject_paths[subject] = path
        
        # Combine and sequence the learning paths
        combined_path = self._sequence_learning_paths(subject_paths, grade_level)
        
        # Add interdisciplinary activities
        if len(subjects) > 1:
            interdisciplinary_activities = self._generate_interdisciplinary_activities(subjects, grade_level)
            combined_path["activities"].extend(interdisciplinary_activities)
        
        return combined_path
    
    def _sequence_learning_paths(self, 
                               subject_paths: Dict[str, List[Dict[str, Any]]], 
                               grade_level: int) -> Dict[str, Any]:
        """
        Sequence learning activities from multiple subjects into a coherent path.
        
        Args:
            subject_paths: Dictionary mapping subjects to their learning paths
            grade_level: The student's grade level
            
        Returns:
            A sequenced learning path with activities from all subjects
        """
        # Initialize the combined path
        combined_path = {
            "grade_level": grade_level,
            "subjects": list(subject_paths.keys()),
            "activities": [],
            "estimated_duration_days": 0
        }
        
        # Simple interleaving of activities from different subjects
        # In a real implementation, this would use more sophisticated sequencing logic
        
        # First, add all lessons grouped by subject
        for subject, path in subject_paths.items():
            lesson_activities = [activity for activity in path if activity.get("content_type") == ContentType.LESSON.value]
            for activity in lesson_activities:
                activity["subject"] = subject
                combined_path["activities"].append(activity)
        
        # Then add exercises and practice activities
        for subject, path in subject_paths.items():
            practice_activities = [activity for activity in path if activity.get("content_type") in 
                                  [ContentType.EXERCISE.value, "laboratory", "coding_practice"]]
            for activity in practice_activities:
                activity["subject"] = subject
                combined_path["activities"].append(activity)
        
        # Then add quizzes
        for subject, path in subject_paths.items():
            quiz_activities = [activity for activity in path if activity.get("content_type") == ContentType.QUIZ.value]
            for activity in quiz_activities:
                activity["subject"] = subject
                combined_path["activities"].append(activity)
        
        # Finally add projects and assessments
        for subject, path in subject_paths.items():
            project_activities = [activity for activity in path if activity.get("content_type") in 
                                 [ContentType.PROJECT.value, ContentType.ASSESSMENT.value, "startup_simulation"]]
            for activity in project_activities:
                activity["subject"] = subject
                combined_path["activities"].append(activity)
        
        # Calculate estimated duration
        total_minutes = sum(activity.get("estimated_time_minutes", 30) for activity in combined_path["activities"])
        # Assuming 2 hours of study per day
        combined_path["estimated_duration_days"] = round(total_minutes / 120)
        
        return combined_path
    
    def _generate_interdisciplinary_activities(self, 
                                             subjects: List[str], 
                                             grade_level: int) -> List[Dict[str, Any]]:
        """
        Generate interdisciplinary activities that span multiple subjects.
        
        Args:
            subjects: List of subjects to combine
            grade_level: The student's grade level
            
        Returns:
            A list of interdisciplinary activities
        """
        activities = []
        
        # Create an interdisciplinary project
        if len(subjects) >= 2:
            project_title = "Interdisciplinary Project: "
            project_description = "Apply concepts from multiple subjects to solve a real-world problem: "
            
            if "mathematics" in subjects and "technology" in subjects:
                project_title += "Data-Driven Solution"
                project_description += "Use mathematical analysis and technology implementation to create a data-driven application."
            elif "science" in subjects and "technology" in subjects:
                project_title += "Scientific Innovation"
                project_description += "Apply scientific principles and technology skills to develop an innovative solution to an environmental or health challenge."
            elif "mathematics" in subjects and "science" in subjects:
                project_title += "Scientific Modeling"
                project_description += "Use mathematical models to analyze and predict scientific phenomena."
            else:
                project_title += "Cross-Domain Innovation"
                project_description += "Combine knowledge from different domains to create an innovative solution to a community challenge."
            
            activities.append({
                "type": "activity",
                "content_type": "interdisciplinary_project",
                "subjects": subjects,
                "difficulty": LearningLevel.INTERMEDIATE.value,
                "title": project_title,
                "description": project_description,
                "estimated_time_minutes": 180
            })
        
        # Add an entrepreneurship activity if appropriate for the grade level
        if grade_level >= 8:
            activities.append({
                "type": "activity",
                "content_type": "entrepreneurship_challenge",
                "subjects": subjects,
                "difficulty": LearningLevel.INTERMEDIATE.value,
                "title": "Entrepreneurship Challenge: From Knowledge to Business",
                "description": "Develop a business idea that leverages your knowledge across multiple subjects to solve a real problem in your community.",
                "estimated_time_minutes": 120
            })
        
        return activities
    
    def generate_content(self, 
                        subject: str, 
                        topic: str, 
                        content_type: str, 
                        difficulty: str, 
                        grade_level: int) -> Dict[str, Any]:
        """
        Generate content for a specific subject and topic.
        
        Args:
            subject: The academic subject
            topic: The specific topic
            content_type: The type of content to generate
            difficulty: The difficulty level
            grade_level: The target grade level
            
        Returns:
            The generated content
        """
        if not self.initialized:
            self.initialize()
        
        # Get the appropriate agent
        agent = self.get_agent_for_subject(subject)
        if agent is None:
            return {"error": f"No agent available for subject: {subject}"}
        
        # Convert string parameters to enums
        try:
            content_type_enum = ContentType(content_type)
        except ValueError:
            # Handle custom content types that aren't in the enum
            content_type_enum = ContentType.LESSON  # Default
        
        try:
            difficulty_enum = LearningLevel(difficulty)
        except ValueError:
            difficulty_enum = LearningLevel.INTERMEDIATE  # Default
        
        # Generate the content
        return agent.generate_content(topic, content_type_enum, difficulty_enum, grade_level)
    
    def analyze_performance(self, 
                           student_id: int, 
                           subject: str, 
                           activity_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze a student's performance in a specific subject.
        
        Args:
            student_id: The unique identifier for the student
            subject: The academic subject
            activity_results: Results from a learning activity
            
        Returns:
            Analysis results with feedback and recommendations
        """
        if not self.initialized:
            self.initialize()
        
        # Get the appropriate agent
        agent = self.get_agent_for_subject(subject)
        if agent is None:
            return {"error": f"No agent available for subject: {subject}"}
        
        # Analyze the performance
        return agent.analyze_performance(student_id, activity_results)
    
    def answer_question(self, 
                       question: str, 
                       subject: str = None, 
                       context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Answer a student's question, routing to the appropriate agent.
        
        Args:
            question: The question text
            subject: The academic subject (if known)
            context: Additional context about the question
            
        Returns:
            The answer with metadata
        """
        if not self.initialized:
            self.initialize()
        
        # Default context
        if context is None:
            context = {}
        
        # If subject is specified, route to that agent
        if subject:
            agent = self.get_agent_for_subject(subject)
            if agent:
                answer, confidence = agent.answer_question(question, context)
                return {
                    "question": question,
                    "answer": answer,
                    "confidence": confidence,
                    "subject": subject,
                    "agent": agent.name
                }
        
        # If subject is not specified or agent not found, try all agents
        results = []
        for agent_id, agent in self.agents.items():
            answer, confidence = agent.answer_question(question, context)
            results.append({
                "agent_id": agent_id,
                "agent_name": agent.name,
                "answer": answer,
                "confidence": confidence
            })
        
        # Select the answer with highest confidence
        best_result = max(results, key=lambda x: x["confidence"])
        
        return {
            "question": question,
            "answer": best_result["answer"],
            "confidence": best_result["confidence"],
            "agent": best_result["agent_name"],
            "all_responses": results
        }
    
    def suggest_resources(self, 
                         subject: str, 
                         topic: str, 
                         learning_style: str = None, 
                         difficulty: str = None) -> List[Dict[str, Any]]:
        """
        Suggest learning resources for a specific subject and topic.
        
        Args:
            subject: The academic subject
            topic: The topic to find resources for
            learning_style: The student's preferred learning style
            difficulty: The preferred difficulty level
            
        Returns:
            A list of resource recommendations
        """
        if not self.initialized:
            self.initialize()
        
        # Get the appropriate agent
        agent = self.get_agent_for_subject(subject)
        if agent is None:
            return []
        
        # Convert difficulty string to enum if provided
        difficulty_enum = None
        if difficulty:
            try:
                difficulty_enum = LearningLevel(difficulty)
            except ValueError:
                difficulty_enum = LearningLevel.INTERMEDIATE  # Default
        
        # Get resource suggestions
        return agent.suggest_resources(topic, learning_style, difficulty_enum)
    
    def get_entrepreneurship_connection(self, 
                                       subject: str, 
                                       topic: str, 
                                       grade_level: int) -> Dict[str, Any]:
        """
        Get entrepreneurship connections for a specific subject and topic.
        
        Args:
            subject: The academic subject
            topic: The academic topic
            grade_level: The student's grade level
            
        Returns:
            Information connecting the topic to business opportunities
        """
        if not self.initialized:
            self.initialize()
        
        # Get the appropriate agent
        agent = self.get_agent_for_subject(subject)
        if agent is None:
            return {
                "error": f"No agent available for subject: {subject}",
                "subject": subject,
                "topic": topic,
                "grade_level": grade_level
            }
        
        # Get entrepreneurship connection
        return agent.get_entrepreneurship_connection(topic, grade_level)
    
    def get_agent_info(self) -> Dict[str, Any]:
        """
        Get information about all available agents.
        
        Returns:
            Dictionary with information about all agents
        """
        if not self.initialized:
            self.initialize()
        
        agent_info = {}
        for agent_id, agent in self.agents.items():
            agent_info[agent_id] = agent.get_agent_info()
        
        return {
            "initialized": self.initialized,
            "agent_count": len(self.agents),
            "agents": agent_info
        }


# Create a global integrator instance
integrator = AgentIntegrator()
