document.addEventListener('DOMContentLoaded', function () {
    const chatMessages = document.getElementById('chatMessages');
    const messageInput = document.getElementById('messageInput');
    const sendButton = document.getElementById('sendButton');
    const typingIndicator = document.getElementById('typingIndicator');

    // Función para desplazar automáticamente hacia abajo
    function scrollToBottom() {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Desplazamiento inicial
    scrollToBottom();

    // Función para enviar mensajes
    function sendMessage() {
        const message = messageInput.value.trim();
        if (!message) return;

        // Desactivar el input y botón mientras se procesa
        messageInput.disabled = true;
        sendButton.disabled = true;

        // Solicitud AJAX
        fetch('{% url "chatbot:enviar_mensaje" personaje.id %}', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                mensaje: message,
                conversacion_id: '{{ conversacion.id }}'
            })
        })
            .then(response => response.json())
            .then(data => {
                if (data.exito) {
                    // Limpiar el input
                    messageInput.value = '';

                    // Crear elementos para mensaje del usuario
                    const userMessageDiv = document.createElement('div');
                    userMessageDiv.className = 'message message-usuario';
                    userMessageDiv.innerHTML = `
                            <div class="message-content">
                                ${data.mensaje_usuario.texto}
                                <div class="message-time">${data.mensaje_usuario.fecha}</div>
                            </div>
                        `;
                    chatMessages.appendChild(userMessageDiv);
                    scrollToBottom();

                    // Mostrar indicador de escritura
                    typingIndicator.style.display = 'block';

                    // Simular tiempo de respuesta (entre 1 y 3 segundos)
                    setTimeout(() => {
                        // Ocultar indicador de escritura
                        typingIndicator.style.display = 'none';

                        // Crear elementos para mensaje del personaje
                        const characterMessageDiv = document.createElement('div');
                        characterMessageDiv.className = 'message message-personaje';
                        characterMessageDiv.innerHTML = `
                                <div class="message-content">
                                    ${data.mensaje_personaje.texto}
                                    <div class="message-time">${data.mensaje_personaje.fecha}</div>
                                </div>
                            `;
                        chatMessages.appendChild(characterMessageDiv);
                        scrollToBottom();
                    }, Math.random() * 2000 + 1000); // Entre 1 y 3 segundos
                } else {
                    alert('Error: ' + data.error);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Ha ocurrido un error. Por favor, intenta de nuevo.');
            })
            .finally(() => {
                // Reactivar el input y botón
                messageInput.disabled = false;
                sendButton.disabled = false;
                messageInput.focus();
            });
    }

    // Evento para el botón de enviar
    sendButton.addEventListener('click', sendMessage);

    // Evento para presionar Enter
    messageInput.addEventListener('keypress', function (event) {
        if (event.key === 'Enter') {
            event.preventDefault();
            sendMessage();
        }
    });

    // Enfocar el input automáticamente
    messageInput.focus();
});
