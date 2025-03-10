document.addEventListener('DOMContentLoaded', function () {
    const chatMessages = document.getElementById('chatMessages');
    // Desplazamiento inicial hacia el final del chat
    chatMessages.scrollTop = chatMessages.scrollHeight;
});
