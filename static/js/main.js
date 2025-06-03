document.addEventListener('DOMContentLoaded', function() {
    // View toggle functionality
    const gridViewBtn = document.getElementById('gridView');
    const listViewBtn = document.getElementById('listView');
    const resultsContainer = document.getElementById('results');

    if (gridViewBtn && listViewBtn) {
        gridViewBtn.addEventListener('click', () => {
            resultsContainer.classList.remove('results-list');
            resultsContainer.classList.add('results-grid');
            gridViewBtn.classList.add('active');
            listViewBtn.classList.remove('active');
            localStorage.setItem('viewPreference', 'grid');
        });

        listViewBtn.addEventListener('click', () => {
            resultsContainer.classList.remove('results-grid');
            resultsContainer.classList.add('results-list');
            listViewBtn.classList.add('active');
            gridViewBtn.classList.remove('active');
            localStorage.setItem('viewPreference', 'list');
        });

        // Load user's preference
        const viewPreference = localStorage.getItem('viewPreference') || 'grid';
        if (viewPreference === 'grid') {
            gridViewBtn.click();
        } else {
            listViewBtn.click();
        }
    }

    // Theme toggle functionality
    const themeToggle = document.getElementById('themeToggle');
    if (themeToggle) {
        // Check for saved theme preference or system preference
        const savedTheme = localStorage.getItem('theme');
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        
        // Set initial theme
        if (savedTheme === 'dark' || (!savedTheme && prefersDark)) {
            document.documentElement.setAttribute('data-theme', 'dark');
            themeToggle.checked = true;
        }

        // Handle theme toggle
        themeToggle.addEventListener('change', function() {
            if (this.checked) {
                document.documentElement.setAttribute('data-theme', 'dark');
                localStorage.setItem('theme', 'dark');
            } else {
                document.documentElement.setAttribute('data-theme', 'light');
                localStorage.setItem('theme', 'light');
            }
        });
    }

    // Character counter initialization
    const initCharacterCounter = (() => {
        let initialized = false;
        
        return () => {
            if (initialized) return;
            
            const questionTextarea = document.getElementById('question');
            const charCounter = document.querySelector('.char-counter span');
            
            if (questionTextarea && charCounter) {
                const maxLength = parseInt(questionTextarea.getAttribute('maxlength')) || 2000;
                
                const updateCharCount = () => {
                    const count = questionTextarea.value.length;
                    charCounter.textContent = count;
                    
                    // Visual feedback when approaching/exceeding limit
                    if (count > (maxLength * 0.9)) {
                        charCounter.parentElement.classList.add('warning');
                    } else {
                        charCounter.parentElement.classList.remove('warning');
                    }
                };

                // Update on input
                questionTextarea.addEventListener('input', updateCharCount);
                
                // Initial count update
                updateCharCount();
                
                initialized = true;
            }
        };
    })();

    // Initialize character counter
    initCharacterCounter();

    // Initialize history manager
    window.historyManager = {
        getHistory: function() {
            return JSON.parse(localStorage.getItem('questionHistory') || '[]');
        },
        
        saveHistory: function(history) {
            localStorage.setItem('questionHistory', JSON.stringify(history));
        },
        
        addQuestion: function(question, responses = null) {
            const history = this.getHistory();
            const timestamp = new Date().toLocaleString();
            
            history.unshift({
                question: question,
                timestamp: timestamp,
                responses: responses,
                sessionId: new Date().getTime()
            });
            
            // Keep only last 50 questions
            if (history.length > 50) {
                history.pop();
            }
            
            this.saveHistory(history);
            this.displayHistory();
        },
        
        displayHistory: function() {
            const historyContent = document.querySelector('.history-content');
            const template = document.getElementById('history-item-template');
            const history = this.getHistory();
            
            if (!historyContent || !template) return;
            
            historyContent.innerHTML = '';
            
            history.forEach(item => {
                const clone = template.content.cloneNode(true);
                const historyItem = clone.querySelector('.history-item');
                
                historyItem.querySelector('.question-text').textContent = item.question;
                historyItem.querySelector('.timestamp').textContent = item.timestamp;
                
                // Setup reuse question button
                historyItem.querySelector('.reuse-question').addEventListener('click', () => {
                    window.location.href = `/?question=${encodeURIComponent(item.question)}`;
                });
                
                // Setup view responses button
                historyItem.querySelector('.view-responses').addEventListener('click', () => {
                    if (item.responses) {
                        // Store the responses in sessionStorage for viewing
                        sessionStorage.setItem('viewResponses', JSON.stringify({
                            question: item.question,
                            timestamp: item.timestamp,
                            responses: item.responses
                        }));
                        window.location.href = `/view-responses/${item.sessionId}`;
                    }
                });
                
                historyContent.appendChild(historyItem);
            });
        }
    };

    // Save question when form is submitted
    const form = document.getElementById('questionForm');
    if (form) {
        form.addEventListener('submit', function(e) {
            const selectedAIs = document.querySelectorAll('input[name="ai_models"]:checked');
            if (selectedAIs.length === 0) {
                e.preventDefault();
                alert('Please select at least one AI model');
                return;
            }

            const question = document.getElementById('question').value.trim();
            if (!question) {
                e.preventDefault();
                alert('Please enter a question');
                return;
            }

            // Save to history
            window.historyManager.addQuestion(question);
        });
    }

    // Save AI model selections
    const aiCheckboxes = document.querySelectorAll('input[name="ai_models"]');
    aiCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            const selectedModels = Array.from(aiCheckboxes)
                .filter(cb => cb.checked)
                .map(cb => cb.value);
            localStorage.setItem('selectedAIModels', JSON.stringify(selectedModels));
        });
    });

    // Load saved AI model selections
    const savedModels = JSON.parse(localStorage.getItem('selectedAIModels') || '[]');
    aiCheckboxes.forEach(checkbox => {
        if (savedModels.includes(checkbox.value)) {
            checkbox.checked = true;
        }
    });

    // History Panel Toggle
    const historyBtn = document.getElementById('historyToggleBtn');
    const historyPanel = document.querySelector('.history-panel');
    const closeHistoryBtn = document.querySelector('.close-history');

    if (historyBtn && historyPanel) {
        historyBtn.addEventListener('click', () => {
            historyPanel.classList.toggle('active');
            historyBtn.classList.toggle('active');
            window.historyManager.displayHistory(); // Refresh history when panel is opened
        });

        if (closeHistoryBtn) {
            closeHistoryBtn.addEventListener('click', () => {
                historyPanel.classList.remove('active');
                historyBtn.classList.remove('active');
            });
        }

        // Close history panel when clicking outside
        document.addEventListener('click', (e) => {
            if (!historyPanel.contains(e.target) && !historyBtn.contains(e.target) && historyPanel.classList.contains('active')) {
                historyPanel.classList.remove('active');
                historyBtn.classList.remove('active');
            }
        });
    }

    // Initialize history display
    window.historyManager.displayHistory();
}); 