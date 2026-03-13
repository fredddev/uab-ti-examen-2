"""
Servicio para interactuar con la API de Groq.
Sin conexión a base de datos — conversación stateless por petición.
"""

import os
from groq import Groq

SYSTEM_PROMPT = (
    "Eres un asistente virtual amable, cordial y respetuoso. "
    "Siempre respondes de forma amigable, con buena disposición y sin importar el tema. "
    "Tus respuestas son claras, útiles y nunca groseras."
)

def get_groq_client() -> Groq:
    """Devuelve un cliente Groq inicializado con la clave de entorno."""
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise EnvironmentError("La variable de entorno GROQ_API_KEY no está definida.")
    return Groq(api_key=api_key)


def send_message(user_message: str, history: list[dict] | None = None) -> str:
    """
    Envía un mensaje a la IA Groq y retorna la respuesta como string.

    Args:
        user_message: Texto enviado por el usuario.
        history:      Lista de mensajes previos con roles 'user'/'assistant'
                      (opcional, para contexto de conversación).

    Returns:
        Respuesta de la IA como string.
    """
    client = get_groq_client()

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

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
