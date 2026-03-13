"""
Servicio para interactuar con la API de Groq.
Soporta contexto de tareas del usuario para responder preguntas sobre
tareas pendientes, completadas y estadísticas del sistema.
"""

import os
from groq import Groq

SYSTEM_PROMPT = (
    "Eres un asistente virtual amable, cordial y respetuoso. "
    "Siempre respondes de forma amigable, con buena disposición y sin importar el tema. "
    "Tus respuestas son claras, útiles y nunca groseras. "
    "Cuando el usuario pregunta sobre sus tareas, utiliza exclusivamente la información "
    "de contexto proporcionada (no inventes datos)."
)

# Palabras clave que indican que la pregunta está relacionada con tareas del usuario
TASK_KEYWORDS = [
    "tarea", "tareas", "pendiente", "pendientes", "completé", "completada",
    "completadas", "completado", "completados", "cuántas tareas", "cuantas tareas",
    "mis tareas", "en progreso", "en_progreso", "registradas", "registrada",
    "estadísticas", "estadistica", "resumen", "progreso",
]


def is_task_related(message: str) -> bool:
    """Retorna True si el mensaje parece consultar sobre las tareas del usuario."""
    lower = message.lower()
    return any(kw in lower for kw in TASK_KEYWORDS)


def get_groq_client() -> Groq:
    """Devuelve un cliente Groq inicializado con la clave de entorno."""
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise EnvironmentError("La variable de entorno GROQ_API_KEY no está definida.")
    return Groq(api_key=api_key)


def send_message(
    user_message: str,
    history: list[dict] | None = None,
    task_context: str | None = None,
) -> str:
    """
    Envía un mensaje a la IA Groq y retorna la respuesta como string.

    Args:
        user_message:  Texto enviado por el usuario.
        history:       Lista de mensajes previos con roles 'user'/'assistant'
                       (opcional, para contexto de conversación).
        task_context:  Resumen de tareas del usuario inyectado como contexto del sistema
                       (opcional).

    Returns:
        Respuesta de la IA como string.
    """
    client = get_groq_client()

    system_content = SYSTEM_PROMPT
    if task_context:
        system_content += f"\n\nINFORMACIÓN ACTUAL DE LAS TAREAS DEL USUARIO:\n{task_context}"

    messages = [{"role": "system", "content": system_content}]

    if history:
        messages.extend(history)

    messages.append({"role": "user", "content": user_message})

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",   # modelo LLaMA 3.3 70B disponible en Groq
        messages=messages,
        temperature=0.7,
        max_tokens=1024,
    )

    return completion.choices[0].message.content
