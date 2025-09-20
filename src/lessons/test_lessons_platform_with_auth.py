"""
Test script for the Lessons Platform with dynamic content generation.

This version includes authentication for UI integration tests.
"""

import sys
import os
import json
from datetime import datetime
from flask_login import login_user

# Add the project root to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, project_root)

# Import after setting up path
from src.main import app, db

# Create an application context for testing
app_context = app.app_context()
app_context.push()

# Import models after app context is established
from src.models import (
    Subject, Topic, Lesson, LessonSection, 
    LessonActivity, LessonResource, LessonProgress, User
)
from src.lessons.generator import lesson_generator
from src.lessons.content_manager import content_manager


def test_subject_generation():
    """Test subject generation for grades 4-9."""
    print("\n=== Testing Subject Generation ===")
    
    results = {}
    for grade in range(4, 10):
        print(f"\nGenerating subjects for Grade {grade}...")
        
        # Generate basic subjects for this grade
        subjects = []
        for subject_name in ["Mathematics", "Science", "Technology"]:
            # Check if subject already exists
            subject = Subject.query.filter_by(name=subject_name, grade_level=grade).first()
            if not subject:
                subject = Subject(
                    name=subject_name,
                    description=f"{subject_name} for Grade {grade}",
                    grade_level=grade
                )
                db.session.add(subject)
                db.session.flush()
                print(f"Created subject: {subject_name} (Grade {grade})")
            else:
                print(f"Subject already exists: {subject_name} (Grade {grade})")
            
            subjects.append(subject)
        
        db.session.commit()
        
        results[grade] = {
            "subjects": [s.name for s in subjects],
            "count": len(subjects)
        }
    
    print("\nSubject generation results:")
    for grade, data in results.items():
        print(f"Grade {grade}: {data['count']} subjects - {', '.join(data['subjects'])}")
    
    return all(data["count"] > 0 for data in results.values())


def test_topic_generation():
    """Test topic generation for subjects across grades 4-9."""
    print("\n=== Testing Topic Generation ===")
    
    results = {}
    for grade in range(4, 10):
        results[grade] = {}
        
        subjects = Subject.query.filter_by(grade_level=grade).all()
        for subject in subjects:
            print(f"\nGenerating topics for {subject.name} (Grade {grade})...")
            
            # Generate curriculum structure
            curriculum = lesson_generator.generate_subject_curriculum(
                subject_name=subject.name,
                grade_levels=[grade]
            )
            
            # Extract topics
            topics = curriculum["grade_levels"].get(grade, {}).get("topics", [])
            
            # Save topics to database
            saved_topics = []
            for topic_name in topics:
                # Check if topic already exists
                topic = Topic.query.filter_by(name=topic_name, subject_id=subject.id).first()
                if not topic:
                    topic = Topic(
                        name=topic_name,
                        description=f"Topic in {subject.name} for Grade {grade}",
                        subject_id=subject.id,
                        grade_level=grade
                    )
                    db.session.add(topic)
                    db.session.flush()
                    print(f"Created topic: {topic_name}")
                else:
                    print(f"Topic already exists: {topic_name}")
                
                saved_topics.append(topic)
            
            db.session.commit()
            
            results[grade][subject.name] = {
                "topics": [t.name for t in saved_topics],
                "count": len(saved_topics)
            }
    
    print("\nTopic generation results:")
    for grade, subjects in results.items():
        print(f"\nGrade {grade}:")
        for subject_name, data in subjects.items():
            print(f"  {subject_name}: {data['count']} topics - {', '.join(data['topics'])}")
    
    return all(
        all(data["count"] > 0 for data in subjects.values())
        for subjects in results.values()
    )


def test_lesson_generation():
    """Test lesson generation for topics across grades 4-9."""
    print("\n=== Testing Lesson Generation ===")
    
    results = {}
    # Test one subject per grade to avoid long test times
    for grade in range(4, 10):
        results[grade] = {}
        
        # Get a subject for this grade
        subject = Subject.query.filter_by(grade_level=grade).first()
        if not subject:
            print(f"No subject found for Grade {grade}, skipping...")
            continue
        
        print(f"\nGenerating lessons for {subject.name} (Grade {grade})...")
        
        # Get topics for this subject
        topics = Topic.query.filter_by(subject_id=subject.id).all()
        if not topics:
            print(f"No topics found for {subject.name} (Grade {grade}), skipping...")
            continue
        
        # Generate a lesson for each topic
        lessons = []
        for topic in topics[:2]:  # Limit to 2 topics per subject for testing
            print(f"Generating lesson for topic: {topic.name}...")
            
            # Generate lesson
            lesson_data = lesson_generator.generate_lesson(
                subject_name=subject.name,
                topic=topic.name,
                grade_level=grade,
                difficulty="intermediate"
            )
            
            # Save to database
            lesson = lesson_generator.save_lesson_to_database(lesson_data)
            print(f"Created lesson: {lesson.title}")
            
            lessons.append(lesson)
        
        results[grade][subject.name] = {
            "lessons": [l.title for l in lessons],
            "count": len(lessons)
        }
    
    print("\nLesson generation results:")
    for grade, subjects in results.items():
        print(f"\nGrade {grade}:")
        for subject_name, data in subjects.items():
            print(f"  {subject_name}: {data['count']} lessons - {', '.join(data['lessons'])}")
    
    return all(
        all(data["count"] > 0 for data in subjects.values())
        for subjects in results.values() if subjects
    )


def test_content_storage_and_retrieval():
    """Test content storage and retrieval functionality."""
    print("\n=== Testing Content Storage and Retrieval ===")
    
    # Get a random lesson
    lesson = Lesson.query.first()
    if not lesson:
        print("No lessons found, skipping test...")
        return False
    
    print(f"Testing content storage and retrieval for lesson: {lesson.title}")
    
    # Cache the lesson
    print("Caching lesson...")
    content_manager.cache_lesson(lesson.id)
    
    # Retrieve from cache
    print("Retrieving from cache...")
    cached_lesson = content_manager.get_cached_lesson(lesson.id)
    
    if not cached_lesson:
        print("Failed to retrieve lesson from cache")
        return False
    
    print(f"Successfully retrieved lesson from cache: {cached_lesson['title']}")
    
    # Get with details
    print("Getting lesson with details...")
    lesson_details = content_manager.get_lesson_with_details(lesson.id)
    
    if not lesson_details:
        print("Failed to get lesson with details")
        return False
    
    print(f"Successfully retrieved lesson with details: {lesson_details['title']}")
    print(f"Number of sections: {len(lesson_details['sections'])}")
    print(f"Number of activities: {len(lesson_details['activities'])}")
    print(f"Number of resources: {len(lesson_details['resources'])}")
    
    # Invalidate cache
    print("Invalidating cache...")
    content_manager.invalidate_cache(lesson.id)
    
    # Verify cache is invalidated
    cached_lesson = content_manager.get_cached_lesson(lesson.id)
    if cached_lesson:
        print("Cache invalidation failed")
        return False
    
    print("Cache successfully invalidated")
    
    return True


def test_curriculum_generation():
    """Test full curriculum generation for a subject across multiple grades."""
    print("\n=== Testing Full Curriculum Generation ===")
    
    # Test with one subject across grades 4-6 (limited for testing time)
    subject_name = "Mathematics"
    grade_levels = [4, 5, 6]
    
    print(f"Generating curriculum for {subject_name} across grades {grade_levels}...")
    
    # Generate curriculum
    results = lesson_generator.generate_and_save_curriculum(
        subject_name=subject_name,
        grade_levels=grade_levels
    )
    
    print(f"Curriculum generation results:")
    print(f"Total lessons generated: {results['total_lessons']}")
    
    for grade, grade_data in results.get("grade_levels", {}).items():
        print(f"\nGrade {grade}:")
        print(f"Lessons generated: {grade_data['lessons_generated']}")
        print(f"Topics: {len(grade_data['topics'])}")
        for topic in grade_data['topics']:
            print(f"  - {topic['name']}: Lesson ID {topic['lesson_id']} - {topic['lesson_title']}")
    
    return results['total_lessons'] > 0


def test_user_interface_integration():
    """Test user interface integration with the Flask application."""
    print("\n=== Testing User Interface Integration ===")
    
    # Create a test client
    client = app.test_client()
    
    # Create a test session context
    with client.session_transaction() as session:
        # Find a test user
        test_user = User.query.filter_by(email='student@goldenhand.com').first()
        if not test_user:
            print("Creating test user...")
            test_user = User(
                username='testuser',
                email='student@goldenhand.com',
                role='student'
            )
            test_user.set_password('student123')
            db.session.add(test_user)
            db.session.commit()
        
        # Log in the test user
        session['user_id'] = test_user.id
        session['_fresh'] = True
    
    # Test routes with authenticated session
    routes = [
        "/lessons/",
        "/lessons/grades?grade=4",
        "/lessons/api/subjects?grade=4"
    ]
    
    results = {}
    for route in routes:
        print(f"Testing route: {route}")
        response = client.get(route)
        status_code = response.status_code
        
        results[route] = {
            "status_code": status_code,
            "success": 200 <= status_code < 300
        }
        
        print(f"Status code: {status_code}")
        if not results[route]["success"]:
            print(f"Route test failed: {route}")
    
    # Test subject API
    print("\nTesting subject API...")
    response = client.get("/lessons/api/subjects?grade=4")
    if response.status_code == 200:
        data = json.loads(response.data)
        subjects = data.get("subjects", [])
        print(f"Retrieved {len(subjects)} subjects for Grade 4")
        for subject in subjects:
            print(f"  - {subject['name']}")
    
    # Test lesson generation API
    print("\nTesting lesson generation API...")
    subject = Subject.query.filter_by(grade_level=4).first()
    if subject:
        topic = Topic.query.filter_by(subject_id=subject.id).first()
        if topic:
            response = client.post("/lessons/generate/lesson", data={
                "subject": subject.name,
                "topic": topic.name,
                "grade": 4,
                "difficulty": "intermediate"
            })
            
            print(f"Lesson generation status code: {response.status_code}")
            results["lesson_generation"] = {
                "status_code": response.status_code,
                "success": 200 <= response.status_code < 400
            }
    
    print("\nUser interface integration results:")
    for route, data in results.items():
        print(f"{route}: {'Success' if data['success'] else 'Failed'} ({data['status_code']})")
    
    return all(data["success"] for data in results.values())


def run_all_tests():
    """Run all tests and report results."""
    print("=== Running All Tests ===")
    print(f"Date and time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    tests = [
        ("Subject Generation", test_subject_generation),
        ("Topic Generation", test_topic_generation),
        ("Lesson Generation", test_lesson_generation),
        ("Content Storage and Retrieval", test_content_storage_and_retrieval),
        ("Curriculum Generation", test_curriculum_generation),
        ("User Interface Integration", test_user_interface_integration)
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
    output_dir = os.path.join(project_root, "test_output")
    os.makedirs(output_dir, exist_ok=True)
    
    with open(os.path.join(output_dir, 'lessons_platform_test_results_with_auth.txt'), 'w') as f:
        f.write(f"Lessons Platform Test Results - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        for name, result in results.items():
            f.write(f"{name}: {result}\n")
        f.write(f"\nOverall result: {'PASSED' if all_passed else 'FAILED'}\n")
    
    print(f"Test results saved to '{output_dir}/lessons_platform_test_results_with_auth.txt'")
    
    # Clean up
    app_context.pop()
    
    return all_passed


if __name__ == "__main__":
    run_all_tests()
