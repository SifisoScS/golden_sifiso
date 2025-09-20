from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from src.models.community import Community, CommunityPost, PostComment, Startup, StartupTeam

community_bp = Blueprint('community', __name__)

@community_bp.route('/')
@login_required
def index():
    """Community hub home page"""
    communities = Community.query.all()
    startups = Startup.query.order_by(Startup.created_at.desc()).limit(5).all()
    return render_template('community/index.html', communities=communities, startups=startups)

@community_bp.route('/community/<int:community_id>')
@login_required
def community_details(community_id):
    """Community details page"""
    community = Community.query.get_or_404(community_id)
    posts = CommunityPost.query.filter_by(community_id=community_id).order_by(CommunityPost.created_at.desc()).all()
    return render_template('community/details.html', community=community, posts=posts)

@community_bp.route('/post/<int:post_id>')
@login_required
def post_details(post_id):
    """Post details page"""
    post = CommunityPost.query.get_or_404(post_id)
    comments = PostComment.query.filter_by(post_id=post_id).order_by(PostComment.created_at).all()
    return render_template('community/post.html', post=post, comments=comments)

@community_bp.route('/startups')
@login_required
def startups():
    """Startups listing page"""
    startups = Startup.query.all()
    return render_template('community/startups.html', startups=startups)

@community_bp.route('/startup/<int:startup_id>')
@login_required
def startup_details(startup_id):
    """Startup details page"""
    startup = Startup.query.get_or_404(startup_id)
    team_members = StartupTeam.query.filter_by(startup_id=startup_id).all()
    return render_template('community/startup_details.html', startup=startup, team_members=team_members)

@community_bp.route('/mentorship')
@login_required
def mentorship():
    """Mentorship program page"""
    return render_template('community/mentorship.html')

@community_bp.route('/events')
@login_required
def events():
    """Community events page"""
    return render_template('community/events.html')
