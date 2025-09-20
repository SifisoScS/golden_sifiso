"""
Technology Architect Agent for The Golden Hand Learning Platform.

This module implements a specialized agent for technology education,
providing personalized learning paths, content generation, and performance analysis
for technology and computer science topics.
"""

from typing import Dict, List, Any, Optional, Tuple
from src.specialized_agents.base_agent import BaseAgent, ContentType, LearningLevel


class TechnologyAgent(BaseAgent):
    """
    Specialized agent for technology education.
    
    This agent provides technology-specific learning resources, content generation,
    and performance analysis to support students in developing digital skills
    with a focus on practical applications and entrepreneurship.
    """
    
    def __init__(self, name: str = "Technology Architect", 
                description: str = "Specialized agent for technology and digital skills education"):
        """
        Initialize the Technology Architect agent.
        
        Args:
            name: The name of the agent
            description: A brief description of the agent's capabilities
        """
        super().__init__(name, description)
        self.topics_by_grade = self._initialize_topics()
        
    def _initialize_topics(self) -> Dict[int, List[str]]:
        """
        Initialize the technology topics by grade level.
        
        Returns:
            Dictionary mapping grade levels to lists of topics
        """
        return {
            1: ["Basic Computer Skills", "Digital Storytelling", "Introduction to Coding", "Online Safety"],
            2: ["Computer Parts", "Digital Art", "Simple Programming", "Internet Basics"],
            3: ["Word Processing", "Block Coding", "Digital Communication", "Responsible Technology Use"],
            4: ["Spreadsheet Basics", "Animation", "Computational Thinking", "Digital Citizenship"],
            5: ["Presentation Software", "Game Design Basics", "Introduction to Algorithms", "Digital Research"],
            6: ["Digital Media", "Website Basics", "Programming Concepts", "Data Collection"],
            7: ["Digital Design", "Web Development", "Programming with Python", "Data Analysis"],
            8: ["App Design", "Advanced Web Development", "Programming Projects", "Digital Solutions"],
            9: ["Computer Science Principles", "Web Applications", "Python Programming", "Database Basics"],
            10: ["Software Development", "Full Stack Development", "Data Structures", "User Experience Design"],
            11: ["Mobile App Development", "Advanced Programming", "Databases", "AI and Machine Learning Basics"],
            12: ["Entrepreneurial Technology", "Software Engineering", "Systems Design", "Emerging Technologies"]
        }
    
    def generate_learning_path(self, 
                              student_id: int, 
                              grade_level: int, 
                              prior_knowledge: Dict[str, float] = None) -> List[Dict[str, Any]]:
        """
        Generate a personalized technology learning path for a student.
        
        Args:
            student_id: The unique identifier for the student
            grade_level: The student's current grade level (1-12)
            prior_knowledge: Dictionary mapping topics to proficiency levels (0.0-1.0)
            
        Returns:
            A list of learning activities in recommended sequence
        """
        # Default prior knowledge if none provided
        if prior_knowledge is None:
            prior_knowledge = {}
        
        # Get topics for this grade level
        grade_topics = self.topics_by_grade.get(grade_level, [])
        if not grade_topics:
            return []
        
        learning_path = []
        
        # Create a learning path based on topics and prior knowledge
        for topic in grade_topics:
            # Get proficiency level (default to 0.0 if not known)
            proficiency = prior_knowledge.get(topic, 0.0)
            
            # Determine appropriate difficulty level
            if proficiency < 0.3:
                difficulty = LearningLevel.BEGINNER
            elif proficiency < 0.7:
                difficulty = LearningLevel.INTERMEDIATE
            else:
                difficulty = LearningLevel.ADVANCED
            
            # Add lesson activity
            learning_path.append({
                "type": "activity",
                "content_type": ContentType.LESSON.value,
                "topic": topic,
                "difficulty": difficulty.value,
                "title": f"{topic} - {difficulty.value.capitalize()} Level",
                "description": f"Learn about {topic} at a {difficulty.value} level",
                "estimated_time_minutes": 30
            })
            
            # Add coding practice for technology
            learning_path.append({
                "type": "activity",
                "content_type": "coding_practice",
                "topic": topic,
                "difficulty": difficulty.value,
                "title": f"{topic} Coding Practice",
                "description": f"Apply your knowledge with hands-on coding related to {topic}",
                "estimated_time_minutes": 45
            })
            
            # Add exercise activity
            learning_path.append({
                "type": "activity",
                "content_type": ContentType.EXERCISE.value,
                "topic": topic,
                "difficulty": difficulty.value,
                "title": f"{topic} Practice",
                "description": f"Practice {topic} with interactive exercises",
                "estimated_time_minutes": 20
            })
            
            # Add quiz for assessment
            learning_path.append({
                "type": "activity",
                "content_type": ContentType.QUIZ.value,
                "topic": topic,
                "difficulty": difficulty.value,
                "title": f"{topic} Quiz",
                "description": f"Test your knowledge of {topic}",
                "estimated_time_minutes": 15
            })
        
        # Add a project at the end to apply all topics
        learning_path.append({
            "type": "activity",
            "content_type": ContentType.PROJECT.value,
            "topic": "Technology Integration",
            "difficulty": LearningLevel.INTERMEDIATE.value,
            "title": f"Grade {grade_level} Technology Project",
            "description": "Apply technology concepts you've learned to build a real-world solution",
            "estimated_time_minutes": 120
        })
        
        # Add entrepreneurship-focused activity for higher grades
        if grade_level >= 8:
            learning_path.append({
                "type": "activity",
                "content_type": "startup_simulation",
                "topic": "Tech Entrepreneurship",
                "difficulty": LearningLevel.INTERMEDIATE.value,
                "title": "Tech Startup Simulation",
                "description": "Simulate launching a technology startup based on the skills you've learned",
                "estimated_time_minutes": 90
            })
        
        return learning_path
    
    def generate_content(self, 
                        topic: str, 
                        content_type: ContentType, 
                        difficulty: LearningLevel, 
                        grade_level: int) -> Dict[str, Any]:
        """
        Generate technology content for a given topic.
        
        Args:
            topic: The specific technology topic to generate content for
            content_type: The type of content to generate (lesson, exercise, etc.)
            difficulty: The difficulty level of the content
            grade_level: The target grade level (1-12)
            
        Returns:
            A dictionary containing the generated content
        """
        # Basic content structure
        content = {
            "topic": topic,
            "content_type": content_type.value,
            "difficulty": difficulty.value,
            "grade_level": grade_level,
            "title": f"{topic} - {content_type.value.capitalize()}",
            "created_at": "2025-05-21T06:20:00Z"
        }
        
        # Generate content based on type
        if content_type == ContentType.LESSON:
            content.update({
                "introduction": f"Welcome to this technology lesson on {topic}. We'll explore key concepts, practice coding, and discover how these skills can be applied in the real world and in entrepreneurship.",
                "objectives": [
                    f"Understand the fundamental principles of {topic}",
                    f"Develop practical skills in {topic}",
                    f"Learn how to apply {topic} to solve real-world problems",
                    f"Explore entrepreneurial opportunities related to {topic}"
                ],
                "sections": [
                    {
                        "title": "Key Concepts",
                        "content": f"This section covers the key concepts of {topic}...",
                        "illustrations": [
                            {"caption": "Diagram illustrating key concept", "image_url": "#"}
                        ]
                    },
                    {
                        "title": "Practical Application",
                        "content": f"Here's how to apply {topic} in practical scenarios...",
                        "code_examples": [
                            {"language": "python", "description": "Example 1", "code": "# Python code example\nprint('Hello, world!')"},
                            {"language": "html", "description": "Example 2", "code": "<!-- HTML example -->\n<h1>Hello, world!</h1>"}
                        ]
                    },
                    {
                        "title": "Real-World Applications",
                        "content": f"Here's how {topic} is used in industry and business...",
                        "examples": [
                            {"application": "E-commerce application", "description": "How this concept is used in online stores"},
                            {"application": "Mobile app development", "description": "How this concept is used in mobile applications"}
                        ]
                    },
                    {
                        "title": "Entrepreneurship Connection",
                        "content": f"Here's how {topic} can be leveraged to create business opportunities...",
                        "examples": [
                            {"business_opportunity": "Creating digital solutions for local businesses", "technical_basis": "Application of web development skills"}
                        ]
                    }
                ],
                "summary": f"In this lesson, we've covered the fundamentals of {topic}, its applications, and potential entrepreneurial opportunities."
            })
        
        elif content_type == ContentType.EXERCISE:
            # Generate exercises based on difficulty
            num_problems = 5 if difficulty == LearningLevel.BEGINNER else (
                8 if difficulty == LearningLevel.INTERMEDIATE else 10)
            
            problems = []
            for i in range(num_problems):
                problems.append({
                    "id": f"problem_{i+1}",
                    "question": f"Sample {topic} problem {i+1} for {difficulty.value} level",
                    "options": ["Option A", "Option B", "Option C", "Option D"] if i % 2 == 0 else None,
                    "answer": "Option B" if i % 2 == 0 else "Sample answer",
                    "explanation": f"Explanation for problem {i+1}"
                })
            
            content.update({
                "instructions": f"Practice the following {topic} problems. Apply your technical knowledge and problem-solving skills.",
                "problems": problems,
                "hints_available": True
            })
        
        elif content_type == ContentType.QUIZ:
            # Generate quiz questions
            questions = []
            for i in range(10):
                questions.append({
                    "id": f"question_{i+1}",
                    "text": f"Sample {topic} quiz question {i+1}",
                    "options": ["Option A", "Option B", "Option C", "Option D"],
                    "correct_answer": "Option C",
                    "points": 1
                })
            
            content.update({
                "instructions": f"This quiz will test your knowledge of {topic}. Select the best answer for each question.",
                "time_limit_minutes": 15,
                "passing_score": 7,
                "questions": questions
            })
        
        elif content_type == ContentType.PROJECT:
            content.update({
                "title": f"{topic} Project: Building a Digital Solution",
                "description": f"Apply your knowledge of {topic} to develop a solution to a real-world problem.",
                "objectives": [
                    "Apply technology concepts to a practical challenge",
                    "Develop technical implementation skills",
                    "Connect technology to entrepreneurship and innovation"
                ],
                "scenario": f"South African communities and businesses face various challenges that can be addressed with technology. Use your knowledge of {topic} to develop a digital solution to one of these challenges...",
                "tasks": [
                    {"description": "Task 1: Identify a problem that can be solved with technology", "deliverable": "Problem statement"},
                    {"description": "Task 2: Design your solution", "deliverable": "Solution design document"},
                    {"description": "Task 3: Implement a prototype", "deliverable": "Working prototype"},
                    {"description": "Task 4: Test your solution", "deliverable": "Test results"},
                    {"description": "Task 5: Develop a business model", "deliverable": "Business plan"}
                ],
                "resources": [
                    {"name": "Project guide", "type": "document", "url": "#"},
                    {"name": "Code templates", "type": "code", "url": "#"},
                    {"name": "Business model canvas", "type": "document", "url": "#"}
                ],
                "rubric": [
                    {"criterion": "Technical implementation", "weight": 30},
                    {"criterion": "Problem-solving approach", "weight": 20},
                    {"criterion": "User experience", "weight": 20},
                    {"criterion": "Business potential", "weight": 15},
                    {"criterion": "Presentation quality", "weight": 15}
                ]
            })
        
        elif content_type == ContentType.ASSESSMENT:
            content.update({
                "instructions": f"This assessment will evaluate your understanding of {topic}.",
                "sections": [
                    {
                        "name": "Multiple Choice",
                        "questions": [
                            {"id": "mc_1", "text": "Sample multiple choice question 1", "options": ["A", "B", "C", "D"], "answer": "B"},
                            {"id": "mc_2", "text": "Sample multiple choice question 2", "options": ["A", "B", "C", "D"], "answer": "A"}
                        ]
                    },
                    {
                        "name": "Coding Problems",
                        "questions": [
                            {"id": "code_1", "text": "Write a function that...", "starter_code": "def solution():\n    # Your code here\n    pass", "test_cases": [{"input": "example input", "expected_output": "example output"}]},
                            {"id": "code_2", "text": "Create a program that...", "starter_code": "# Your code here", "test_cases": [{"input": "example input", "expected_output": "example output"}]}
                        ]
                    },
                    {
                        "name": "Application Design",
                        "questions": [
                            {"id": "design_1", "text": "Design a solution for the following scenario...", "answer": "Sample solution approach"}
                        ]
                    }
                ],
                "time_limit_minutes": 60,
                "total_points": 100
            })
        
        # Special case for coding practice content
        elif str(content_type.value).lower() == "coding_practice" or content_type.value == "coding_practice":
            content.update({
                "content_type": "coding_practice",
                "title": f"{topic} Coding Practice",
                "introduction": f"In this coding practice, you will apply your knowledge of {topic} by writing and running code.",
                "setup_instructions": [
                    "Make sure you have the necessary software installed",
                    "Create a new project folder",
                    "Follow the instructions for each task"
                ],
                "tasks": [
                    {
                        "title": "Task 1: Basic Implementation",
                        "description": "Implement a simple solution that demonstrates the core concept",
                        "starter_code": "# Your code here",
                        "hints": ["Think about how to structure your solution", "Remember to handle edge cases"],
                        "test_cases": [{"input": "example input", "expected_output": "example output"}]
                    },
                    {
                        "title": "Task 2: Advanced Implementation",
                        "description": "Extend your solution to handle more complex scenarios",
                        "starter_code": "# Your code here",
                        "hints": ["Build on your previous solution", "Consider performance optimization"],
                        "test_cases": [{"input": "example input", "expected_output": "example output"}]
                    }
                ],
                "resources": [
                    {"name": "Documentation", "url": "#"},
                    {"name": "Tutorial video", "url": "#"}
                ],
                "submission_instructions": "Submit your code files along with a brief explanation of your approach."
            })
        
        # Special case for startup simulation content
        elif str(content_type.value).lower() == "startup_simulation" or content_type.value == "startup_simulation":
            content.update({
                "content_type": "startup_simulation",
                "title": "Tech Startup Simulation",
                "introduction": "In this simulation, you will experience the process of launching a technology startup based on the skills you've learned.",
                "objectives": [
                    "Apply technical skills to a business context",
                    "Understand the startup development process",
                    "Develop entrepreneurial thinking",
                    "Practice pitching and presenting business ideas"
                ],
                "phases": [
                    {
                        "title": "Phase 1: Ideation",
                        "description": "Generate and evaluate business ideas based on technology solutions",
                        "activities": [
                            "Identify problems that can be solved with technology",
                            "Brainstorm potential solutions",
                            "Evaluate ideas based on feasibility and market potential"
                        ],
                        "deliverable": "Business idea document"
                    },
                    {
                        "title": "Phase 2: Market Research",
                        "description": "Research your target market and competition",
                        "activities": [
                            "Define your target audience",
                            "Analyze competitors",
                            "Identify your unique value proposition"
                        ],
                        "deliverable": "Market research report"
                    },
                    {
                        "title": "Phase 3: Prototype Development",
                        "description": "Create a simple prototype of your solution",
                        "activities": [
                            "Design user interface mockups",
                            "Develop a basic working prototype",
                            "Test with potential users"
                        ],
                        "deliverable": "Prototype and user feedback"
                    },
                    {
                        "title": "Phase 4: Business Model",
                        "description": "Develop a business model for your startup",
                        "activities": [
                            "Define revenue streams",
                            "Identify key resources and partners",
                            "Calculate startup costs and projections"
                        ],
                        "deliverable": "Business model canvas"
                    },
                    {
                        "title": "Phase 5: Pitch",
                        "description": "Create and deliver a pitch for your startup",
                        "activities": [
                            "Develop a pitch deck",
                            "Practice your presentation",
                            "Deliver your pitch and answer questions"
                        ],
                        "deliverable": "Pitch presentation"
                    }
                ],
                "resources": [
                    {"name": "Business Model Canvas Template", "url": "#"},
                    {"name": "Pitch Deck Template", "url": "#"},
                    {"name": "South African Startup Resources", "url": "#"}
                ],
                "evaluation_criteria": [
                    {"criterion": "Innovation and creativity", "weight": 20},
                    {"criterion": "Technical feasibility", "weight": 20},
                    {"criterion": "Market potential", "weight": 20},
                    {"criterion": "Business model viability", "weight": 20},
                    {"criterion": "Pitch quality", "weight": 20}
                ]
            })
        
        return content
    
    def analyze_performance(self, 
                           student_id: int, 
                           activity_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze a student's technology performance and provide feedback.
        
        Args:
            student_id: The unique identifier for the student
            activity_results: Results from a learning activity
            
        Returns:
            Analysis results with feedback and recommendations
        """
        # Extract basic information
        activity_type = activity_results.get("activity_type", "unknown")
        topic = activity_results.get("topic", "unknown")
        score = activity_results.get("score", 0)
        max_score = activity_results.get("max_score", 100)
        answers = activity_results.get("answers", [])
        
        # Calculate percentage score
        percentage = (score / max_score * 100) if max_score > 0 else 0
        
        # Determine performance level
        if percentage >= 90:
            performance_level = "Excellent"
            next_steps = ["Explore advanced concepts in this topic", "Start a personal project applying these skills"]
        elif percentage >= 75:
            performance_level = "Good"
            next_steps = ["Review specific areas of difficulty", "Practice with more complex examples"]
        elif percentage >= 60:
            performance_level = "Satisfactory"
            next_steps = ["Focus on areas of weakness", "Review core concepts and practice more"]
        else:
            performance_level = "Needs Improvement"
            next_steps = ["Revisit fundamental concepts", "Work with simpler examples and exercises"]
        
        # Identify strengths and weaknesses
        strengths = []
        weaknesses = []
        
        # This would be more sophisticated in a real implementation
        # For now, we'll use a simple rule-based approach
        if activity_type == "quiz" and answers:
            # Analyze question categories (simplified)
            categories = {}
            for answer in answers:
                category = answer.get("category", "general")
                correct = answer.get("correct", False)
                
                if category not in categories:
                    categories[category] = {"correct": 0, "total": 0}
                
                categories[category]["total"] += 1
                if correct:
                    categories[category]["correct"] += 1
            
            # Determine strengths and weaknesses based on category performance
            for category, stats in categories.items():
                if stats["total"] > 0:
                    cat_percentage = (stats["correct"] / stats["total"]) * 100
                    if cat_percentage >= 80:
                        strengths.append(category)
                    elif cat_percentage <= 50:
                        weaknesses.append(category)
        
        # Generate analysis
        analysis = {
            "student_id": student_id,
            "topic": topic,
            "activity_type": activity_type,
            "score": score,
            "max_score": max_score,
            "percentage": percentage,
            "performance_level": performance_level,
            "strengths": strengths or ["Not enough data to determine specific strengths"],
            "weaknesses": weaknesses or ["Not enough data to determine specific weaknesses"],
            "feedback": f"You scored {percentage:.1f}% on this {activity_type}. {performance_level}.",
            "next_steps": next_steps,
            "recommended_resources": self.suggest_resources(topic)
        }
        
        # Add coding assessment if applicable
        if activity_type in ["coding_practice", "project"]:
            analysis["coding_skills"] = {
                "code_quality": 4,  # Scale of 1-5
                "problem_solving": 3,
                "efficiency": 4,
                "documentation": 3,
                "overall": 3.5,
                "feedback": "Your code is well-structured and efficient. Work on improving documentation and problem-solving approaches."
            }
        
        # Add entrepreneurship connection
        analysis["entrepreneurship_connection"] = self.get_entrepreneurship_connection(topic, 10)
        
        return analysis
    
    def answer_question(self, 
                       question: str, 
                       context: Dict[str, Any] = None) -> Tuple[str, float]:
        """
        Answer a technology question from a student.
        
        Args:
            question: The question text
            context: Additional context about the question
            
        Returns:
            A tuple containing (answer, confidence_score)
        """
        # This is a simplified implementation
        # In a real system, this would use more sophisticated NLP and tech knowledge
        
        # Default context
        if context is None:
            context = {}
        
        # Extract topic from context if available
        topic = context.get("topic", "unknown")
        grade_level = context.get("grade_level", 10)
        
        # Simple keyword matching for demonstration
        keywords = question.lower().split()
        
        # Check for question types
        if any(word in keywords for word in ["programming", "code", "coding"]):
            answer = "Programming is the process of creating instructions for computers to follow. It involves writing code in languages like Python, JavaScript, or Java to solve problems and build applications."
            confidence = 0.9
        elif any(word in keywords for word in ["web", "website", "html", "css"]):
            answer = "Web development involves creating websites and web applications. HTML is used for structure, CSS for styling, and JavaScript for interactivity. Backend technologies like Python, PHP, or Node.js handle server-side logic."
            confidence = 0.85
        elif any(word in keywords for word in ["app", "mobile", "android", "ios"]):
            answer = "Mobile app development involves creating applications for smartphones and tablets. Android apps are typically built with Java or Kotlin, while iOS apps use Swift or Objective-C. Cross-platform frameworks like React Native or Flutter allow development for both platforms."
            confidence = 0.85
        elif any(word in keywords for word in ["database", "data", "sql"]):
            answer = "Databases store and organize data for applications. SQL (Structured Query Language) is used to manage relational databases like MySQL or PostgreSQL. NoSQL databases like MongoDB store data in different formats and are often used for large-scale applications."
            confidence = 0.85
        elif any(word in keywords for word in ["ai", "artificial intelligence", "machine learning"]):
            answer = "Artificial Intelligence (AI) enables computers to perform tasks that typically require human intelligence. Machine Learning is a subset of AI that allows systems to learn from data and improve over time without explicit programming."
            confidence = 0.8
        elif any(word in keywords for word in ["business", "entrepreneur", "startup"]):
            # Get entrepreneurship connection
            connection = self.get_entrepreneurship_connection(topic, grade_level)
            answer = connection.get("description", "Technology skills are essential for modern entrepreneurship, enabling the creation of digital products and services that solve real-world problems.")
            confidence = 0.7
        else:
            answer = "I'm not sure about the answer to this specific technology question. Could you provide more details or rephrase it?"
            confidence = 0.3
        
        return answer, confidence
    
    def suggest_resources(self, 
                         topic: str, 
                         learning_style: str = None, 
                         difficulty: LearningLevel = None) -> List[Dict[str, Any]]:
        """
        Suggest technology resources for further learning.
        
        Args:
            topic: The topic to find resources for
            learning_style: The student's preferred learning style
            difficulty: The preferred difficulty level
            
        Returns:
            A list of resource recommendations
        """
        # Default difficulty if not specified
        if difficulty is None:
            difficulty = LearningLevel.INTERMEDIATE
        
        # Base resources that are generally helpful
        resources = [
            {
                "title": "freeCodeCamp",
                "description": f"Free interactive coding lessons on {topic}",
                "url": "https://www.freecodecamp.org/",
                "type": "interactive",
                "difficulty": LearningLevel.BEGINNER.value
            },
            {
                "title": "W3Schools",
                "description": "Web development tutorials and references",
                "url": "https://www.w3schools.com/",
                "type": "tutorial",
                "difficulty": LearningLevel.INTERMEDIATE.value
            },
            {
                "title": "GitHub Learning Lab",
                "description": "Interactive courses on coding and development",
                "url": "https://lab.github.com/",
                "type": "interactive",
                "difficulty": LearningLevel.INTERMEDIATE.value
            },
            {
                "title": "Tech Entrepreneurship",
                "description": "Learn how to build a tech startup",
                "url": "#",
                "type": "course",
                "difficulty": LearningLevel.INTERMEDIATE.value
            }
        ]
        
        # Add resources based on learning style if specified
        if learning_style == "visual":
            resources.append({
                "title": "Visual Tech Tutorials",
                "description": f"Visual explanations of {topic} with diagrams and videos",
                "url": "#",
                "type": "video",
                "difficulty": difficulty.value
            })
        elif learning_style == "auditory":
            resources.append({
                "title": f"{topic} Explained - Tech Podcast",
                "description": f"Audio explanations of {topic} concepts",
                "url": "#",
                "type": "audio",
                "difficulty": difficulty.value
            })
        elif learning_style == "kinesthetic":
            resources.append({
                "title": f"Hands-on {topic} Projects",
                "description": f"Interactive projects to learn {topic} by doing",
                "url": "#",
                "type": "project",
                "difficulty": difficulty.value
            })
        
        # Add difficulty-specific resources
        if difficulty == LearningLevel.BEGINNER:
            resources.append({
                "title": f"{topic} for Beginners",
                "description": f"Introduction to basic concepts in {topic}",
                "url": "#",
                "type": "course",
                "difficulty": LearningLevel.BEGINNER.value
            })
        elif difficulty == LearningLevel.ADVANCED:
            resources.append({
                "title": f"Advanced {topic}",
                "description": f"In-depth exploration of advanced concepts in {topic}",
                "url": "#",
                "type": "course",
                "difficulty": LearningLevel.ADVANCED.value
            })
        
        # Add South African context resource
        resources.append({
            "title": f"South African {topic} Community",
            "description": f"Connect with local developers and entrepreneurs interested in {topic}",
            "url": "#",
            "type": "community",
            "difficulty": difficulty.value
        })
        
        # Add entrepreneurship-focused resource
        resources.append({
            "title": f"From Code to Company: Building a {topic} Startup",
            "description": f"Learn how to turn your {topic} skills into a viable business",
            "url": "#",
            "type": "course",
            "difficulty": difficulty.value,
            "tags": ["entrepreneurship", "startup", "business"]
        })
        
        return resources
    
    def get_entrepreneurship_connection(self, 
                                       topic: str, 
                                       grade_level: int) -> Dict[str, Any]:
        """
        Connect technology topics to entrepreneurship opportunities.
        
        Args:
            topic: The academic topic to connect to entrepreneurship
            grade_level: The student's grade level
            
        Returns:
            Information connecting the topic to business opportunities
        """
        # Define connections between technology topics and entrepreneurship
        entrepreneurship_connections = {
            "Web Development": {
                "description": "Web development skills enable you to create websites and web applications for businesses and organizations.",
                "business_applications": [
                    "Creating websites for local businesses",
                    "Developing e-commerce platforms",
                    "Building web applications for specific industries"
                ],
                "startup_ideas": [
                    "Web development agency serving local businesses",
                    "Industry-specific web application (e.g., for healthcare, education)",
                    "Online marketplace for local products"
                ],
                "case_study": "How a young developer from Soweto built a web development agency serving over 50 local businesses, creating employment for 10 people."
            },
            "Mobile App Development": {
                "description": "Mobile app development allows you to create applications that solve problems for smartphone users.",
                "business_applications": [
                    "Creating apps for businesses to reach customers",
                    "Developing solutions for specific local challenges",
                    "Building tools for other businesses"
                ],
                "startup_ideas": [
                    "Mobile app for connecting local service providers with customers",
                    "Transportation or delivery app for your community",
                    "Educational app focused on South African curriculum"
                ],
                "case_study": "How a team of students from Cape Town developed a mobile app that helps people find safe transportation, now used by thousands daily."
            },
            "Programming": {
                "description": "Programming skills are the foundation for creating software solutions to various problems.",
                "business_applications": [
                    "Developing custom software for businesses",
                    "Creating automation tools",
                    "Building data analysis solutions"
                ],
                "startup_ideas": [
                    "Software development consultancy",
                    "Industry-specific software solution",
                    "Educational programming platform for African students"
                ],
                "case_study": "How a self-taught programmer from Durban built a software company that now employs 25 people and serves clients across Africa."
            },
            "Data Analysis": {
                "description": "Data analysis skills allow you to help businesses make better decisions based on their data.",
                "business_applications": [
                    "Analyzing customer data for businesses",
                    "Creating dashboards and reports",
                    "Optimizing business operations"
                ],
                "startup_ideas": [
                    "Data analytics consultancy for small businesses",
                    "Industry-specific data solution (e.g., for agriculture, retail)",
                    "Market research service for African markets"
                ],
                "case_study": "How a Johannesburg entrepreneur built a data analytics company that helps small businesses increase their revenue by understanding customer behavior."
            },
            "Artificial Intelligence": {
                "description": "AI skills enable you to create intelligent systems that can automate tasks and provide insights.",
                "business_applications": [
                    "Developing AI-powered customer service solutions",
                    "Creating predictive analytics tools",
                    "Building recommendation systems"
                ],
                "startup_ideas": [
                    "AI-powered solution for a specific industry challenge",
                    "Chatbot development agency",
                    "AI education platform for African students"
                ],
                "case_study": "How a tech startup in Pretoria developed an AI solution for agriculture that helps farmers increase crop yields by 30%."
            }
        }
        
        # Default connection for topics not specifically listed
        default_connection = {
            "description": "Technology skills are essential for modern entrepreneurship, enabling the creation of digital products and services that solve real-world problems.",
            "business_applications": [
                "Developing digital solutions for businesses",
                "Creating online platforms and services",
                "Building tools that solve specific problems"
            ],
            "startup_ideas": [
                "Identify a local problem that can be solved with technology",
                "Create a digital service for a specific community or industry"
            ],
            "case_study": "How South African tech entrepreneurs are building successful businesses by solving local problems with technology."
        }
        
        # Find the most relevant connection
        # First try exact match
        connection = entrepreneurship_connections.get(topic)
        
        # If no exact match, try to find a partial match
        if connection is None:
            for key, value in entrepreneurship_connections.items():
                if key.lower() in topic.lower() or topic.lower() in key.lower():
                    connection = value
                    break
        
        # If still no match, use the default
        if connection is None:
            connection = default_connection
        
        # Add grade-appropriate context
        if grade_level <= 6:
            connection["grade_context"] = "Even at this early stage, learning technology helps you understand how digital tools can solve problems around you."
        elif grade_level <= 9:
            connection["grade_context"] = "At this grade level, you can start creating simple websites, apps, or programs that address needs in your school or community."
        else:
            connection["grade_context"] = "With these advanced technology skills, you're equipped to develop professional-quality solutions that could form the basis of a real startup."
        
        # Add topic and grade level to the result
        connection["topic"] = topic
        connection["grade_level"] = grade_level
        
        return connection
