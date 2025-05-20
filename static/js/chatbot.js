document.addEventListener('DOMContentLoaded', function() {
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const chatContainer = document.getElementById('chat-container');
    
    chatForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const message = userInput.value.trim();
        
        if (!message) return;
        
        // Add user message to chat
        addMessage(message, 'user');
        userInput.value = '';
        
        // Get bot response
        fetch('/chatbot', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: JSON.stringify({ message: message })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                throw new Error(data.error);
            }
            addMessage(data.response, 'bot');
        })
        .catch(error => {
            addMessage(`Error: ${error.message}`, 'error');
        });
    });
    
    function addMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('d-flex', 'mb-3');
        
        if (sender === 'user') {
            messageDiv.classList.add('justify-content-end');
            messageDiv.innerHTML = `
                <div class="bg-primary text-white p-3 rounded" style="max-width: 70%;">
                    ${text}
                </div>
            `;
        } else {
            messageDiv.classList.add('justify-content-start');
            const bgClass = sender === 'error' ? 'bg-danger' : 'bg-light';
            messageDiv.innerHTML = `
                <div class="${bgClass} text-dark p-3 rounded" style="max-width: 70%;">
                    ${text}
                </div>
            `;
        }
        
        chatContainer.appendChild(messageDiv);
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }
});