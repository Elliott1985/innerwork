// Chatbot functionality for InnerWork

document.addEventListener('DOMContentLoaded', function() {
    const chatForm = document.getElementById('chatForm');
    const messageInput = document.getElementById('messageInput');
    const chatHistory = document.getElementById('chatHistory');
    const clearSessionBtn = document.getElementById('clearSessionBtn');
    const messageCountBadge = document.getElementById('messageCount');
    
    let messageCount = 0;
    
    // Auto-scroll to bottom of chat
    function scrollToBottom() {
        chatHistory.scrollTop = chatHistory.scrollHeight;
    }
    
    // Initial scroll
    scrollToBottom();
    
    // Update message count
    function updateMessageCount() {
        messageCount++;
        messageCountBadge.textContent = `${messageCount} message${messageCount !== 1 ? 's' : ''}`;
    }
    
    // Hide welcome message if it exists
    function hideWelcomeMessage() {
        const welcomeMsg = document.getElementById('welcomeMessage');
        if (welcomeMsg) {
            welcomeMsg.style.display = 'none';
        }
    }
    
    // Add message to chat UI
    function addMessageToUI(message, isUser = true) {
        hideWelcomeMessage();
        
        const messageDiv = document.createElement('div');
        messageDiv.className = isUser ? 'message user-message mb-3 animate-fade-in' : 'message bot-message mb-4 animate-fade-in';
        
        if (isUser) {
            const bubbleDiv = document.createElement('div');
            bubbleDiv.className = 'message-bubble user';
            bubbleDiv.textContent = message;
            
            const timestamp = document.createElement('small');
            timestamp.className = 'text-muted d-block mt-1';
            timestamp.style.fontSize = '0.75rem';
            const now = new Date();
            timestamp.textContent = now.toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit' });
            
            messageDiv.appendChild(bubbleDiv);
            messageDiv.appendChild(timestamp);
        } else {
            // Bot message with avatar
            const containerDiv = document.createElement('div');
            containerDiv.className = 'd-flex align-items-start';
            
            const avatar = document.createElement('div');
            avatar.className = 'bot-avatar me-2';
            avatar.style.cssText = 'width: 36px; height: 36px; background: linear-gradient(135deg, #c59fc9, #d4a5a5); border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-size: 0.9rem; flex-shrink: 0;';
            avatar.textContent = 'D';
            
            const bubbleDiv = document.createElement('div');
            bubbleDiv.className = 'message-bubble bot';
            bubbleDiv.style.flexGrow = '1';
            bubbleDiv.textContent = message;
            
            containerDiv.appendChild(avatar);
            containerDiv.appendChild(bubbleDiv);
            messageDiv.appendChild(containerDiv);
        }
        
        chatHistory.appendChild(messageDiv);
        scrollToBottom();
        updateMessageCount();
    }
    
    // Handle form submission
    chatForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const message = messageInput.value.trim();
        if (!message) return;
        
        // Disable input during processing
        messageInput.disabled = true;
        
        // Add user message to UI
        addMessageToUI(message, true);
        
        // Clear input
        messageInput.value = '';
        
        // Show typing indicator
        const typingDiv = document.createElement('div');
        typingDiv.className = 'message bot-message mb-4';
        typingDiv.id = 'typing-indicator';
        
        const typingContainer = document.createElement('div');
        typingContainer.className = 'd-flex align-items-start';
        
        const avatar = document.createElement('div');
        avatar.className = 'bot-avatar me-2';
        avatar.style.cssText = 'width: 36px; height: 36px; background: linear-gradient(135deg, #c59fc9, #d4a5a5); border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-size: 0.9rem; flex-shrink: 0;';
        avatar.textContent = 'D';
        
        const bubbleDiv = document.createElement('div');
        bubbleDiv.className = 'message-bubble bot';
        bubbleDiv.style.flexGrow = '1';
        bubbleDiv.innerHTML = '<em style="color: #999;">Debbie is typing...</em>';
        
        typingContainer.appendChild(avatar);
        typingContainer.appendChild(bubbleDiv);
        typingDiv.appendChild(typingContainer);
        
        chatHistory.appendChild(typingDiv);
        scrollToBottom();
        
        try {
            // Send message to backend
            const response = await fetch('/chatbot/message', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message: message })
            });
            
            const data = await response.json();
            
            // Remove typing indicator
            const indicator = document.getElementById('typing-indicator');
            if (indicator) {
                indicator.remove();
            }
            
            // Add bot response to UI
            if (data.response) {
                addMessageToUI(data.response, false);
            } else if (data.error) {
                addMessageToUI('I apologize, but I encountered a technical difficulty. Could you try sharing that again?', false);
            }
            
        } catch (error) {
            console.error('Error:', error);
            
            // Remove typing indicator
            const indicator = document.getElementById('typing-indicator');
            if (indicator) {
                indicator.remove();
            }
            
            addMessageToUI('I\'m having trouble connecting right now. Please give it another try in a moment.', false);
        } finally {
            // Re-enable input
            messageInput.disabled = false;
            messageInput.focus();
        }
    });
    
    // Clear session handler
    if (clearSessionBtn) {
        clearSessionBtn.addEventListener('click', async function() {
            if (!confirm('Are you sure you want to start a fresh conversation? This will clear the current context.')) {
                return;
            }
            
            try {
                const response = await fetch('/chatbot/clear', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    }
                });
                
                if (response.ok) {
                    // Clear UI
                    chatHistory.innerHTML = `
                        <div class="text-center text-muted py-5" id="welcomeMessage">
                            <div class="mb-4">
                                <svg width="80" height="80" viewBox="0 0 80 80" fill="none" xmlns="http://www.w3.org/2000/svg">
                                    <circle cx="40" cy="40" r="40" fill="#f8f5f2"/>
                                    <path d="M40 20c-11.046 0-20 8.954-20 20 0 5.039 1.87 9.636 4.941 13.145L22 62l8.855-2.941C34.364 61.13 38.961 63 44 63c11.046 0 20-8.954 20-20s-8.954-20-20-20z" fill="url(#welcomeGradient)"/>
                                    <circle cx="32" cy="38" r="2.5" fill="white"/>
                                    <circle cx="40" cy="38" r="2.5" fill="white"/>
                                    <circle cx="48" cy="38" r="2.5" fill="white"/>
                                    <path d="M32 48c0-4 3.5-7 8-7s8 3 8 7" stroke="white" stroke-width="2" stroke-linecap="round"/>
                                    <defs>
                                        <linearGradient id="welcomeGradient" x1="0" y1="0" x2="80" y2="80">
                                            <stop offset="0%" stop-color="#c59fc9"/>
                                            <stop offset="100%" stop-color="#d4a5a5"/>
                                        </linearGradient>
                                    </defs>
                                </svg>
                            </div>
                            <h5 class="mb-3" style="color: #c59fc9;">Welcome to Your Safe Space</h5>
                            <p class="mb-2">I'm Debbie &mdash; here to listen, support, and guide you.</p>
                            <p class="small text-muted">Share what's on your mind. There's no judgment here, only compassion.</p>
                        </div>
                    `;
                    
                    // Reset message count
                    messageCount = 0;
                    messageCountBadge.textContent = '0 messages';
                    
                    messageInput.focus();
                }
            } catch (error) {
                console.error('Error clearing session:', error);
                alert('Unable to clear session. Please refresh the page.');
            }
        });
    }
    
    // Focus on input when page loads
    messageInput.focus();
});
