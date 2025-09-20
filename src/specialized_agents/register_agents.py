"""
Agent Registration Module for The Golden Hand Learning Platform.

This module handles the registration of all specialized agents with the registry.
It must be imported at application startup to ensure all agents are available.
"""

from src.specialized_agents.agent_registry import registry
from src.specialized_agents.mathematics_navigator.math_agent import MathematicsAgent
from src.specialized_agents.science_illuminator.science_agent import ScienceAgent
from src.specialized_agents.technology_architect.tech_agent import TechnologyAgent

def register_all_agents():
    """Register all specialized agents with the registry."""
    # Register the Mathematics Navigator agent
    registry.register_agent("math_agent", MathematicsAgent)
    
    # Register the Science Illuminator agent
    registry.register_agent("science_agent", ScienceAgent)
    
    # Register the Technology Architect agent
    registry.register_agent("tech_agent", TechnologyAgent)
    
    print(f"Registered agents: {registry.list_registered_agents()}")
    return True

# Register all agents when this module is imported
register_all_agents()
