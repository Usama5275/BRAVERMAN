document.addEventListener('DOMContentLoaded', function() {
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const chatMessages = document.getElementById('chat-messages');
    const chatContainer = document.getElementById('chat-container');

    // Function to add a message to the chat
    function addMessage(message, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}`;
        
        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        messageContent.textContent = message;
        
        messageDiv.appendChild(messageContent);
        chatMessages.appendChild(messageDiv);
        
        // Scroll to the bottom of the chat
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    // Function to show typing indicator
    function showTypingIndicator() {
        const typingDiv = document.createElement('div');
        typingDiv.className = 'message assistant';
        typingDiv.id = 'typing-indicator';
        
        const typingContent = document.createElement('div');
        typingContent.className = 'message-content typing-indicator';
        
        for (let i = 0; i < 3; i++) {
            const dot = document.createElement('span');
            typingContent.appendChild(dot);
        }
        
        typingDiv.appendChild(typingContent);
        chatMessages.appendChild(typingDiv);
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    // Function to remove typing indicator
    function removeTypingIndicator() {
        const typingIndicator = document.getElementById('typing-indicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }

    // Handle form submission
    chatForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const message = userInput.value.trim();
        if (!message) return;
        
        // Add user message to chat
        addMessage(message, 'user');
        
        // Clear input field
        userInput.value = '';
        
        // Show typing indicator
        showTypingIndicator();
        
        // Send message to server
        fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: message })
        })
        .then(response => response.json())
        .then(data => {
            // Remove typing indicator
            removeTypingIndicator();
            
            // Add assistant response to chat
            addMessage(data.response, 'assistant');
        })
        .catch(error => {
            console.error('Error:', error);
            removeTypingIndicator();
            addMessage('Sorry, there was an error processing your request.', 'assistant');
        });
    });

    // Focus input field on page load
    userInput.focus();
});