"""
Test script to verify agent registration and initialization.

This script tests whether the agent registration fix is working properly
and agents are available for topic generation.
"""

import sys
import os

# Add the project root to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Import after setting up path
from src.main import app
from src.specialized_agents.agent_registry import registry
from src.specialized_agents.agent_factory import AgentFactory
from src.specialized_agents.agent_integrator import integrator
from src.specialized_agents import register_agents  # This should trigger registration

def test_agent_registration():
    """Test if agents are properly registered."""
    print("\n=== Testing Agent Registration ===")
    
    # Check registered agents
    registered_agents = registry.list_registered_agents()
    print(f"Registered agents: {registered_agents}")
    
    # Check if required agents are registered
    required_agents = ["math_agent", "science_agent", "tech_agent"]
    all_required_registered = all(agent in registered_agents for agent in required_agents)
    
    print(f"All required agents registered: {all_required_registered}")
    
    return all_required_registered

def test_agent_instantiation():
    """Test if agents can be instantiated."""
    print("\n=== Testing Agent Instantiation ===")
    
    results = {}
    
    # Try to instantiate each agent
    for agent_id in ["math_agent", "science_agent", "tech_agent"]:
        agent = AgentFactory.create_agent(agent_id)
        results[agent_id] = agent is not None
        print(f"Agent {agent_id}: {'Successfully instantiated' if results[agent_id] else 'Failed to instantiate'}")
        
        if agent:
            print(f"  Name: {agent.name}")
            print(f"  Initialized: {agent.initialized}")
            print(f"  Has topics_by_grade: {hasattr(agent, 'topics_by_grade')}")
            if hasattr(agent, 'topics_by_grade'):
                for grade in range(4, 10):
                    topics = agent.topics_by_grade.get(grade, [])
                    print(f"  Grade {grade}: {len(topics)} topics")
    
    all_instantiated = all(results.values())
    print(f"All agents successfully instantiated: {all_instantiated}")
    
    return all_instantiated

def test_integrator_initialization():
    """Test if the agent integrator initializes properly."""
    print("\n=== Testing Agent Integrator ===")
    
    # Check initial state
    print(f"Integrator initialized: {integrator.initialized}")
    
    # Try to initialize
    if not integrator.initialized:
        success = integrator.initialize()
        print(f"Initialization attempt result: {success}")
        print(f"Integrator initialized after attempt: {integrator.initialized}")
    
    # Check if agents are available through the integrator
    subjects = ["mathematics", "science", "technology"]
    results = {}
    
    for subject in subjects:
        agent = integrator.get_agent_for_subject(subject)
        results[subject] = agent is not None
        print(f"Subject {subject}: {'Agent available' if results[subject] else 'No agent available'}")
        
        if agent:
            print(f"  Agent name: {agent.name}")
    
    all_subjects_have_agents = all(results.values())
    print(f"All subjects have agents: {all_subjects_have_agents}")
    
    return integrator.initialized and all_subjects_have_agents

def run_all_tests():
    """Run all agent registration tests."""
    print("=== Running Agent Registration Tests ===")
    
    tests = [
        ("Agent Registration", test_agent_registration),
        ("Agent Instantiation", test_agent_instantiation),
        ("Integrator Initialization", test_integrator_initialization)
    ]
    
    results = {}
    all_passed = True
    
    for name, test_func in tests:
        print(f"\n{'=' * 50}")
        print(f"Running test: {name}")
        print(f"{'=' * 50}")
        
        try:
            result = test_func()
            results[name] = "PASSED" if result else "FAILED"
            if not result:
                all_passed = False
        except Exception as e:
            import traceback
            print(f"Error during test: {str(e)}")
            print(traceback.format_exc())
            results[name] = "ERROR"
            all_passed = False
    
    print("\n\n=== Test Results Summary ===")
    for name, result in results.items():
        print(f"{name}: {result}")
    
    print(f"\nOverall result: {'PASSED' if all_passed else 'FAILED'}")
    
    return all_passed

if __name__ == "__main__":
    with app.app_context():
        run_all_tests()
