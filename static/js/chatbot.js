// Chatbot functionality for InnerWork

document.addEventListener('DOMContentLoaded', function() {
    const chatForm = document.getElementById('chatForm');
    const messageInput = document.getElementById('messageInput');
    const chatHistory = document.getElementById('chatHistory');
    
    // Auto-scroll to bottom of chat
    function scrollToBottom() {
        chatHistory.scrollTop = chatHistory.scrollHeight;
    }
    
    // Initial scroll
    scrollToBottom();
    
    // Add message to chat UI
    function addMessageToUI(message, isUser = true) {
        const messageDiv = document.createElement('div');
        messageDiv.className = isUser ? 'message user-message mb-3' : 'message bot-message mb-3';
        
        const bubbleDiv = document.createElement('div');
        bubbleDiv.className = isUser ? 'message-bubble user' : 'message-bubble bot';
        
        const label = isUser ? 'You' : 'Virtual Debbie';
        bubbleDiv.innerHTML = `<strong>${label}:</strong> ${message}`;
        
        messageDiv.appendChild(bubbleDiv);
        
        if (isUser) {
            const timestamp = document.createElement('small');
            timestamp.className = 'text-muted';
            const now = new Date();
            timestamp.textContent = now.toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit' });
            messageDiv.appendChild(timestamp);
        }
        
        chatHistory.appendChild(messageDiv);
        scrollToBottom();
    }
    
    // Handle form submission
    chatForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const message = messageInput.value.trim();
        if (!message) return;
        
        // Add user message to UI
        addMessageToUI(message, true);
        
        // Clear input
        messageInput.value = '';
        
        // Show typing indicator
        const typingDiv = document.createElement('div');
        typingDiv.className = 'message bot-message mb-3';
        typingDiv.id = 'typing-indicator';
        typingDiv.innerHTML = '<div class="message-bubble bot"><em>Virtual Debbie is thinking...</em></div>';
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
                addMessageToUI('Sorry, I encountered an error. Please try again.', false);
            }
            
        } catch (error) {
            console.error('Error:', error);
            
            // Remove typing indicator
            const indicator = document.getElementById('typing-indicator');
            if (indicator) {
                indicator.remove();
            }
            
            addMessageToUI('Sorry, I had trouble connecting. Please try again.', false);
        }
    });
    
    // Focus on input when page loads
    messageInput.focus();
});
