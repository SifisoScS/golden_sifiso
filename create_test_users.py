from src.main import app, db
from src.models.user import User
from werkzeug.security import generate_password_hash

with app.app_context():
    # Create a test admin user
    admin = User(
        username="admin",
        email="admin@goldenhand.com",
        first_name="Admin",
        last_name="User",
        grade=12,
        role="admin"
    )
    admin.password_hash = generate_password_hash("admin123")
    
    # Create a test student user
    student = User(
        username="student",
        email="student@goldenhand.com",
        first_name="Student",
        last_name="User",
        grade=10,
        role="student"
    )
    student.password_hash = generate_password_hash("student123")
    
    # Add users to database
    db.session.add(admin)
    db.session.add(student)
    db.session.commit()
    
    print("Test users created successfully!")
    print("Admin login: admin@goldenhand.com / admin123")
    print("Student login: student@goldenhand.com / student123")
