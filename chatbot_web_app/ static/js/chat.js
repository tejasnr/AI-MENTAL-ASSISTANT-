// static/js/chat.js

document.addEventListener('DOMContentLoaded', () => {
    const socket = io();

    const chatForm = document.getElementById('chat-form');
    const chatWindow = document.getElementById('chat-window');
    const messageInput = document.getElementById('message-input');

    chatForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const message = messageInput.value.trim();
        if (message) {
            addMessageToChat('user', message);
            socket.emit('user_message', message);
            messageInput.value = '';
        }
    });

    socket.on('assistant_message', (message) => {
        addMessageToChat('assistant', message);
    });

    function addMessageToChat(sender, message) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', sender);

        const messageContent = document.createElement('div');
        messageContent.classList.add('message-content');
        messageContent.textContent = message;

        messageElement.appendChild(messageContent);
        chatWindow.appendChild(messageElement);

        chatWindow.scrollTop = chatWindow.scrollHeight;
    }
});


