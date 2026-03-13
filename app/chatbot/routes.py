"""
Rutas del chatbot.

GET  /chatbot/       → Renderiza la página del chat.
POST /api/chat       → Recibe JSON {"message": "...", "history": [...]}
                       y devuelve JSON {"reply": "..."}.
"""

from flask import request, jsonify, render_template
from app.chatbot import chatbot_bp
from app.chatbot.service import send_message
from app import csrf


@chatbot_bp.route("/", methods=["GET"])
def chat_page():
    """Página principal del chatbot."""
    return render_template("chatbot/chat.html")


@chatbot_bp.route("/api/chat", methods=["POST"])
@csrf.exempt
def api_chat():
    """
    Endpoint POST que recibe un mensaje y devuelve la respuesta de Groq.

    Body JSON esperado:
        {
            "message": "Hola, ¿cómo estás?",
            "history": [                          ← opcional
                {"role": "user",      "content": "..."},
                {"role": "assistant", "content": "..."}
            ]
        }

    Respuesta JSON:
        {"reply": "Hola! Estoy muy bien, gracias por preguntar..."}
    """
    data = request.get_json(silent=True)

    if not data or not data.get("message", "").strip():
        return jsonify({"error": "El campo 'message' es requerido y no puede estar vacío."}), 400

    user_message = data["message"].strip()
    history = data.get("history", [])

    try:
        reply = send_message(user_message, history)
    except EnvironmentError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": f"Error al contactar con Groq: {str(e)}"}), 502

    return jsonify({"reply": reply})
