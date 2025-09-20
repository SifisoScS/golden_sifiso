// Main JavaScript file for The Golden Hand application

document.addEventListener('DOMContentLoaded', function() {
    // Add logo animation
    const logo = document.querySelector('header img');
    if (logo) {
        logo.classList.add('logo-animate');
    }

    // Add scroll animations
    const sections = document.querySelectorAll('section');
    if (sections.length > 0) {
        const observerOptions = {
            root: null,
            rootMargin: '0px',
            threshold: 0.1
        };

        const sectionObserver = new IntersectionObserver(function(entries, observer) {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('fade-in');
                    observer.unobserve(entry.target);
                }
            });
        }, observerOptions);

        sections.forEach(section => {
            section.style.opacity = '0';
            sectionObserver.observe(section);
        });
    }

    // Mobile menu toggle
    const menuBtn = document.getElementById('menu-btn');
    const mobileMenu = document.getElementById('mobile-menu');
    if (menuBtn && mobileMenu) {
        menuBtn.addEventListener('click', () => {
            mobileMenu.classList.toggle('hidden');
        });
    }

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 80,
                    behavior: 'smooth'
                });
                
                // Close mobile menu if open
                if (mobileMenu && !mobileMenu.classList.contains('hidden')) {
                    mobileMenu.classList.add('hidden');
                }
            }
        });
    });

    // Add card hover effects
    const cards = document.querySelectorAll('.dashboard-card, .quiz-option, .community-post');
    cards.forEach(card => {
        card.classList.add('card-hover');
    });

    // Initialize progress bars
    initializeProgressBars();

    // Initialize accessibility toggles
    initializeAccessibilityToggles();

    // Initialize quiz functionality if on quiz page
    if (document.querySelector('.quiz-container')) {
        initializeQuiz();
    }

    // Initialize audio player if on audio page
    if (document.querySelector('.audio-player')) {
        initializeAudioPlayer();
    }
});

// Progress bar initialization
function initializeProgressBars() {
    const progressBars = document.querySelectorAll('.progress-bar');
    progressBars.forEach(bar => {
        const fill = bar.querySelector('.progress-bar-fill');
        if (fill) {
            const percentage = fill.getAttribute('data-percentage') || '0';
            fill.style.width = `${percentage}%`;
        }
    });
}

// Accessibility toggles
function initializeAccessibilityToggles() {
    const contrastToggle = document.getElementById('contrast-toggle');
    const textSizeToggle = document.getElementById('text-size-toggle');
    
    if (contrastToggle) {
        contrastToggle.addEventListener('click', function() {
            document.body.classList.toggle('high-contrast');
            localStorage.setItem('high-contrast', document.body.classList.contains('high-contrast'));
        });
        
        // Check saved preference
        if (localStorage.getItem('high-contrast') === 'true') {
            document.body.classList.add('high-contrast');
        }
    }
    
    if (textSizeToggle) {
        textSizeToggle.addEventListener('click', function() {
            document.body.classList.toggle('large-text');
            localStorage.setItem('large-text', document.body.classList.contains('large-text'));
        });
        
        // Check saved preference
        if (localStorage.getItem('large-text') === 'true') {
            document.body.classList.add('large-text');
        }
    }
}

// Quiz functionality
function initializeQuiz() {
    const quizOptions = document.querySelectorAll('.quiz-option');
    const submitButton = document.querySelector('.quiz-submit');
    
    quizOptions.forEach(option => {
        option.addEventListener('click', function() {
            // Deselect all options in the same question
            const questionId = this.getAttribute('data-question');
            document.querySelectorAll(`.quiz-option[data-question="${questionId}"]`).forEach(opt => {
                opt.classList.remove('selected');
            });
            
            // Select this option
            this.classList.add('selected');
        });
    });
    
    if (submitButton) {
        submitButton.addEventListener('click', function() {
            // Collect selected answers
            const answers = {};
            document.querySelectorAll('.quiz-option.selected').forEach(selected => {
                const questionId = selected.getAttribute('data-question');
                const optionId = selected.getAttribute('data-option');
                answers[questionId] = optionId;
            });
            
            // Submit answers via fetch API
            fetch('/quiz/submit', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ answers }),
            })
            .then(response => response.json())
            .then(data => {
                // Handle response (e.g., show results)
                if (data.redirect) {
                    window.location.href = data.redirect;
                }
            })
            .catch(error => {
                console.error('Error submitting quiz:', error);
            });
        });
    }
}

// Audio player functionality
function initializeAudioPlayer() {
    const audioPlayers = document.querySelectorAll('.audio-player');
    
    audioPlayers.forEach(player => {
        const audio = player.querySelector('audio');
        const playButton = player.querySelector('.play-button');
        const pauseButton = player.querySelector('.pause-button');
        const progressBar = player.querySelector('.audio-progress');
        const currentTime = player.querySelector('.current-time');
        const duration = player.querySelector('.duration');
        
        if (audio && playButton && pauseButton) {
            playButton.addEventListener('click', () => {
                audio.play();
                playButton.classList.add('hidden');
                pauseButton.classList.remove('hidden');
            });
            
            pauseButton.addEventListener('click', () => {
                audio.pause();
                pauseButton.classList.add('hidden');
                playButton.classList.remove('hidden');
            });
            
            audio.addEventListener('timeupdate', () => {
                if (progressBar) {
                    const percentage = (audio.currentTime / audio.duration) * 100;
                    progressBar.style.width = `${percentage}%`;
                }
                
                if (currentTime) {
                    currentTime.textContent = formatTime(audio.currentTime);
                }
            });
            
            audio.addEventListener('loadedmetadata', () => {
                if (duration) {
                    duration.textContent = formatTime(audio.duration);
                }
            });
            
            // Track audio progress for offline learning
            audio.addEventListener('ended', () => {
                // Send completion status to server
                const audioId = player.getAttribute('data-audio-id');
                if (audioId) {
                    fetch(`/audio/${audioId}/complete`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        }
                    });
                }
                
                playButton.classList.remove('hidden');
                pauseButton.classList.add('hidden');
            });
        }
    });
}

// Helper function to format time in MM:SS
function formatTime(seconds) {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = Math.floor(seconds % 60);
    return `${minutes}:${remainingSeconds < 10 ? '0' : ''}${remainingSeconds}`;
}

// Startup idea generator for the iKhaya AI section
function generateStartupIdea() {
    const industries = [
        'Agriculture', 'Education', 'Healthcare', 'Transportation', 
        'Finance', 'Retail', 'Energy', 'Entertainment', 'Tourism'
    ];
    
    const technologies = [
        'AI', 'Blockchain', 'Mobile Apps', 'IoT', 
        'Renewable Energy', 'Robotics', 'AR/VR', 'Data Analytics'
    ];
    
    const problems = [
        'accessibility', 'affordability', 'efficiency', 'sustainability',
        'education', 'healthcare', 'financial inclusion', 'food security'
    ];
    
    const randomIndustry = industries[Math.floor(Math.random() * industries.length)];
    const randomTech = technologies[Math.floor(Math.random() * technologies.length)];
    const randomProblem = problems[Math.floor(Math.random() * problems.length)];
    
    const ideaElement = document.getElementById('startup-idea');
    if (ideaElement) {
        ideaElement.textContent = `A ${randomTech} solution for ${randomProblem} in the ${randomIndustry} sector`;
        ideaElement.classList.add('slide-up');
        
        // Remove animation class after animation completes
        setTimeout(() => {
            ideaElement.classList.remove('slide-up');
        }, 500);
    }
}

// Initialize dashboard widgets if on dashboard page
function initializeDashboard() {
    const progressCharts = document.querySelectorAll('.progress-chart');
    if (progressCharts.length > 0) {
        // Simple chart rendering using canvas
        progressCharts.forEach(chart => {
            const canvas = chart.querySelector('canvas');
            if (canvas) {
                const ctx = canvas.getContext('2d');
                const data = JSON.parse(chart.getAttribute('data-values') || '[]');
                const labels = JSON.parse(chart.getAttribute('data-labels') || '[]');
                
                if (data.length > 0 && ctx) {
                    // Simple bar chart
                    const barWidth = canvas.width / data.length;
                    const maxValue = Math.max(...data);
                    
                    ctx.clearRect(0, 0, canvas.width, canvas.height);
                    
                    data.forEach((value, index) => {
                        const barHeight = (value / maxValue) * (canvas.height - 30);
                        
                        ctx.fillStyle = '#ca8a04';
                        ctx.fillRect(
                            index * barWidth + 10, 
                            canvas.height - barHeight - 20, 
                            barWidth - 20, 
                            barHeight
                        );
                        
                        ctx.fillStyle = '#1f2937';
                        ctx.font = '10px Arial';
                        ctx.textAlign = 'center';
                        ctx.fillText(
                            labels[index] || '', 
                            index * barWidth + barWidth / 2, 
                            canvas.height - 5
                        );
                    });
                }
            }
        });
    }
}
