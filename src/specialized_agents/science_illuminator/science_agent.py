"""
Science Illuminator Agent for The Golden Hand Learning Platform.

This module implements a specialized agent for science education,
providing personalized learning paths, content generation, and performance analysis
for science topics.
"""

from typing import Dict, List, Any, Optional, Tuple
from src.specialized_agents.base_agent import BaseAgent, ContentType, LearningLevel


class ScienceAgent(BaseAgent):
    """
    Specialized agent for science education.
    
    This agent provides science-specific learning resources, content generation,
    and performance analysis to support students in developing scientific knowledge
    with a focus on practical applications and entrepreneurship.
    """
    
    def __init__(self, name: str = "Science Illuminator", 
                description: str = "Specialized agent for science education"):
        """
        Initialize the Science Illuminator agent.
        
        Args:
            name: The name of the agent
            description: A brief description of the agent's capabilities
        """
        super().__init__(name, description)
        self.topics_by_grade = self._initialize_topics()
        
    def _initialize_topics(self) -> Dict[int, List[str]]:
        """
        Initialize the science topics by grade level.
        
        Returns:
            Dictionary mapping grade levels to lists of topics
        """
        return {
            1: ["Plants and Animals", "Weather", "The Five Senses", "Earth and Space"],
            2: ["Life Cycles", "States of Matter", "Habitats", "Simple Machines"],
            3: ["Animal Adaptations", "Forces and Motion", "Solar System", "Ecosystems"],
            4: ["Energy", "Human Body Systems", "Earth's Processes", "Classification"],
            5: ["Matter and Mixtures", "Ecosystems", "Weather and Climate", "Space Exploration"],
            6: ["Cells", "Forces and Motion", "Earth's Structure", "Energy Transformations"],
            7: ["Human Body Systems", "Chemical Reactions", "Weather and Climate", "Ecology"],
            8: ["Genetics", "Chemistry Fundamentals", "Earth's History", "Waves and Energy"],
            9: ["Biology: Cells and Systems", "Chemistry: Atomic Structure", "Physics: Motion and Forces", "Earth Science: Geology"],
            10: ["Biology: Genetics and Evolution", "Chemistry: Chemical Reactions", "Physics: Energy", "Environmental Science"],
            11: ["Biology: Physiology", "Chemistry: Organic Chemistry", "Physics: Electricity and Magnetism", "Earth Science: Climate"],
            12: ["Advanced Biology", "Advanced Chemistry", "Advanced Physics", "Scientific Research Methods"]
        }
    
    def generate_learning_path(self, 
                              student_id: int, 
                              grade_level: int, 
                              prior_knowledge: Dict[str, float] = None) -> List[Dict[str, Any]]:
        """
        Generate a personalized science learning path for a student.
        
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
            
            # Add laboratory activity for science
            learning_path.append({
                "type": "activity",
                "content_type": "laboratory",
                "topic": topic,
                "difficulty": difficulty.value,
                "title": f"{topic} Laboratory",
                "description": f"Conduct experiments related to {topic}",
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
            "topic": "Science Integration",
            "difficulty": LearningLevel.INTERMEDIATE.value,
            "title": f"Grade {grade_level} Science Project",
            "description": "Apply scientific concepts you've learned in a real-world project",
            "estimated_time_minutes": 90
        })
        
        return learning_path
    
    def generate_content(self, 
                        topic: str, 
                        content_type: ContentType, 
                        difficulty: LearningLevel, 
                        grade_level: int) -> Dict[str, Any]:
        """
        Generate science content for a given topic.
        
        Args:
            topic: The specific science topic to generate content for
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
            "created_at": "2025-05-21T06:18:00Z"
        }
        
        # Generate content based on type
        if content_type == ContentType.LESSON:
            content.update({
                "introduction": f"Welcome to this science lesson on {topic}. We'll explore key concepts, conduct experiments, and discover real-world applications.",
                "objectives": [
                    f"Understand the fundamental principles of {topic}",
                    f"Learn how to apply the scientific method to {topic}",
                    f"Connect {topic} to real-world applications and entrepreneurship"
                ],
                "sections": [
                    {
                        "title": "Key Concepts",
                        "content": f"This section covers the key scientific concepts of {topic}...",
                        "illustrations": [
                            {"caption": "Diagram illustrating key concept", "image_url": "#"}
                        ]
                    },
                    {
                        "title": "Scientific Method Application",
                        "content": f"Here's how the scientific method is applied to {topic}...",
                        "steps": [
                            "1. Ask a question about an observation",
                            "2. Form a hypothesis",
                            "3. Make a prediction based on the hypothesis",
                            "4. Test the prediction",
                            "5. Analyze the results and draw conclusions"
                        ]
                    },
                    {
                        "title": "Real-World Applications",
                        "content": f"Here's how {topic} is applied in real-world situations...",
                        "examples": [
                            {"application": "Medical field application", "description": "How this concept is used in medicine"},
                            {"application": "Environmental application", "description": "How this concept is used in environmental science"}
                        ]
                    },
                    {
                        "title": "Entrepreneurship Connection",
                        "content": f"Here's how {topic} can lead to business opportunities...",
                        "examples": [
                            {"business_opportunity": "Innovation in renewable energy", "scientific_basis": "Application of energy principles"}
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
                "instructions": f"Practice the following {topic} problems. Apply scientific thinking and show your work.",
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
                "title": f"{topic} Project: Scientific Innovation",
                "description": f"Apply your knowledge of {topic} to develop an innovative solution to a real-world problem.",
                "objectives": [
                    "Apply scientific concepts to a practical challenge",
                    "Develop research and experimentation skills",
                    "Connect science to entrepreneurship and innovation"
                ],
                "scenario": f"South Africa faces challenges in areas like water conservation, renewable energy, and healthcare. Use your knowledge of {topic} to develop a solution to one of these challenges...",
                "tasks": [
                    {"description": "Task 1: Identify a problem related to the topic", "deliverable": "Problem statement"},
                    {"description": "Task 2: Research existing solutions", "deliverable": "Research summary"},
                    {"description": "Task 3: Design your scientific solution", "deliverable": "Solution design"},
                    {"description": "Task 4: Create a prototype or model", "deliverable": "Prototype/model"},
                    {"description": "Task 5: Test and refine your solution", "deliverable": "Test results"},
                    {"description": "Task 6: Develop a business case", "deliverable": "Business plan"}
                ],
                "resources": [
                    {"name": "Project guide", "type": "document", "url": "#"},
                    {"name": "Scientific method template", "type": "document", "url": "#"},
                    {"name": "Business plan template", "type": "document", "url": "#"}
                ],
                "rubric": [
                    {"criterion": "Scientific accuracy", "weight": 25},
                    {"criterion": "Innovation and creativity", "weight": 20},
                    {"criterion": "Practical application", "weight": 25},
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
                        "name": "Short Answer",
                        "questions": [
                            {"id": "sa_1", "text": "Sample short answer question 1", "answer": "Sample answer 1"},
                            {"id": "sa_2", "text": "Sample short answer question 2", "answer": "Sample answer 2"}
                        ]
                    },
                    {
                        "name": "Practical Application",
                        "questions": [
                            {"id": "pa_1", "text": "Describe how you would apply the scientific method to solve a real-world problem related to this topic.", "answer": "Sample answer with scientific method steps"}
                        ]
                    }
                ],
                "time_limit_minutes": 45,
                "total_points": 100
            })
        
        # Special case for laboratory content
        elif str(content_type.value).lower() == "laboratory" or content_type.value == "laboratory":
            content.update({
                "content_type": "laboratory",
                "title": f"{topic} Laboratory Investigation",
                "introduction": f"In this laboratory activity, you will conduct experiments related to {topic}.",
                "safety_guidelines": [
                    "Always wear safety goggles when handling chemicals",
                    "Follow all instructions carefully",
                    "Report any spills or accidents immediately"
                ],
                "materials": [
                    "List of required materials for the experiment",
                    "Additional equipment needed"
                ],
                "procedure": [
                    "Step 1: Detailed instructions for the first step",
                    "Step 2: Detailed instructions for the second step",
                    "Step 3: Detailed instructions for the third step"
                ],
                "observations": {
                    "instructions": "Record your observations in the provided table",
                    "table_headers": ["Trial", "Measurement 1", "Measurement 2", "Observations"]
                },
                "analysis_questions": [
                    "What patterns did you observe in your data?",
                    "How do your results relate to the scientific concepts discussed in class?",
                    "What sources of error might have affected your results?"
                ],
                "conclusion": "Write a conclusion summarizing your findings and how they relate to the scientific concepts of this topic.",
                "extension": "Design a follow-up experiment that would further explore this topic."
            })
        
        return content
    
    def analyze_performance(self, 
                           student_id: int, 
                           activity_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze a student's science performance and provide feedback.
        
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
            next_steps = ["Explore advanced concepts in this topic", "Consider a related science project"]
        elif percentage >= 75:
            performance_level = "Good"
            next_steps = ["Review specific areas of difficulty", "Try additional experiments"]
        elif percentage >= 60:
            performance_level = "Satisfactory"
            next_steps = ["Focus on areas of weakness", "Review core scientific concepts"]
        else:
            performance_level = "Needs Improvement"
            next_steps = ["Revisit fundamental concepts", "Work with simpler experiments first"]
        
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
        
        # Add scientific thinking assessment
        if activity_type in ["laboratory", "project"]:
            analysis["scientific_thinking"] = {
                "hypothesis_formation": 4,  # Scale of 1-5
                "experimental_design": 3,
                "data_analysis": 4,
                "conclusion_drawing": 3,
                "overall": 3.5,
                "feedback": "You show good skills in hypothesis formation and data analysis. Work on improving your experimental design and conclusion drawing."
            }
        
        # Add entrepreneurship connection
        analysis["entrepreneurship_connection"] = self.get_entrepreneurship_connection(topic, 10)
        
        return analysis
    
    def answer_question(self, 
                       question: str, 
                       context: Dict[str, Any] = None) -> Tuple[str, float]:
        """
        Answer a science question from a student.
        
        Args:
            question: The question text
            context: Additional context about the question
            
        Returns:
            A tuple containing (answer, confidence_score)
        """
        # This is a simplified implementation
        # In a real system, this would use more sophisticated NLP and science knowledge
        
        # Default context
        if context is None:
            context = {}
        
        # Extract topic from context if available
        topic = context.get("topic", "unknown")
        grade_level = context.get("grade_level", 10)
        
        # Simple keyword matching for demonstration
        keywords = question.lower().split()
        
        # Check for question types
        if any(word in keywords for word in ["scientific", "method", "experiment"]):
            answer = "The scientific method is a process for experimentation used to explore observations and answer questions. It involves making observations, forming a hypothesis, conducting experiments, analyzing data, and drawing conclusions."
            confidence = 0.9
        elif any(word in keywords for word in ["biology", "cell", "organism"]):
            answer = "Biology is the study of living organisms. Cells are the basic structural and functional units of all living organisms. They contain organelles that perform specific functions to keep the cell alive."
            confidence = 0.85
        elif any(word in keywords for word in ["chemistry", "element", "compound", "reaction"]):
            answer = "Chemistry is the study of matter, its properties, and the changes it undergoes. Elements are pure substances that cannot be broken down further by chemical means. Compounds are substances made up of two or more elements chemically combined."
            confidence = 0.85
        elif any(word in keywords for word in ["physics", "force", "motion", "energy"]):
            answer = "Physics is the study of matter, energy, and the interactions between them. Forces cause objects to accelerate, and energy is the capacity to do work or cause change."
            confidence = 0.85
        elif any(word in keywords for word in ["earth", "geology", "climate"]):
            answer = "Earth science studies the planet's physical characteristics, atmosphere, and surrounding space. It includes geology (study of Earth's structure), meteorology (study of weather), and oceanography (study of oceans)."
            confidence = 0.8
        elif any(word in keywords for word in ["business", "entrepreneur", "startup"]):
            # Get entrepreneurship connection
            connection = self.get_entrepreneurship_connection(topic, grade_level)
            answer = connection.get("description", "Science is essential for innovation and developing solutions to real-world problems, which can lead to business opportunities.")
            confidence = 0.7
        else:
            answer = "I'm not sure about the answer to this specific science question. Could you provide more details or rephrase it?"
            confidence = 0.3
        
        return answer, confidence
    
    def suggest_resources(self, 
                         topic: str, 
                         learning_style: str = None, 
                         difficulty: LearningLevel = None) -> List[Dict[str, Any]]:
        """
        Suggest science resources for further learning.
        
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
                "title": "Khan Academy Science",
                "description": f"Free online lessons and exercises on {topic}",
                "url": "https://www.khanacademy.org/science",
                "type": "interactive",
                "difficulty": LearningLevel.BEGINNER.value
            },
            {
                "title": "PhET Interactive Simulations",
                "description": "Interactive science simulations that make learning fun",
                "url": "https://phet.colorado.edu/",
                "type": "simulation",
                "difficulty": LearningLevel.INTERMEDIATE.value
            },
            {
                "title": "Science and Entrepreneurship",
                "description": "Learn how scientific discoveries lead to business innovations",
                "url": "#",
                "type": "course",
                "difficulty": LearningLevel.INTERMEDIATE.value
            }
        ]
        
        # Add resources based on learning style if specified
        if learning_style == "visual":
            resources.append({
                "title": "Visual Science",
                "description": f"Visual explanations of {topic} with interactive diagrams",
                "url": "#",
                "type": "interactive",
                "difficulty": difficulty.value
            })
        elif learning_style == "auditory":
            resources.append({
                "title": f"{topic} Explained - Science Podcast",
                "description": f"Audio explanations of {topic} concepts",
                "url": "#",
                "type": "audio",
                "difficulty": difficulty.value
            })
        elif learning_style == "kinesthetic":
            resources.append({
                "title": f"Hands-on {topic} Experiments",
                "description": f"Physical experiments and activities to learn {topic}",
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
        
        # Add South African context resource
        resources.append({
            "title": f"{topic} in South African Context",
            "description": f"Learn how {topic} is applied in South African research and industry",
            "url": "#",
            "type": "article",
            "difficulty": difficulty.value
        })
        
        # Add entrepreneurship-focused resource
        resources.append({
            "title": f"From Science to Startup: {topic} Applications",
            "description": f"Learn how {topic} can be applied to create innovative business solutions",
            "url": "#",
            "type": "course",
            "difficulty": difficulty.value,
            "tags": ["entrepreneurship", "innovation", "application"]
        })
        
        return resources
    
    def get_entrepreneurship_connection(self, 
                                       topic: str, 
                                       grade_level: int) -> Dict[str, Any]:
        """
        Connect science topics to entrepreneurship opportunities.
        
        Args:
            topic: The academic topic to connect to entrepreneurship
            grade_level: The student's grade level
            
        Returns:
            Information connecting the topic to business opportunities
        """
        # Define connections between science topics and entrepreneurship
        entrepreneurship_connections = {
            "Biology": {
                "description": "Biology knowledge can lead to innovations in healthcare, agriculture, and biotechnology.",
                "business_applications": [
                    "Developing healthcare solutions",
                    "Creating sustainable agricultural practices",
                    "Biotechnology innovations"
                ],
                "startup_ideas": [
                    "Develop a mobile health monitoring app",
                    "Create sustainable farming solutions for urban areas",
                    "Design biodegradable packaging from local materials"
                ],
                "case_study": "How a South African biotech startup developed drought-resistant crop varieties to help local farmers increase yields by 40%."
            },
            "Chemistry": {
                "description": "Chemistry enables the development of new materials, pharmaceuticals, and sustainable products.",
                "business_applications": [
                    "Creating eco-friendly products",
                    "Developing new materials",
                    "Improving manufacturing processes"
                ],
                "startup_ideas": [
                    "Develop affordable water purification solutions",
                    "Create natural cosmetics using indigenous plants",
                    "Design sustainable cleaning products"
                ],
                "case_study": "How a Cape Town startup used green chemistry to develop affordable water filtration systems for rural communities."
            },
            "Physics": {
                "description": "Physics knowledge can lead to innovations in energy, transportation, and technology.",
                "business_applications": [
                    "Renewable energy solutions",
                    "Efficient transportation systems",
                    "Sensor and measurement technologies"
                ],
                "startup_ideas": [
                    "Create affordable solar energy solutions for off-grid communities",
                    "Develop energy-efficient transportation for urban areas",
                    "Design low-cost scientific instruments for schools"
                ],
                "case_study": "How a Johannesburg-based startup applied physics principles to develop low-cost solar water heaters, creating jobs and reducing energy costs."
            },
            "Environmental Science": {
                "description": "Environmental science knowledge can lead to solutions for sustainability, conservation, and resource management.",
                "business_applications": [
                    "Waste management solutions",
                    "Conservation technologies",
                    "Sustainable resource management"
                ],
                "startup_ideas": [
                    "Create a waste recycling business",
                    "Develop eco-tourism experiences",
                    "Design water conservation systems for homes and businesses"
                ],
                "case_study": "How a Durban entrepreneur turned plastic waste into building materials, addressing both environmental issues and housing needs."
            }
        }
        
        # Default connection for topics not specifically listed
        default_connection = {
            "description": "Scientific knowledge is the foundation for innovation and solving real-world problems, which can lead to business opportunities.",
            "business_applications": [
                "Developing innovative products",
                "Creating efficient processes",
                "Solving community challenges"
            ],
            "startup_ideas": [
                "Identify a local problem that can be solved with scientific knowledge",
                "Develop educational resources that make science accessible"
            ],
            "case_study": "How South African entrepreneurs use scientific thinking to build innovative solutions to local challenges."
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
            connection["grade_context"] = "Even at this early stage, understanding science helps you identify problems that could be solved with simple innovations."
        elif grade_level <= 9:
            connection["grade_context"] = "At this grade level, you can start applying scientific knowledge to develop solutions for community challenges."
        else:
            connection["grade_context"] = "With these advanced scientific skills, you're equipped to develop innovative solutions that could form the basis of a startup."
        
        # Add topic and grade level to the result
        connection["topic"] = topic
        connection["grade_level"] = grade_level
        
        return connection
