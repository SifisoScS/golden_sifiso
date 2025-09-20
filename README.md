# The Golden Hand - User Guide

## Overview
The Golden Hand is a comprehensive educational platform designed to empower South African students with digital technology skills and entrepreneurship mindset. The platform consists of five integrated components:

1. **Lessons Platform** - Structured, curriculum-aligned education for Grades 1-12 & Tertiary
2. **Quiz App** - Gamified, critical thinking-based mastery
3. **Audio Learning** - Accessible offline education by subject and grade
4. **Community Hub (SISONKE)** - Mentorship, peer support, and collaboration
5. **iKhaya AI** - A homegrown African AI hub for building AI solutions

## Getting Started

### Installation
1. Ensure you have Python 3.8+ installed
2. Clone the repository
3. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
5. Initialize the database:
   ```
   python create_db.py
   ```
6. Create test users (optional):
   ```
   python create_test_users.py
   ```

### Running the Application
1. Start the Flask development server:
   ```
   python -m src.main
   ```
2. Open your browser and navigate to `http://127.0.0.1:5000`

### Test User Credentials
- Admin: admin@goldenhand.com / admin123
- Student: student@goldenhand.com / student123

## Features

### Landing Page
The landing page showcases The Golden Hand's vision, structure, and educational journey. It highlights the platform's focus on equipping students with digital skills and entrepreneurship mindset.

### User Authentication
- User registration with grade level selection
- Secure login and session management
- Profile management

### Dashboard
- Overview of learning progress across all five components
- Recent lessons and quiz performance
- Startup idea generator
- Community activity feed
- Upcoming events

### Lessons Platform
- Structured curriculum-aligned lessons
- Grade-specific content
- Interactive learning materials

### Quiz App
- Gamified learning assessments
- Critical thinking challenges
- Progress tracking

### Audio Learning
- Offline-capable audio lessons
- Subject and grade categorization
- Progress tracking

### Community Hub (SISONKE)
- Peer support and mentorship
- Startup team formation
- Community posts and discussions
- Events calendar

### iKhaya AI
- AI project development
- Tutorials and resources
- Model training and dataset management

## Accessibility Features
- High contrast mode
- Text size adjustment
- Multilingual support (planned)
- Offline capabilities for audio content

## Technical Details
- Built with Flask framework
- SQLAlchemy for database ORM
- Flask-Login for authentication
- Responsive design with Tailwind CSS
- Interactive features with vanilla JavaScript

## Vision
The Golden Hand is designed to help South African students learn digital technology and equip them to start their own businesses after Grade 12, rather than solely pursuing traditional higher education or employment. The platform nurtures entrepreneurial mindsets and practical skills for the digital economy.

## Next Steps
1. Expand content library across all grade levels
2. Implement full multilingual support
3. Enhance offline capabilities
4. Develop mobile applications
5. Build partnerships with schools and organizations
