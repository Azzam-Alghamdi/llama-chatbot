let isBotTyping = false;

function createMessageElement(message, sender) {
    const element = document.createElement('div');
    element.className = `message ${sender}-message`;
    element.innerHTML = `
                <div>${message.text}</div>
                <span class="timestamp">${message.time}</span>`;
    return element;
}

function showTypingIndicator() {
    if (isBotTyping) return;

    isBotTyping = true;
    const container = document.getElementById('chat-container');
    const typingIndicator = document.createElement('div');
    typingIndicator.className = 'message bot-message';
    typingIndicator.innerHTML = `
                <div class="typing">
                    <span></span><span></span><span></span>
                </div>
            `;
    container.appendChild(typingIndicator);
    container.scrollTop = container.scrollHeight;
}

function hideTypingIndicator() {
    isBotTyping = false;
    const typingElements = document.querySelectorAll('.typing');
    typingElements.forEach(el => el.parentElement.remove());
}

async function loadMessages() {
    try {
        const response = await fetch('/messages');
        const data = await response.json();
        const container = document.getElementById('chat-container');
        container.innerHTML = '';

        data.messages.forEach(message => {
            const element = createMessageElement(message, message.sender);
            container.appendChild(element);
        });

        container.scrollTop = container.scrollHeight;
    } catch (error) {
        console.error('Error loading messages:', error);
    }
}

async function sendMessage() {
    const input = document.getElementById('message-input');
    const message = input.value.trim();

    if (message) {
        try {
            // Send user message
            await fetch('/send', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `message=${encodeURIComponent(message)}`
            });

            input.value = '';
            await loadMessages();

            // Show typing indicator
            showTypingIndicator();

            // Simulate bot response delay
            setTimeout(async () => {
                hideTypingIndicator();
                await loadMessages();
            }, 1500);

        } catch (error) {
            console.error('Error sending message:', error);
        }
    }
}

// Handle Enter key
document.getElementById('message-input').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        e.preventDefault();
        sendMessage();
    }
});

// Initial load
loadMessages();