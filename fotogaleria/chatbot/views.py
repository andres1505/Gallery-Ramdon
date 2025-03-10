from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .models import Personaje, Conversacion, Mensaje
import json
import random

def lista_personajes(request):
    """Vista para mostrar todos los personajes disponibles"""
    personajes = Personaje.objects.filter(activo=True)
    return render(request, 'chatbot/lista_personajes.html', {
        'personajes': personajes,
    })

def detalle_personaje(request, personaje_id):
    """Vista para mostrar el detalle de un personaje y comenzar una conversación"""
    personaje = get_object_or_404(Personaje, id=personaje_id, activo=True)
    
    # Crear una nueva conversación o recuperar la más reciente
    if request.user.is_authenticated:
        conversacion, created = Conversacion.objects.get_or_create(
            usuario=request.user,
            personaje=personaje,
            defaults={'titulo': f"Conversación con {personaje.nombre}"}
        )
    else:
        # Para usuarios no autenticados, siempre crear una nueva
        conversacion = Conversacion.objects.create(
            personaje=personaje,
            titulo=f"Conversación con {personaje.nombre}"
        )
    
    # Si es una nueva conversación, añadir un mensaje de bienvenida
    if created or conversacion.mensajes.count() == 0:
        saludos = [
            f"¡Hola! Soy {personaje.nombre}. ¿En qué puedo ayudarte?",
            f"¡Bienvenido! Es un placer hablar contigo. Soy {personaje.nombre}.",
            f"¡Hey! Soy {personaje.nombre}. ¿Qué quieres saber de mí?",
        ]
        Mensaje.objects.create(
            conversacion=conversacion,
            texto=random.choice(saludos),
            tipo=Mensaje.PERSONAJE
        )
    
    mensajes = conversacion.mensajes.all()
    
    return render(request, 'chatbot/detalle_personaje.html', {
        'personaje': personaje,
        'conversacion': conversacion,
        'mensajes': mensajes,
    })

@csrf_exempt
def enviar_mensaje(request, personaje_id):
    """Vista para procesar los mensajes enviados por AJAX"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    
    try:
        data = json.loads(request.body)
        mensaje_texto = data.get('mensaje', '').strip()
        conversacion_id = data.get('conversacion_id')
        
        if not mensaje_texto:
            return JsonResponse({'error': 'Mensaje vacío'}, status=400)
        
        personaje = get_object_or_404(Personaje, id=personaje_id, activo=True)
        conversacion = get_object_or_404(Conversacion, id=conversacion_id, personaje=personaje)
        
        # Guardar mensaje del usuario
        mensaje_usuario = Mensaje.objects.create(
            conversacion=conversacion,
            texto=mensaje_texto,
            tipo=Mensaje.USUARIO
        )
        
        # Generar respuesta del personaje
        respuesta = generar_respuesta(personaje, mensaje_texto)
        
        # Guardar respuesta del personaje
        mensaje_personaje = Mensaje.objects.create(
            conversacion=conversacion,
            texto=respuesta,
            tipo=Mensaje.PERSONAJE
        )
        
        return JsonResponse({
            'exito': True,
            'mensaje_usuario': {
                'id': mensaje_usuario.id,
                'texto': mensaje_usuario.texto,
                'fecha': mensaje_usuario.fecha.strftime('%H:%M'),
            },
            'mensaje_personaje': {
                'id': mensaje_personaje.id,
                'texto': mensaje_personaje.texto,
                'fecha': mensaje_personaje.fecha.strftime('%H:%M'),
            }
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def generar_respuesta(personaje, mensaje):
    """
    Función para generar respuestas basadas en la personalidad del personaje.
    En una implementación real, aquí se conectaría con una API de IA.
    """
    # Respuestas predeterminadas básicas según el personaje
    if personaje.nombre.lower() == "messi":
        respuestas = [
            "En el fútbol, como en la vida, lo importante es seguir adelante y dar lo mejor.",
            "Siempre he soñado con ganar trofeos con mi país. Ese es mi mayor objetivo.",
            "La clave del éxito es trabajar día a día y mantener la humildad.",
            "Los récords son bonitos, pero lo importante es ganar títulos en equipo.",
            "¡Cada partido es una nueva oportunidad para dar alegría a la gente!"
        ]
    elif personaje.nombre.lower() == "cristiano":
        respuestas = [
            "¡SIUUU! El trabajo duro siempre vence al talento cuando el talento no trabaja duro.",
            "Los logros se consiguen con dedicación y sacrificio constantes.",
            "Siempre busco superar mis propios límites. La competencia conmigo mismo es la más importante.",
            "Cuando la gente duda de mí, es cuando más me motivo para demostrar que están equivocados.",
            "El fútbol es mi pasión, pero la familia siempre es lo primero."
        ]
    elif personaje.nombre.lower() == "spiderman":
        respuestas = [
            "Un gran poder conlleva una gran responsabilidad.",
            "La ciudad nunca duerme, ¡y yo tampoco cuando hay villanos sueltos!",
            "A veces ser héroe significa tomar decisiones difíciles.",
            "¡Mi sentido arácnido está en alerta máxima!",
            "Entre salvar la ciudad y entregar los deberes a tiempo, ¡la vida de un estudiante superhéroe no es fácil!"
        ]
    elif personaje.nombre.lower() == "cj":
        respuestas = [
            "Ah, aquí vamos de nuevo...",
            "Grove Street. Hogar. Al menos lo era antes de que lo arruinara todo.",
            "Sigo al tren, ¡no te preocupes!",
            "Los números no mienten. Vengo a recuperar lo que es mío.",
            "Las cosas son más complicadas de lo que parecen, pero al final todo tiene sentido."
        ]
    else:
        respuestas = [
            f"Como {personaje.nombre}, estoy aquí para conversar contigo.",
            "Esa es una pregunta interesante. Déjame pensarlo.",
            "Gracias por chatear conmigo. ¿Hay algo más que quieras saber?",
            "Estoy disfrutando mucho esta conversación.",
            "¡Vaya! Nunca me habían preguntado eso antes."
        ]
    
    # En un sistema real, aquí usarías la API de OpenAI u otra IA
    # Por ahora, seleccionamos una respuesta aleatoria
    return random.choice(respuestas)

def historial_conversaciones(request):
    """Vista para mostrar el historial de conversaciones del usuario"""
    if not request.user.is_authenticated:
        # Para usuarios no autenticados, mostrar un mensaje
        return render(request, 'chatbot/historial_conversaciones.html', {
            'conversaciones': [],
            'mensaje': 'Debes iniciar sesión para ver tu historial de conversaciones'
        })
    
    conversaciones = Conversacion.objects.filter(usuario=request.user).order_by('-fecha_creacion')
    return render(request, 'chatbot/historial_conversaciones.html', {
        'conversaciones': conversaciones,
    })

def ver_conversacion(request, conversacion_id):
    """Vista para ver una conversación específica"""
    conversacion = get_object_or_404(Conversacion, id=conversacion_id)
    
    # Verificar que el usuario tiene acceso a esta conversación
    if request.user.is_authenticated and conversacion.usuario != request.user:
        # Si el usuario está autenticado pero no es el dueño
        return redirect('chatbot:historial_conversaciones')
    
    mensajes = conversacion.mensajes.all()
    
    return render(request, 'chatbot/ver_conversacion.html', {
        'conversacion': conversacion,
        'personaje': conversacion.personaje,
        'mensajes': mensajes,
    })

