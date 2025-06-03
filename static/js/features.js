// Toast Notification System
class ToastManager {
    constructor() {
        this.container = document.createElement('div');
        this.container.className = 'toast-container';
        document.body.appendChild(this.container);
    }

    show(message, type = 'info') {
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        toast.textContent = message;
        this.container.appendChild(toast);

        setTimeout(() => {
            toast.remove();
        }, 3000);
    }
}

// Dark Mode Manager
class ThemeManager {
    constructor() {
        this.theme = localStorage.getItem('theme') || 'light';
        this.applyTheme();
        this.setupToggle();
    }

    applyTheme() {
        document.documentElement.setAttribute('data-theme', this.theme);
        document.body.classList.add('theme-transition');
    }

    setupToggle() {
        const toggle = document.getElementById('themeToggle');
        if (toggle) {
            toggle.checked = this.theme === 'dark';
            toggle.addEventListener('change', () => {
                this.theme = toggle.checked ? 'dark' : 'light';
                localStorage.setItem('theme', this.theme);
                this.applyTheme();
            });
        }
    }
}

// Character Counter
class CharacterCounter {
    constructor(textareaId, limit = 1000) {
        this.textarea = document.getElementById(textareaId);
        this.limit = limit;
        if (this.textarea) {
            this.setup();
        }
    }

    setup() {
        const counter = document.createElement('div');
        counter.className = 'character-counter';
        this.textarea.parentNode.appendChild(counter);

        this.textarea.addEventListener('input', () => {
            const count = this.textarea.value.length;
            counter.textContent = `${count}/${this.limit} characters`;
            if (count > this.limit) {
                counter.style.color = '#EF4444';
            } else {
                counter.style.color = '';
            }
        });
    }
}

// History Manager
class HistoryManager {
    constructor() {
        this.history = JSON.parse(localStorage.getItem('questionHistory') || '[]');
        this.setupPanel();
    }

    setupPanel() {
        const panel = document.createElement('div');
        panel.className = 'history-panel';
        panel.innerHTML = `
            <div class="p-4">
                <h3>Question History</h3>
                <div id="historyList"></div>
            </div>
        `;
        document.body.appendChild(panel);

        const toggleBtn = document.getElementById('historyToggle');
        if (toggleBtn) {
            toggleBtn.addEventListener('click', () => {
                panel.classList.toggle('active');
            });
        }

        this.updateHistoryList();
    }

    addQuestion(question, responses) {
        this.history.unshift({
            question,
            responses,
            timestamp: new Date().toISOString()
        });
        localStorage.setItem('questionHistory', JSON.stringify(this.history.slice(0, 50)));
        this.updateHistoryList();
    }

    updateHistoryList() {
        const list = document.getElementById('historyList');
        if (list) {
            list.innerHTML = this.history.map(item => `
                <div class="history-item p-2 border-b">
                    <p class="font-bold">${item.question}</p>
                    <small>${new Date(item.timestamp).toLocaleString()}</small>
                </div>
            `).join('');
        }
    }
}

// Response Manager
class ResponseManager {
    constructor() {
        this.setupCopyButtons();
        this.setupVoting();
        this.setupSharing();
    }

    setupCopyButtons() {
        document.querySelectorAll('.ai-response').forEach(response => {
            const copyBtn = document.createElement('button');
            copyBtn.className = 'copy-button';
            copyBtn.innerHTML = '📋';
            copyBtn.addEventListener('click', () => this.copyResponse(response));
            response.appendChild(copyBtn);
        });
    }

    copyResponse(response) {
        const text = response.querySelector('.response-text').textContent;
        navigator.clipboard.writeText(text).then(() => {
            toastManager.show('Response copied to clipboard!', 'success');
        });
    }

    setupVoting() {
        document.querySelectorAll('.vote-button').forEach(button => {
            button.addEventListener('click', (e) => {
                const voteType = button.getAttribute('data-vote');
                const response = button.closest('.ai-response');
                const model = response.getAttribute('data-model');
                
                response.querySelectorAll('.vote-button').forEach(btn => {
                    btn.classList.remove('active');
                });
                
                button.classList.add('active');
                
                fetch('/vote', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        model: model,
                        vote: voteType
                    })
                })
                .then(response => response.json())
                .then(data => {
                    toastManager.show(`Vote ${voteType} recorded!`, 'success');
                })
                .catch(error => {
                    console.error('Error saving vote:', error);
                    toastManager.show('Failed to save vote', 'error');
                });
            });
        });
    }

    setupSharing() {
        // Remove any existing share buttons first
        document.querySelectorAll('.share-button').forEach(btn => btn.remove());
        
        document.querySelectorAll('.ai-response').forEach(response => {
            const actionButtons = response.querySelector('.action-buttons');
            if (!actionButtons) return;

            const shareBtn = document.createElement('button');
            shareBtn.className = 'share-button';
            shareBtn.innerHTML = '🔗';
            shareBtn.setAttribute('title', 'Share Response');
            shareBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                this.showShareMenu(response, shareBtn);
            });
            actionButtons.appendChild(shareBtn);
        });

        // Close share menu when clicking outside
        document.addEventListener('click', (e) => {
            if (!e.target.closest('.share-menu') && !e.target.closest('.share-button')) {
                document.querySelectorAll('.share-menu').forEach(menu => menu.remove());
            }
        });
    }

    showShareMenu(response, shareBtn) {
        // Remove any existing share menus
        document.querySelectorAll('.share-menu').forEach(menu => menu.remove());
        
        const responseText = response.querySelector('.response-text').textContent;
        const menu = document.createElement('div');
        menu.className = 'share-menu';
        
        const shareOptions = [
            {
                icon: '🐦',
                text: 'Share on Twitter',
                action: () => {
                    const tweetText = `${responseText.substring(0, 200)}${responseText.length > 200 ? '...' : ''}`;
                    window.open(`https://twitter.com/intent/tweet?text=${encodeURIComponent(tweetText)}`, '_blank');
                }
            },
            {
                icon: '💼',
                text: 'Share on LinkedIn',
                action: () => {
                    window.open(`https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(window.location.href)}`, '_blank');
                }
            },
            {
                icon: '📧',
                text: 'Share via Email',
                action: () => {
                    const subject = 'AI Response Share';
                    const body = `Check out this AI response:\n\n${responseText}`;
                    window.location.href = `mailto:?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
                }
            },
            null, // Divider
            {
                icon: '📋',
                text: 'Copy Response',
                action: () => {
                    navigator.clipboard.writeText(responseText)
                        .then(() => toastManager.show('Response copied to clipboard!', 'success'));
                }
            },
            {
                icon: '🔗',
                text: 'Copy Link',
                action: () => {
                    navigator.clipboard.writeText(window.location.href)
                        .then(() => toastManager.show('Link copied to clipboard!', 'success'));
                }
            }
        ];

        const menuContent = shareOptions.map(option => {
            if (!option) return '<div class="share-menu-divider"></div>';
            
            return `
                <button class="share-menu-button" data-action="${option.text}">
                    <i>${option.icon}</i>
                    <span>${option.text}</span>
                </button>
            `;
        }).join('');

        menu.innerHTML = menuContent;
        response.appendChild(menu);

        // Position the menu relative to the share button
        const buttonRect = shareBtn.getBoundingClientRect();
        const menuRect = menu.getBoundingClientRect();
        
        // Adjust position to prevent overflow
        let topPosition = buttonRect.bottom + window.scrollY;
        let leftPosition = buttonRect.left + window.scrollX - (menuRect.width - buttonRect.width);
        
        // Check if menu would go off the right edge
        if (leftPosition + menuRect.width > window.innerWidth) {
            leftPosition = window.innerWidth - menuRect.width - 10;
        }
        
        // Check if menu would go off the bottom edge
        if (topPosition + menuRect.height > window.innerHeight + window.scrollY) {
            topPosition = buttonRect.top + window.scrollY - menuRect.height;
        }
        
        menu.style.position = 'fixed';
        menu.style.top = `${topPosition}px`;
        menu.style.left = `${leftPosition}px`;

        // Add click handlers
        menu.querySelectorAll('.share-menu-button').forEach((button, index) => {
            const option = shareOptions[index];
            if (option) {
                button.addEventListener('click', (e) => {
                    e.stopPropagation();
                    option.action();
                    menu.remove();
                });
            }
        });
    }
}

// Export Manager
class ExportManager {
    constructor() {
        this.setupExportButtons();
    }

    setupExportButtons() {
        document.querySelectorAll('.export-button').forEach(button => {
            button.addEventListener('click', () => {
                const format = button.getAttribute('data-format');
                if (format === 'pdf') {
                    this.exportAsPDF();
                } else if (format === 'json') {
                    this.exportAsJSON();
                }
            });
        });
    }

    exportAsPDF() {
        toastManager.show('PDF export coming soon!', 'info');
    }

    exportAsJSON() {
        const data = {
            question: document.querySelector('#question-text').textContent,
            responses: Array.from(document.querySelectorAll('.ai-response')).map(response => ({
                model: response.getAttribute('data-model'),
                response: response.querySelector('.response-text').textContent,
                confidence: parseFloat(response.querySelector('.confidence').textContent.match(/[\d.]+/)[0]) / 100,
                responseTime: parseFloat(response.querySelector('.response-time').textContent.match(/[\d.]+/)[0])
            }))
        };

        const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'ai-responses.json';
        a.click();
        URL.revokeObjectURL(url);
    }
}

// View toggle functionality
document.addEventListener('DOMContentLoaded', function() {
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
});

// Initialize all features
document.addEventListener('DOMContentLoaded', function() {
    window.toastManager = new ToastManager();
    window.themeManager = new ThemeManager();
    window.characterCounter = new CharacterCounter('question', 1000);
    window.historyManager = new HistoryManager();
    window.responseManager = new ResponseManager();
    window.exportManager = new ExportManager();
}); 