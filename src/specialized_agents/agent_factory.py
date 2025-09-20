"""
Agent Factory for The Golden Hand Learning Platform.

This module provides a factory for creating and configuring specialized learning agents,
abstracting the instantiation process and providing a consistent interface.
"""

from typing import Dict, Any, Type, Optional
from src.specialized_agents.base_agent import BaseAgent
from src.specialized_agents.agent_registry import registry


class AgentFactory:
    """
    Factory for creating specialized learning agents.
    
    This class provides methods for creating and configuring agent instances,
    abstracting the instantiation details and ensuring proper initialization.
    """
    
    @staticmethod
    def create_agent(agent_id: str, **kwargs) -> Optional[BaseAgent]:
        """
        Create an instance of a registered agent.
        
        Args:
            agent_id: Unique identifier for the agent type to create
            **kwargs: Configuration parameters for the agent
            
        Returns:
            Configured agent instance or None if agent_id is not registered
        """
        # Get the agent instance from the registry
        agent = registry.get_agent_instance(agent_id, **kwargs)
        
        if agent is not None:
            # Initialize the agent
            agent.initialize()
        
        return agent
    
    @staticmethod
    def create_subject_agent(subject: str, **kwargs) -> Optional[BaseAgent]:
        """
        Create an agent based on academic subject.
        
        This is a convenience method that maps common subject names to
        the appropriate agent types.
        
        Args:
            subject: Academic subject (e.g., "mathematics", "science", "technology")
            **kwargs: Configuration parameters for the agent
            
        Returns:
            Configured agent instance or None if subject is not supported
        """
        # Map subjects to agent IDs
        subject_map = {
            "mathematics": "math_agent",
            "math": "math_agent",
            "algebra": "math_agent",
            "calculus": "math_agent",
            "geometry": "math_agent",
            
            "science": "science_agent",
            "biology": "science_agent",
            "chemistry": "science_agent",
            "physics": "science_agent",
            
            "technology": "tech_agent",
            "computer science": "tech_agent",
            "programming": "tech_agent",
            "coding": "tech_agent",
            "web development": "tech_agent",
            "app development": "tech_agent"
        }
        
        # Normalize subject to lowercase
        subject_lower = subject.lower()
        
        # Get the agent ID for this subject
        agent_id = subject_map.get(subject_lower)
        if agent_id is None:
            return None
        
        # Create the agent
        return AgentFactory.create_agent(agent_id, **kwargs)
    
    @staticmethod
    def create_all_agents(**kwargs) -> Dict[str, BaseAgent]:
        """
        Create instances of all registered agents.
        
        Args:
            **kwargs: Configuration parameters for the agents
            
        Returns:
            Dictionary mapping agent IDs to configured instances
        """
        agents = {}
        
        for agent_id in registry.list_registered_agents():
            agent = AgentFactory.create_agent(agent_id, **kwargs)
            if agent is not None:
                agents[agent_id] = agent
        
        return agents
