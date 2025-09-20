"""
Agent Registry for The Golden Hand Learning Platform.

This module provides a registry for managing specialized learning agents,
allowing for dynamic registration, retrieval, and management of agents.
"""

from typing import Dict, List, Type, Optional, Any
from src.specialized_agents.base_agent import BaseAgent


class AgentRegistry:
    """
    Registry for managing specialized learning agents.
    
    This class provides a central registry for all subject-specific agents,
    allowing for dynamic registration, retrieval, and management.
    """
    
    def __init__(self):
        """Initialize an empty agent registry."""
        self._agents: Dict[str, Type[BaseAgent]] = {}
        self._instances: Dict[str, BaseAgent] = {}
    
    def register_agent(self, agent_id: str, agent_class: Type[BaseAgent]) -> bool:
        """
        Register a new agent class with the registry.
        
        Args:
            agent_id: Unique identifier for the agent
            agent_class: The agent class to register
            
        Returns:
            bool: True if registration was successful, False if agent_id already exists
        """
        if agent_id in self._agents:
            return False
        
        self._agents[agent_id] = agent_class
        return True
    
    def unregister_agent(self, agent_id: str) -> bool:
        """
        Remove an agent class from the registry.
        
        Args:
            agent_id: Unique identifier for the agent to remove
            
        Returns:
            bool: True if unregistration was successful, False if agent_id doesn't exist
        """
        if agent_id not in self._agents:
            return False
        
        del self._agents[agent_id]
        # Also remove any instances
        if agent_id in self._instances:
            del self._instances[agent_id]
        return True
    
    def get_agent_class(self, agent_id: str) -> Optional[Type[BaseAgent]]:
        """
        Get an agent class by its identifier.
        
        Args:
            agent_id: Unique identifier for the agent
            
        Returns:
            The agent class or None if not found
        """
        return self._agents.get(agent_id)
    
    def get_agent_instance(self, agent_id: str, **kwargs) -> Optional[BaseAgent]:
        """
        Get or create an instance of an agent.
        
        This method implements a singleton pattern for agent instances.
        
        Args:
            agent_id: Unique identifier for the agent
            **kwargs: Arguments to pass to the agent constructor if creating a new instance
            
        Returns:
            An agent instance or None if the agent class is not registered
        """
        # Return existing instance if available
        if agent_id in self._instances:
            return self._instances[agent_id]
        
        # Create new instance if class is registered
        agent_class = self.get_agent_class(agent_id)
        if agent_class is None:
            return None
        
        instance = agent_class(**kwargs)
        self._instances[agent_id] = instance
        return instance
    
    def list_registered_agents(self) -> List[str]:
        """
        Get a list of all registered agent identifiers.
        
        Returns:
            List of agent identifiers
        """
        return list(self._agents.keys())
    
    def get_agent_info(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """
        Get information about a registered agent.
        
        Args:
            agent_id: Unique identifier for the agent
            
        Returns:
            Dictionary with agent information or None if not found
        """
        instance = self.get_agent_instance(agent_id)
        if instance is None:
            return None
        
        return instance.get_agent_info()


# Create a global registry instance
registry = AgentRegistry()
