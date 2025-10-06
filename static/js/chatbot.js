document.addEventListener('DOMContentLoaded', () => {
    const chatbotButton = document.createElement('button');
    chatbotButton.id = 'chatbot-button';
    chatbotButton.innerHTML = '💬';
    chatbotButton.setAttribute('aria-label', 'Open chatbot');
    document.body.appendChild(chatbotButton);

    const chatbotPanel = document.createElement('div');
    chatbotPanel.id = 'chatbot-panel';
    chatbotPanel.innerHTML = `
        <div id="chatbot-header">
            <span>Chat with Us</span>
            <button id="chatbot-close" aria-label="Close chatbot">&times;</button>
        </div>
        <div id="chatbot-messages"></div>
        <div id="chatbot-input">
            <input type="text" id="chatbot-message" placeholder="Type your message..." />
            <button id="chatbot-send">Send</button>
        </div>
    `;
    document.body.appendChild(chatbotPanel);

    const messagesDiv = document.getElementById('chatbot-messages');
    const messageInput = document.getElementById('chatbot-message');
    const sendButton = document.getElementById('chatbot-send');
    const closeButton = document.getElementById('chatbot-close');

    chatbotButton.addEventListener('click', () => {
        chatbotPanel.style.display = 'flex';
        messageInput.focus();
    });

    closeButton.addEventListener('click', () => {
        chatbotPanel.style.display = 'none';
    });

    sendButton.addEventListener('click', sendMessage);
    messageInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });

    function sendMessage() {
        const message = messageInput.value.trim();
        if (!message) return;

        addMessage('user', message);
        messageInput.value = '';

        fetch('/chatbot', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                addMessage('bot', data.error);
            } else {
                addMessage('bot', data.response);
            }
        })
        .catch(error => {
            addMessage('bot', 'Sorry, something went wrong.');
        });
    }

    function addMessage(sender, text) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `chatbot-message ${sender}`;
        messageDiv.textContent = text;
        messagesDiv.appendChild(messageDiv);
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    }
});
