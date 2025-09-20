"""
Mathematics Navigator Agent for The Golden Hand Learning Platform.

This module implements a specialized agent for mathematics education,
providing personalized learning paths, content generation, and performance analysis
for mathematics topics.
"""

from typing import Dict, List, Any, Optional, Tuple
from src.specialized_agents.base_agent import BaseAgent, ContentType, LearningLevel


class MathematicsAgent(BaseAgent):
    """
    Specialized agent for mathematics education.
    
    This agent provides mathematics-specific learning resources, content generation,
    and performance analysis to support students in developing mathematical skills
    with a focus on practical applications and entrepreneurship.
    """
    
    def __init__(self, name: str = "Mathematics Navigator", 
                description: str = "Specialized agent for mathematics education"):
        """
        Initialize the Mathematics Navigator agent.
        
        Args:
            name: The name of the agent
            description: A brief description of the agent's capabilities
        """
        super().__init__(name, description)
        self.topics_by_grade = self._initialize_topics()
        
    def _initialize_topics(self) -> Dict[int, List[str]]:
        """
        Initialize the mathematics topics by grade level.
        
        Returns:
            Dictionary mapping grade levels to lists of topics
        """
        return {
            1: ["Counting", "Basic Addition", "Basic Subtraction", "Shapes"],
            2: ["Addition", "Subtraction", "Simple Fractions", "Time"],
            3: ["Multiplication", "Division", "Fractions", "Measurement"],
            4: ["Multi-digit Operations", "Decimals", "Geometry", "Data Analysis"],
            5: ["Fractions Operations", "Decimals Operations", "Geometry", "Measurement"],
            6: ["Ratios", "Percentages", "Intro to Algebra", "Statistics"],
            7: ["Pre-Algebra", "Geometry", "Statistics", "Probability"],
            8: ["Algebra I", "Geometry", "Data Analysis", "Mathematical Modeling"],
            9: ["Algebra II", "Geometry", "Trigonometry", "Statistics"],
            10: ["Advanced Algebra", "Trigonometry", "Probability", "Financial Mathematics"],
            11: ["Pre-Calculus", "Statistics", "Mathematical Modeling", "Business Mathematics"],
            12: ["Calculus", "Advanced Statistics", "Discrete Mathematics", "Financial Planning"]
        }
    
    def generate_learning_path(self, 
                              student_id: int, 
                              grade_level: int, 
                              prior_knowledge: Dict[str, float] = None) -> List[Dict[str, Any]]:
        """
        Generate a personalized mathematics learning path for a student.
        
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
            "topic": "Mathematics Integration",
            "difficulty": LearningLevel.INTERMEDIATE.value,
            "title": f"Grade {grade_level} Mathematics Project",
            "description": "Apply all the mathematics concepts you've learned in a real-world project",
            "estimated_time_minutes": 60
        })
        
        return learning_path
    
    def generate_content(self, 
                        topic: str, 
                        content_type: ContentType, 
                        difficulty: LearningLevel, 
                        grade_level: int) -> Dict[str, Any]:
        """
        Generate mathematics content for a given topic.
        
        Args:
            topic: The specific mathematics topic to generate content for
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
            "created_at": "2025-05-21T06:16:00Z"
        }
        
        # Generate content based on type
        if content_type == ContentType.LESSON:
            content.update({
                "introduction": f"Welcome to this lesson on {topic}. We'll explore key concepts and applications.",
                "objectives": [
                    f"Understand the fundamental principles of {topic}",
                    f"Learn how to apply {topic} to solve problems",
                    f"Connect {topic} to real-world applications"
                ],
                "sections": [
                    {
                        "title": "Key Concepts",
                        "content": f"This section covers the key concepts of {topic}...",
                        "examples": [
                            {"problem": "Example problem 1", "solution": "Step-by-step solution 1"},
                            {"problem": "Example problem 2", "solution": "Step-by-step solution 2"}
                        ]
                    },
                    {
                        "title": "Applications",
                        "content": f"Here's how {topic} is applied in real-world situations...",
                        "examples": [
                            {"scenario": "Real-world scenario 1", "application": "How to apply the concept"}
                        ]
                    },
                    {
                        "title": "Entrepreneurship Connection",
                        "content": f"Here's how {topic} can be used in business and entrepreneurship...",
                        "examples": [
                            {"business_scenario": "Business application", "mathematical_approach": "How to use math to solve it"}
                        ]
                    }
                ],
                "summary": f"In this lesson, we've covered the fundamentals of {topic} and its applications."
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
                "instructions": f"Practice the following {topic} problems. Take your time and show your work.",
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
                "title": f"{topic} Project: Real-World Application",
                "description": f"Apply your knowledge of {topic} to solve a real-world problem.",
                "objectives": [
                    "Apply mathematical concepts to a practical scenario",
                    "Develop problem-solving skills",
                    "Connect mathematics to entrepreneurship"
                ],
                "scenario": f"You are starting a small business and need to use {topic} to optimize your operations...",
                "tasks": [
                    {"description": "Task 1: Analyze the problem", "deliverable": "Analysis document"},
                    {"description": "Task 2: Apply mathematical concepts", "deliverable": "Mathematical model"},
                    {"description": "Task 3: Implement your solution", "deliverable": "Implementation plan"},
                    {"description": "Task 4: Present your findings", "deliverable": "Presentation"}
                ],
                "resources": [
                    {"name": "Project guide", "type": "document", "url": "#"},
                    {"name": "Sample data", "type": "spreadsheet", "url": "#"}
                ],
                "rubric": [
                    {"criterion": "Mathematical accuracy", "weight": 30},
                    {"criterion": "Problem-solving approach", "weight": 25},
                    {"criterion": "Real-world applicability", "weight": 25},
                    {"criterion": "Presentation quality", "weight": 20}
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
                        "name": "Problem Solving",
                        "questions": [
                            {"id": "ps_1", "text": "Sample problem 1", "answer": "Sample solution 1"},
                            {"id": "ps_2", "text": "Sample problem 2", "answer": "Sample solution 2"}
                        ]
                    }
                ],
                "time_limit_minutes": 45,
                "total_points": 100
            })
        
        return content
    
    def analyze_performance(self, 
                           student_id: int, 
                           activity_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze a student's mathematics performance and provide feedback.
        
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
            next_steps = ["Move to more advanced topics", "Try more challenging problems"]
        elif percentage >= 75:
            performance_level = "Good"
            next_steps = ["Review specific areas of difficulty", "Practice with more examples"]
        elif percentage >= 60:
            performance_level = "Satisfactory"
            next_steps = ["Focus on areas of weakness", "Review core concepts"]
        else:
            performance_level = "Needs Improvement"
            next_steps = ["Revisit fundamental concepts", "Work with simpler examples first"]
        
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
        
        # Add entrepreneurship connection
        analysis["entrepreneurship_connection"] = self.get_entrepreneurship_connection(topic, 10)
        
        return analysis
    
    def answer_question(self, 
                       question: str, 
                       context: Dict[str, Any] = None) -> Tuple[str, float]:
        """
        Answer a mathematics question from a student.
        
        Args:
            question: The question text
            context: Additional context about the question
            
        Returns:
            A tuple containing (answer, confidence_score)
        """
        # This is a simplified implementation
        # In a real system, this would use more sophisticated NLP and math parsing
        
        # Default context
        if context is None:
            context = {}
        
        # Extract topic from context if available
        topic = context.get("topic", "unknown")
        grade_level = context.get("grade_level", 10)
        
        # Simple keyword matching for demonstration
        keywords = question.lower().split()
        
        # Check for question types
        if any(word in keywords for word in ["add", "sum", "plus", "addition"]):
            answer = "To add numbers, you combine their values. For example, 5 + 3 = 8."
            confidence = 0.9
        elif any(word in keywords for word in ["subtract", "minus", "difference"]):
            answer = "To subtract, you find the difference between two numbers. For example, 8 - 3 = 5."
            confidence = 0.9
        elif any(word in keywords for word in ["multiply", "product", "times"]):
            answer = "Multiplication is repeated addition. For example, 4 × 3 means 4 + 4 + 4 = 12."
            confidence = 0.9
        elif any(word in keywords for word in ["divide", "quotient"]):
            answer = "Division is sharing a number into equal parts. For example, 12 ÷ 3 = 4."
            confidence = 0.9
        elif any(word in keywords for word in ["formula", "equation"]):
            answer = "Mathematical formulas express relationships between variables. For example, the area of a rectangle is A = length × width."
            confidence = 0.8
        elif any(word in keywords for word in ["business", "entrepreneur", "startup"]):
            # Get entrepreneurship connection
            connection = self.get_entrepreneurship_connection(topic, grade_level)
            answer = connection.get("description", "Mathematics is essential for business planning and financial management.")
            confidence = 0.7
        else:
            answer = "I'm not sure about the answer to this specific mathematics question. Could you provide more details or rephrase it?"
            confidence = 0.3
        
        return answer, confidence
    
    def suggest_resources(self, 
                         topic: str, 
                         learning_style: str = None, 
                         difficulty: LearningLevel = None) -> List[Dict[str, Any]]:
        """
        Suggest mathematics resources for further learning.
        
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
                "title": "Khan Academy",
                "description": f"Free online lessons and exercises on {topic}",
                "url": "https://www.khanacademy.org/math",
                "type": "interactive",
                "difficulty": LearningLevel.BEGINNER.value
            },
            {
                "title": "Desmos",
                "description": "Interactive graphing calculator and activities",
                "url": "https://www.desmos.com/",
                "type": "tool",
                "difficulty": LearningLevel.INTERMEDIATE.value
            },
            {
                "title": "Mathematics for Business and Economics",
                "description": "Learn how mathematics applies to business scenarios",
                "url": "#",
                "type": "course",
                "difficulty": LearningLevel.INTERMEDIATE.value
            }
        ]
        
        # Add resources based on learning style if specified
        if learning_style == "visual":
            resources.append({
                "title": "Visual Mathematics",
                "description": f"Visual explanations of {topic} with interactive diagrams",
                "url": "#",
                "type": "interactive",
                "difficulty": difficulty.value
            })
        elif learning_style == "auditory":
            resources.append({
                "title": f"{topic} Explained - Audio Course",
                "description": f"Audio lectures explaining {topic} concepts",
                "url": "#",
                "type": "audio",
                "difficulty": difficulty.value
            })
        elif learning_style == "kinesthetic":
            resources.append({
                "title": f"Hands-on {topic} Activities",
                "description": f"Physical and interactive activities to learn {topic}",
                "url": "#",
                "type": "activity",
                "difficulty": difficulty.value
            })
        
        # Add difficulty-specific resources
        if difficulty == LearningLevel.BEGINNER:
            resources.append({
                "title": f"{topic} Fundamentals",
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
        
        # Add entrepreneurship-focused resource
        resources.append({
            "title": f"Mathematics in Entrepreneurship: {topic} Applications",
            "description": f"Learn how {topic} is applied in business and entrepreneurship",
            "url": "#",
            "type": "course",
            "difficulty": difficulty.value,
            "tags": ["entrepreneurship", "business", "application"]
        })
        
        return resources
    
    def get_entrepreneurship_connection(self, 
                                       topic: str, 
                                       grade_level: int) -> Dict[str, Any]:
        """
        Connect mathematics topics to entrepreneurship opportunities.
        
        Args:
            topic: The academic topic to connect to entrepreneurship
            grade_level: The student's grade level
            
        Returns:
            Information connecting the topic to business opportunities
        """
        # Define connections between math topics and entrepreneurship
        entrepreneurship_connections = {
            "Algebra": {
                "description": "Algebra is essential for financial modeling, pricing strategies, and growth projections in startups.",
                "business_applications": [
                    "Creating pricing models",
                    "Forecasting revenue growth",
                    "Calculating break-even points"
                ],
                "startup_ideas": [
                    "Develop a financial planning app for small businesses",
                    "Create a pricing optimization tool for e-commerce"
                ],
                "case_study": "How a South African tech startup used algebraic models to optimize their pricing strategy and increase revenue by 30%."
            },
            "Statistics": {
                "description": "Statistics enables data-driven decision making, market research analysis, and performance tracking.",
                "business_applications": [
                    "Analyzing market trends",
                    "A/B testing for product features",
                    "Customer segmentation"
                ],
                "startup_ideas": [
                    "Create a market research tool for African entrepreneurs",
                    "Develop a data visualization platform for business insights"
                ],
                "case_study": "How a Johannesburg-based startup used statistical analysis to identify an underserved market segment and built a successful business."
            },
            "Calculus": {
                "description": "Calculus helps optimize business processes, maximize profits, and model complex business systems.",
                "business_applications": [
                    "Optimizing production processes",
                    "Maximizing profit functions",
                    "Resource allocation"
                ],
                "startup_ideas": [
                    "Develop an optimization tool for manufacturing businesses",
                    "Create a resource planning application for small businesses"
                ],
                "case_study": "How a Cape Town engineering startup used calculus to optimize their production line and reduce costs by 25%."
            },
            "Geometry": {
                "description": "Geometry is valuable in design, spatial planning, and logistics optimization.",
                "business_applications": [
                    "Store layout optimization",
                    "Efficient packaging design",
                    "Delivery route planning"
                ],
                "startup_ideas": [
                    "Create a space planning app for retail businesses",
                    "Develop a logistics optimization tool for delivery services"
                ],
                "case_study": "How a Durban logistics startup used geometric principles to optimize delivery routes and save 40% on fuel costs."
            },
            "Probability": {
                "description": "Probability helps with risk assessment, decision making under uncertainty, and forecasting.",
                "business_applications": [
                    "Risk analysis for business decisions",
                    "Insurance pricing models",
                    "Inventory management"
                ],
                "startup_ideas": [
                    "Develop a risk assessment tool for small businesses",
                    "Create a predictive inventory management system"
                ],
                "case_study": "How a financial services startup in Pretoria used probability models to create innovative insurance products for underserved markets."
            }
        }
        
        # Default connection for topics not specifically listed
        default_connection = {
            "description": "Mathematics is fundamental to business planning, financial management, and data-driven decision making.",
            "business_applications": [
                "Financial planning and analysis",
                "Operational optimization",
                "Data-driven decision making"
            ],
            "startup_ideas": [
                "Develop tools that solve mathematical problems in business contexts",
                "Create educational resources that teach math through entrepreneurship"
            ],
            "case_study": "How successful South African entrepreneurs use mathematical thinking to build sustainable businesses."
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
            connection["grade_context"] = "Even at this early stage, understanding basic math helps in managing a small business like a lemonade stand or craft sale."
        elif grade_level <= 9:
            connection["grade_context"] = "At this grade level, you can start applying these concepts to plan and run small business projects in your community."
        else:
            connection["grade_context"] = "With these advanced mathematical skills, you're equipped to develop business plans and financial models for real startup ventures."
        
        # Add topic and grade level to the result
        connection["topic"] = topic
        connection["grade_level"] = grade_level
        
        return connection
