"""
Script to check subjects and topics in the database.
"""

from src.main import app, db
from src.models.lesson import Subject, Topic
from src.specialized_agents.agent_integrator import integrator
from src.lessons.generator import lesson_generator

def check_subjects_and_topics():
    """Check subjects and topics in the database."""
    print("=== Subjects in Database ===")
    subjects = Subject.query.all()
    for s in subjects:
        print(f"ID: {s.id}, Name: {s.name}, Grade: {s.grade_level}")
        
        # Check topics for this subject
        topics = Topic.query.filter_by(subject_id=s.id).all()
        print(f"  Topics ({len(topics)}):")
        for t in topics:
            print(f"    - {t.name}")
    
    print("\n=== Agent Initialization Status ===")
    print(f"Integrator initialized: {integrator.initialized}")
    if not integrator.initialized:
        print("Initializing integrator...")
        integrator.initialize()
        print(f"Integrator initialized: {integrator.initialized}")
    
    print("\n=== Agent Subject Mapping Test ===")
    for subject_name in ["Mathematics", "Science", "Technology"]:
        agent_subject = lesson_generator._map_subject_to_agent_subject(subject_name)
        agent = integrator.get_agent_for_subject(agent_subject)
        print(f"Subject: {subject_name} -> Agent subject: {agent_subject} -> Agent: {agent.name if agent else 'None'}")
        
        if agent and hasattr(agent, 'topics_by_grade'):
            print(f"  Agent has topics_by_grade: {hasattr(agent, 'topics_by_grade')}")
            for grade in range(4, 10):
                topics = agent.topics_by_grade.get(grade, [])
                print(f"  Grade {grade}: {len(topics)} topics - {', '.join(topics[:3])}...")
        else:
            print("  Agent does not have topics_by_grade attribute")
    
    print("\n=== Testing Topic Generation Logic ===")
    for subject_name in ["Mathematics", "Science", "Technology"]:
        for grade in range(4, 10):
            agent_subject = lesson_generator._map_subject_to_agent_subject(subject_name)
            topics = lesson_generator._generate_topics_for_grade(agent_subject, grade)
            print(f"Subject: {subject_name}, Grade: {grade} -> {len(topics)} topics: {', '.join(topics[:3])}...")
            
            # Check if subject exists in database
            subject = Subject.query.filter_by(name=subject_name, grade_level=grade).first()
            if subject:
                print(f"  Subject exists in DB: ID {subject.id}")
            else:
                print(f"  Subject DOES NOT exist in DB")

if __name__ == "__main__":
    with app.app_context():
        check_subjects_and_topics()
