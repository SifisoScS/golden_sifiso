from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from src.models.audio import AudioLesson, AudioPlayback

audio_bp = Blueprint('audio', __name__)

@audio_bp.route('/')
@login_required
def index():
    """Audio learning home page"""
    audio_lessons = AudioLesson.query.all()
    return render_template('audio/index.html', audio_lessons=audio_lessons)

@audio_bp.route('/<int:audio_id>')
@login_required
def audio_details(audio_id):
    """Audio lesson details page"""
    audio_lesson = AudioLesson.query.get_or_404(audio_id)
    return render_template('audio/details.html', audio_lesson=audio_lesson)

@audio_bp.route('/<int:audio_id>/play')
@login_required
def play_audio(audio_id):
    """Play audio lesson page"""
    audio_lesson = AudioLesson.query.get_or_404(audio_id)
    # Check for existing playback record
    playback = AudioPlayback.query.filter_by(
        user_id=current_user.id, 
        audio_lesson_id=audio_id
    ).first()
    
    if not playback:
        playback = AudioPlayback(
            user_id=current_user.id,
            audio_lesson_id=audio_id
        )
        from src.main import db
        db.session.add(playback)
        db.session.commit()
        
    return render_template('audio/play.html', audio_lesson=audio_lesson, playback=playback)

@audio_bp.route('/by-subject')
@login_required
def by_subject():
    """View audio lessons by subject"""
    from src.models.lesson import Subject
    subjects = Subject.query.all()
    return render_template('audio/by_subject.html', subjects=subjects)

@audio_bp.route('/by-grade')
@login_required
def by_grade():
    """View audio lessons by grade level"""
    grade = request.args.get('grade', type=int)
    if grade:
        audio_lessons = AudioLesson.query.filter_by(grade_level=grade).all()
    else:
        audio_lessons = []
    return render_template('audio/by_grade.html', audio_lessons=audio_lessons, selected_grade=grade)

@audio_bp.route('/offline')
@login_required
def offline():
    """Offline audio lessons page"""
    return render_template('audio/offline.html')
