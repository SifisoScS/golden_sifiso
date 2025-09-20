"""
Test script for specialized agents in The Golden Hand Learning Platform.

This script tests the functionality of the specialized agents system,
including agent registration, content generation, learning path creation,
and integration with the main application.
"""

import sys
import os
import json
from datetime import datetime

# Add the project root to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, project_root)

# Direct imports from the src package
from src.specialized_agents.base_agent import BaseAgent, ContentType, LearningLevel
from src.specialized_agents.agent_registry import registry
from src.specialized_agents.agent_factory import AgentFactory
from src.specialized_agents.agent_integrator import integrator
from src.specialized_agents.mathematics_navigator.math_agent import MathematicsAgent
from src.specialized_agents.science_illuminator.science_agent import ScienceAgent
from src.specialized_agents.technology_architect.tech_agent import TechnologyAgent


def test_agent_registration():
    """Test agent registration functionality."""
    print("\n=== Testing Agent Registration ===")
    
    # Clear existing registrations
    for agent_id in registry.list_registered_agents():
        registry.unregister_agent(agent_id)
    
    # Register agents
    print("Registering Mathematics Agent...")
    result = registry.register_agent("math_agent", MathematicsAgent)
    print(f"Registration result: {result}")
    
    print("Registering Science Agent...")
    result = registry.register_agent("science_agent", ScienceAgent)
    print(f"Registration result: {result}")
    
    print("Registering Technology Agent...")
    result = registry.register_agent("tech_agent", TechnologyAgent)
    print(f"Registration result: {result}")
    
    # List registered agents
    agents = registry.list_registered_agents()
    print(f"Registered agents: {agents}")
    
    # Try to register duplicate
    print("Attempting to register duplicate agent...")
    result = registry.register_agent("math_agent", MathematicsAgent)
    print(f"Duplicate registration result (should be False): {result}")
    
    # Get agent class
    agent_class = registry.get_agent_class("math_agent")
    print(f"Retrieved agent class: {agent_class.__name__ if agent_class else None}")
    
    return len(agents) == 3


def test_agent_factory():
    """Test agent factory functionality."""
    print("\n=== Testing Agent Factory ===")
    
    # Create agent using factory
    print("Creating Mathematics Agent...")
    math_agent = AgentFactory.create_agent("math_agent")
    print(f"Agent created: {math_agent.name if math_agent else None}")
    
    # Create agent by subject
    print("Creating agent by subject (science)...")
    science_agent = AgentFactory.create_subject_agent("science")
    print(f"Agent created: {science_agent.name if science_agent else None}")
    
    # Test subject mapping with alternative names
    print("Testing subject mapping with alternative names...")
    tech_agent1 = AgentFactory.create_subject_agent("technology")
    tech_agent2 = AgentFactory.create_subject_agent("coding")
    tech_agent3 = AgentFactory.create_subject_agent("computer science")
    
    print(f"'technology' maps to: {tech_agent1.name if tech_agent1 else None}")
    print(f"'coding' maps to: {tech_agent2.name if tech_agent2 else None}")
    print(f"'computer science' maps to: {tech_agent3.name if tech_agent3 else None}")
    
    # Create all agents
    print("Creating all agents...")
    all_agents = AgentFactory.create_all_agents()
    print(f"Number of agents created: {len(all_agents)}")
    
    return math_agent is not None and science_agent is not None and len(all_agents) == 3


def test_learning_path_generation():
    """Test learning path generation functionality."""
    print("\n=== Testing Learning Path Generation ===")
    
    # Initialize the integrator
    integrator.initialize()
    
    # Generate a learning path for mathematics
    print("Generating mathematics learning path...")
    math_path = integrator.generate_learning_path(
        student_id=1,
        grade_level=10,
        subjects=["mathematics"],
        prior_knowledge={"mathematics": {"Algebra": 0.8, "Geometry": 0.4}}
    )
    
    print(f"Mathematics path generated with {len(math_path.get('activities', []))} activities")
    
    # Generate a multi-subject learning path
    print("Generating multi-subject learning path...")
    multi_path = integrator.generate_learning_path(
        student_id=1,
        grade_level=10,
        subjects=["mathematics", "science", "technology"],
        prior_knowledge={
            "mathematics": {"Algebra": 0.8, "Geometry": 0.4},
            "science": {"Chemistry": 0.6},
            "technology": {"Programming": 0.7}
        }
    )
    
    print(f"Multi-subject path generated with {len(multi_path.get('activities', []))} activities")
    print(f"Estimated duration: {multi_path.get('estimated_duration_days', 0)} days")
    
    # Check for interdisciplinary activities
    interdisciplinary = [a for a in multi_path.get('activities', []) 
                        if a.get('content_type') == 'interdisciplinary_project']
    print(f"Interdisciplinary activities: {len(interdisciplinary)}")
    
    # Save example learning path to file for inspection
    output_dir = os.path.join(project_root, "test_output")
    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, 'example_learning_path.json'), 'w') as f:
        json.dump(multi_path, f, indent=2)
    print(f"Example learning path saved to '{output_dir}/example_learning_path.json'")
    
    return len(math_path.get('activities', [])) > 0 and len(multi_path.get('activities', [])) > 0


def test_content_generation():
    """Test content generation functionality."""
    print("\n=== Testing Content Generation ===")
    
    # Initialize the integrator
    integrator.initialize()
    
    # Generate different types of content
    content_types = [
        ("mathematics", "Algebra", ContentType.LESSON.value, LearningLevel.INTERMEDIATE.value, 10),
        ("science", "Chemistry", ContentType.EXERCISE.value, LearningLevel.BEGINNER.value, 9),
        ("technology", "Programming", ContentType.PROJECT.value, LearningLevel.ADVANCED.value, 11),
        ("mathematics", "Statistics", "quiz", "intermediate", 10),
        ("science", "Biology", "laboratory", "intermediate", 10),
        ("technology", "Web Development", "coding_practice", "beginner", 10),
        ("technology", "App Development", "startup_simulation", "intermediate", 11)
    ]
    
    success = True
    output_dir = os.path.join(project_root, "test_output")
    os.makedirs(output_dir, exist_ok=True)
    
    for subject, topic, content_type, difficulty, grade_level in content_types:
        print(f"\nGenerating {content_type} content for {subject}: {topic}...")
        content = integrator.generate_content(subject, topic, content_type, difficulty, grade_level)
        
        if "error" in content:
            print(f"Error: {content['error']}")
            success = False
            continue
        
        print(f"Content generated: {content.get('title')}")
        print(f"Content type: {content.get('content_type')}")
        print(f"Sections/items: {len(content.get('sections', content.get('problems', content.get('questions', []))))}")
        
        # For the first item, save to file for inspection
        if subject == "mathematics" and content_type == ContentType.LESSON.value:
            with open(os.path.join(output_dir, 'example_lesson_content.json'), 'w') as f:
                json.dump(content, f, indent=2)
            print(f"Example lesson content saved to '{output_dir}/example_lesson_content.json'")
    
    return success


def test_performance_analysis():
    """Test performance analysis functionality."""
    print("\n=== Testing Performance Analysis ===")
    
    # Initialize the integrator
    integrator.initialize()
    
    # Create sample activity results
    quiz_results = {
        "activity_type": "quiz",
        "topic": "Algebra",
        "score": 8,
        "max_score": 10,
        "answers": [
            {"question_id": 1, "correct": True, "category": "equations"},
            {"question_id": 2, "correct": True, "category": "equations"},
            {"question_id": 3, "correct": False, "category": "inequalities"},
            {"question_id": 4, "correct": True, "category": "functions"},
            {"question_id": 5, "correct": True, "category": "functions"},
            {"question_id": 6, "correct": True, "category": "functions"},
            {"question_id": 7, "correct": True, "category": "graphing"},
            {"question_id": 8, "correct": True, "category": "graphing"},
            {"question_id": 9, "correct": False, "category": "inequalities"},
            {"question_id": 10, "correct": True, "category": "equations"}
        ]
    }
    
    coding_results = {
        "activity_type": "coding_practice",
        "topic": "Python Programming",
        "score": 85,
        "max_score": 100,
        "tasks_completed": 4,
        "total_tasks": 5,
        "time_spent_minutes": 45
    }
    
    laboratory_results = {
        "activity_type": "laboratory",
        "topic": "Chemical Reactions",
        "score": 18,
        "max_score": 20,
        "observations_recorded": True,
        "safety_procedures_followed": True,
        "experiment_completed": True
    }
    
    # Test analysis for different subjects
    print("\nAnalyzing mathematics quiz performance...")
    math_analysis = integrator.analyze_performance(1, "mathematics", quiz_results)
    print(f"Performance level: {math_analysis.get('performance_level')}")
    print(f"Strengths: {math_analysis.get('strengths')}")
    print(f"Weaknesses: {math_analysis.get('weaknesses')}")
    print(f"Recommended resources: {len(math_analysis.get('recommended_resources', []))}")
    
    print("\nAnalyzing technology coding performance...")
    tech_analysis = integrator.analyze_performance(1, "technology", coding_results)
    print(f"Performance level: {tech_analysis.get('performance_level')}")
    if "coding_skills" in tech_analysis:
        print(f"Coding skills assessment: {tech_analysis['coding_skills']['overall']}/5")
    print(f"Entrepreneurship connection: {tech_analysis.get('entrepreneurship_connection', {}).get('topic')}")
    
    print("\nAnalyzing science laboratory performance...")
    science_analysis = integrator.analyze_performance(1, "science", laboratory_results)
    print(f"Performance level: {science_analysis.get('performance_level')}")
    if "scientific_thinking" in science_analysis:
        print(f"Scientific thinking assessment: {science_analysis['scientific_thinking']['overall']}/5")
    
    # Save example analysis to file for inspection
    output_dir = os.path.join(project_root, "test_output")
    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, 'example_performance_analysis.json'), 'w') as f:
        json.dump(tech_analysis, f, indent=2)
    print(f"Example performance analysis saved to '{output_dir}/example_performance_analysis.json'")
    
    return "performance_level" in math_analysis and "performance_level" in tech_analysis and "performance_level" in science_analysis


def test_question_answering():
    """Test question answering functionality."""
    print("\n=== Testing Question Answering ===")
    
    # Initialize the integrator
    integrator.initialize()
    
    # Test questions with specified subjects
    questions_with_subjects = [
        ("How do I solve a quadratic equation?", "mathematics"),
        ("What is the scientific method?", "science"),
        ("How do I create a website?", "technology")
    ]
    
    for question, subject in questions_with_subjects:
        print(f"\nQuestion: {question}")
        print(f"Subject: {subject}")
        
        answer = integrator.answer_question(question, subject)
        print(f"Answer: {answer.get('answer')[:100]}...")
        print(f"Confidence: {answer.get('confidence')}")
    
    # Test questions without specified subject
    questions_without_subject = [
        "What is the relationship between mathematics and entrepreneurship?",
        "How can I use science to start a business?",
        "What programming languages should I learn first?"
    ]
    
    for question in questions_without_subject:
        print(f"\nQuestion: {question}")
        print(f"Subject: Not specified")
        
        answer = integrator.answer_question(question)
        print(f"Answer: {answer.get('answer')[:100]}...")
        print(f"Confidence: {answer.get('confidence')}")
        print(f"Detected agent: {answer.get('agent')}")
    
    # Save example answer to file for inspection
    output_dir = os.path.join(project_root, "test_output")
    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, 'example_question_answer.json'), 'w') as f:
        json.dump(integrator.answer_question(
            "How can I use technology skills to start a business?",
            context={"grade_level": 11}
        ), f, indent=2)
    print(f"Example question answer saved to '{output_dir}/example_question_answer.json'")
    
    return True


def test_resource_suggestions():
    """Test resource suggestion functionality."""
    print("\n=== Testing Resource Suggestions ===")
    
    # Initialize the integrator
    integrator.initialize()
    
    # Test resource suggestions for different subjects and learning styles
    test_cases = [
        ("mathematics", "Algebra", None, None),
        ("science", "Chemistry", "visual", "beginner"),
        ("technology", "Web Development", "kinesthetic", "advanced")
    ]
    
    for subject, topic, learning_style, difficulty in test_cases:
        print(f"\nGetting resources for {subject}: {topic}")
        if learning_style:
            print(f"Learning style: {learning_style}")
        if difficulty:
            print(f"Difficulty: {difficulty}")
        
        resources = integrator.suggest_resources(subject, topic, learning_style, difficulty)
        print(f"Number of resources: {len(resources)}")
        
        if resources:
            print("Resource examples:")
            for i, resource in enumerate(resources[:3]):
                print(f"  {i+1}. {resource.get('title')} - {resource.get('description')[:50]}...")
    
    # Save example resources to file for inspection
    output_dir = os.path.join(project_root, "test_output")
    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, 'example_resources.json'), 'w') as f:
        json.dump(integrator.suggest_resources("technology", "Programming", "visual", "intermediate"), f, indent=2)
    print(f"Example resources saved to '{output_dir}/example_resources.json'")
    
    return True


def test_entrepreneurship_connections():
    """Test entrepreneurship connection functionality."""
    print("\n=== Testing Entrepreneurship Connections ===")
    
    # Initialize the integrator
    integrator.initialize()
    
    # Test entrepreneurship connections for different subjects and grade levels
    test_cases = [
        ("mathematics", "Algebra", 10),
        ("science", "Chemistry", 11),
        ("technology", "Web Development", 12),
        ("mathematics", "Statistics", 9),
        ("science", "Environmental Science", 10),
        ("technology", "Mobile App Development", 11)
    ]
    
    for subject, topic, grade_level in test_cases:
        print(f"\nGetting entrepreneurship connection for {subject}: {topic} (Grade {grade_level})")
        
        connection = integrator.get_entrepreneurship_connection(subject, topic, grade_level)
        print(f"Description: {connection.get('description')[:100]}...")
        
        if "business_applications" in connection:
            print(f"Business applications: {len(connection['business_applications'])}")
            print(f"Example: {connection['business_applications'][0]}")
        
        if "startup_ideas" in connection:
            print(f"Startup ideas: {len(connection['startup_ideas'])}")
            print(f"Example: {connection['startup_ideas'][0]}")
    
    # Save example connection to file for inspection
    output_dir = os.path.join(project_root, "test_output")
    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, 'example_entrepreneurship_connection.json'), 'w') as f:
        json.dump(integrator.get_entrepreneurship_connection("technology", "Programming", 12), f, indent=2)
    print(f"Example entrepreneurship connection saved to '{output_dir}/example_entrepreneurship_connection.json'")
    
    return True


def run_all_tests():
    """Run all tests and report results."""
    print("=== Running All Tests ===")
    print(f"Date and time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Create test output directory
    output_dir = os.path.join(project_root, "test_output")
    os.makedirs(output_dir, exist_ok=True)
    print(f"Test output will be saved to: {output_dir}")
    
    tests = [
        ("Agent Registration", test_agent_registration),
        ("Agent Factory", test_agent_factory),
        ("Learning Path Generation", test_learning_path_generation),
        ("Content Generation", test_content_generation),
        ("Performance Analysis", test_performance_analysis),
        ("Question Answering", test_question_answering),
        ("Resource Suggestions", test_resource_suggestions),
        ("Entrepreneurship Connections", test_entrepreneurship_connections)
    ]
    
    results = {}
    all_passed = True
    
    for name, test_func in tests:
        print(f"\n\n{'=' * 50}")
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
    
    # Save test results to file
    with open(os.path.join(output_dir, 'test_results.txt'), 'w') as f:
        f.write(f"Test Results - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        for name, result in results.items():
            f.write(f"{name}: {result}\n")
        f.write(f"\nOverall result: {'PASSED' if all_passed else 'FAILED'}\n")
    
    print(f"Test results saved to '{output_dir}/test_results.txt'")
    
    return all_passed


if __name__ == "__main__":
    run_all_tests()
