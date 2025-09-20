"""
Community models for The Golden Hand Learning Platform.

This module defines the models for community features, including posts, comments, and connections.
"""

from src.models.base import db
from datetime import datetime

class Community(db.Model):
    __tablename__ = 'communities'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.Text)
    category = db.Column(db.String(50))  # entrepreneurship, coding, design, etc.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    posts = db.relationship('CommunityPost', backref='community', lazy='dynamic')
    members = db.relationship('CommunityMembership', backref='community', lazy='dynamic')
    
    def __repr__(self):
        return f'<Community {self.name}>'


class CommunityMembership(db.Model):
    __tablename__ = 'community_memberships'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    community_id = db.Column(db.Integer, db.ForeignKey('communities.id'))
    role = db.Column(db.String(20), default='member')  # member, moderator, admin
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<CommunityMembership {self.id}>'


class CommunityPost(db.Model):
    __tablename__ = 'community_posts'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    community_id = db.Column(db.Integer, db.ForeignKey('communities.id'))
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    comments = db.relationship('Comment', backref='post', lazy='dynamic')
    
    def __repr__(self):
        return f'<CommunityPost {self.title}>'


class Comment(db.Model):
    __tablename__ = 'comments'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('community_posts.id'))
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Comment {self.id}>'


class PostComment(db.Model):
    __tablename__ = 'post_comments'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('community_posts.id'))
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<PostComment {self.id}>'


class UserConnection(db.Model):
    __tablename__ = 'user_connections'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    connected_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    connection_type = db.Column(db.String(20))  # mentor, peer, mentee
    status = db.Column(db.String(20))  # pending, accepted, rejected
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<UserConnection {self.id}>'


class Startup(db.Model):
    __tablename__ = 'startups'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.Text)
    industry = db.Column(db.String(50))
    founder_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    stage = db.Column(db.String(50))  # idea, prototype, mvp, growth
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    team_members = db.relationship('StartupTeam', backref='startup', lazy='dynamic')
    
    def __repr__(self):
        return f'<Startup {self.name}>'


class StartupTeam(db.Model):
    __tablename__ = 'startup_teams'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    startup_id = db.Column(db.Integer, db.ForeignKey('startups.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    role = db.Column(db.String(50))
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<StartupTeam {self.id}>'
