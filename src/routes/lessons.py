"""
Lessons Platform Blueprint for The Golden Hand Learning Platform.

This module implements the routes and views for the Lessons Platform,
providing access to dynamically generated, curriculum-aligned content
for grades 4-9.
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from src.models.lesson import Lesson, Subject, Topic, LessonSection, LessonActivity, LessonResource
from src.lessons.generator import lesson_generator
import json

lessons_bp = Blueprint('lessons', __name__)

@lessons_bp.route('/')
@login_required
def index():
    """Lessons platform home page"""
    # Get available grade levels
    grade_levels = range(4, 10)  # Grades 4-9
    
    # Get available subjects
    subjects = Subject.query.filter(Subject.grade_level.in_(grade_levels)).all()
    
    return render_template('lessons/index.html', 
                          subjects=subjects, 
                          grade_levels=grade_levels)

@lessons_bp.route('/grades')
@login_required
def grades():
    """View lessons by grade level"""
    grade = request.args.get('grade', type=int)
    
    if not grade or grade < 4 or grade > 9:
        # Default to grade 4 if invalid
        grade = 4
    
    # Get subjects for this grade
    subjects = Subject.query.filter_by(grade_level=grade).all()
    
    # If no subjects exist for this grade, generate them
    if not subjects:
        flash(f"Generating curriculum for Grade {grade}. This may take a moment...", "info")
        # Generate basic subjects for this grade
        for subject_name in ["Mathematics", "Science", "Technology"]:
            subject = Subject(
                name=subject_name,
                description=f"{subject_name} for Grade {grade}",
                grade_level=grade
            )
            db.session.add(subject)
        db.session.commit()
        subjects = Subject.query.filter_by(grade_level=grade).all()
    
    return render_template('lessons/grades.html', 
                          subjects=subjects, 
                          selected_grade=grade,
                          grade_levels=range(4, 10))

@lessons_bp.route('/subject/<int:subject_id>')
@login_required
def subject(subject_id):
    """Subject page with list of topics and lessons"""
    subject = Subject.query.get_or_404(subject_id)
    
    # Get topics for this subject
    topics = Topic.query.filter_by(subject_id=subject_id).all()
    
    # If no topics exist, generate them
    if not topics:
        flash(f"Generating topics for {subject.name} Grade {subject.grade_level}. This may take a moment...", "info")
        # Use the generator to create topics
        curriculum = lesson_generator.generate_subject_curriculum(
            subject_name=subject.name,
            grade_levels=[subject.grade_level]
        )
        
        # Save topics to database
        for topic_name in curriculum["grade_levels"].get(subject.grade_level, {}).get("topics", []):
            topic = Topic(
                name=topic_name,
                description=f"Topic in {subject.name} for Grade {subject.grade_level}",
                subject_id=subject.id,
                grade_level=subject.grade_level
            )
            db.session.add(topic)
        db.session.commit()
        
        # Reload topics
        topics = Topic.query.filter_by(subject_id=subject_id).all()
    
    # Get lessons for each topic
    topic_lessons = {}
    for topic in topics:
        lessons = Lesson.query.filter_by(topic_id=topic.id).all()
        topic_lessons[topic.id] = lessons
    
    return render_template('lessons/subject.html', 
                          subject=subject, 
                          topics=topics,
                          topic_lessons=topic_lessons)

@lessons_bp.route('/topic/<int:topic_id>')
@login_required
def topic(topic_id):
    """Topic page with list of lessons"""
    topic = Topic.query.get_or_404(topic_id)
    subject = Subject.query.get_or_404(topic.subject_id)
    
    # Get lessons for this topic
    lessons = Lesson.query.filter_by(topic_id=topic_id).all()
    
    # If no lessons exist, generate one
    if not lessons:
        flash(f"Generating lesson for {topic.name}. This may take a moment...", "info")
        # Generate a lesson for this topic
        lesson_data = lesson_generator.generate_lesson(
            subject_name=subject.name,
            topic=topic.name,
            grade_level=subject.grade_level,
            difficulty="intermediate"
        )
        
        # Save to database
        lesson_generator.save_lesson_to_database(lesson_data)
        
        # Reload lessons
        lessons = Lesson.query.filter_by(topic_id=topic_id).all()
    
    return render_template('lessons/topic.html', 
                          topic=topic, 
                          subject=subject,
                          lessons=lessons)

@lessons_bp.route('/lesson/<int:lesson_id>')
@login_required
def lesson(lesson_id):
    """Individual lesson page"""
    lesson = Lesson.query.get_or_404(lesson_id)
    subject = Subject.query.get_or_404(lesson.subject_id)
    topic = Topic.query.get(lesson.topic_id) if lesson.topic_id else None
    
    # Get sections, activities, and resources
    sections = LessonSection.query.filter_by(lesson_id=lesson_id).order_by(LessonSection.order).all()
    activities = LessonActivity.query.filter_by(lesson_id=lesson_id).all()
    resources = LessonResource.query.filter_by(lesson_id=lesson_id).all()
    
    # Parse JSON fields
    try:
        learning_objectives = json.loads(lesson.learning_objectives) if lesson.learning_objectives else []
    except:
        learning_objectives = []
        
    try:
        entrepreneurship_connection = json.loads(lesson.entrepreneurship_connection) if lesson.entrepreneurship_connection else {}
    except:
        entrepreneurship_connection = {}
    
    # Format activities for display
    formatted_activities = []
    for activity in activities:
        try:
            activity_data = json.loads(activity.content) if activity.content else {}
            formatted_activities.append({
                'id': activity.id,
                'title': activity.title,
                'type': activity.activity_type,
                'instructions': activity.instructions,
                'data': activity_data
            })
        except:
            formatted_activities.append({
                'id': activity.id,
                'title': activity.title,
                'type': activity.activity_type,
                'instructions': activity.instructions,
                'data': {}
            })
    
    # Format resources for display
    formatted_resources = []
    for resource in resources:
        try:
            resource_data = json.loads(resource.content) if resource.content else {}
            formatted_resources.append({
                'id': resource.id,
                'title': resource.title,
                'type': resource.resource_type,
                'url': resource.url,
                'data': resource_data
            })
        except:
            formatted_resources.append({
                'id': resource.id,
                'title': resource.title,
                'type': resource.resource_type,
                'url': resource.url,
                'data': {}
            })
    
    return render_template('lessons/lesson.html', 
                          lesson=lesson,
                          subject=subject,
                          topic=topic,
                          sections=sections,
                          activities=formatted_activities,
                          resources=formatted_resources,
                          learning_objectives=learning_objectives,
                          entrepreneurship_connection=entrepreneurship_connection)

@lessons_bp.route('/generate/curriculum', methods=['POST'])
@login_required
def generate_curriculum():
    """Generate curriculum for a subject across multiple grade levels"""
    subject_name = request.form.get('subject')
    grade_levels = request.form.getlist('grades', type=int)
    
    if not subject_name or not grade_levels:
        flash("Subject name and grade levels are required", "error")
        return redirect(url_for('lessons.index'))
    
    # Filter grade levels to ensure they're in range 4-9
    grade_levels = [g for g in grade_levels if 4 <= g <= 9]
    
    if not grade_levels:
        flash("Please select valid grade levels (4-9)", "error")
        return redirect(url_for('lessons.index'))
    
    # Generate curriculum
    results = lesson_generator.generate_and_save_curriculum(
        subject_name=subject_name,
        grade_levels=grade_levels
    )
    
    flash(f"Successfully generated {results['total_lessons']} lessons for {subject_name}", "success")
    return redirect(url_for('lessons.index'))

@lessons_bp.route('/generate/lesson', methods=['POST'])
@login_required
def generate_lesson():
    """Generate a lesson for a specific topic"""
    subject_name = request.form.get('subject')
    topic_name = request.form.get('topic')
    grade_level = request.form.get('grade', type=int)
    difficulty = request.form.get('difficulty', 'intermediate')
    
    if not subject_name or not topic_name or not grade_level:
        flash("Subject, topic, and grade level are required", "error")
        return redirect(url_for('lessons.index'))
    
    if grade_level < 4 or grade_level > 9:
        flash("Grade level must be between 4 and 9", "error")
        return redirect(url_for('lessons.index'))
    
    # Generate lesson
    lesson_data = lesson_generator.generate_lesson(
        subject_name=subject_name,
        topic=topic_name,
        grade_level=grade_level,
        difficulty=difficulty
    )
    
    # Save to database
    lesson = lesson_generator.save_lesson_to_database(lesson_data)
    
    flash(f"Successfully generated lesson: {lesson.title}", "success")
    return redirect(url_for('lessons.lesson', lesson_id=lesson.id))

@lessons_bp.route('/api/subjects')
@login_required
def api_subjects():
    """API endpoint to get subjects by grade level"""
    grade = request.args.get('grade', type=int)
    
    if not grade or grade < 4 or grade > 9:
        return jsonify({'error': 'Invalid grade level'}), 400
    
    subjects = Subject.query.filter_by(grade_level=grade).all()
    subject_list = [{'id': s.id, 'name': s.name, 'description': s.description} for s in subjects]
    
    return jsonify({'subjects': subject_list})

@lessons_bp.route('/api/topics')
@login_required
def api_topics():
    """API endpoint to get topics by subject"""
    subject_id = request.args.get('subject_id', type=int)
    
    if not subject_id:
        return jsonify({'error': 'Subject ID is required'}), 400
    
    topics = Topic.query.filter_by(subject_id=subject_id).all()
    topic_list = [{'id': t.id, 'name': t.name, 'description': t.description} for t in topics]
    
    return jsonify({'topics': topic_list})

@lessons_bp.route('/api/lessons')
@login_required
def api_lessons():
    """API endpoint to get lessons by topic"""
    topic_id = request.args.get('topic_id', type=int)
    
    if not topic_id:
        return jsonify({'error': 'Topic ID is required'}), 400
    
    lessons = Lesson.query.filter_by(topic_id=topic_id).all()
    lesson_list = [{'id': l.id, 'title': l.title, 'difficulty': l.difficulty} for l in lessons]
    
    return jsonify({'lessons': lesson_list})
