"""
Rutas del chatbot.

GET  /chatbot/       → Renderiza la página del chat.
POST /api/chat       → Recibe JSON {"message": "...", "history": [...]}
                       y devuelve JSON {"reply": "..."}.
"""

from flask import request, jsonify, render_template
from flask_login import login_required, current_user
from app.chatbot import chatbot_bp
from app.chatbot.service import send_message, is_task_related
from app.models.task import Task
from app import csrf


def _build_task_context(user_id: int) -> str:
    """
    Consulta la base de datos y construye un resumen de tareas del usuario
    para inyectarlo como contexto al modelo de IA.
    """
    tasks = Task.query.filter_by(user_id=user_id).all()

    if not tasks:
        return "El usuario no tiene ninguna tarea registrada."

    pending   = [t for t in tasks if t.status == "pendiente"]
    in_prog   = [t for t in tasks if t.status == "en_progreso"]
    completed = [t for t in tasks if t.status == "completado"]

    lines = [
        f"Total de tareas: {len(tasks)}",
        f"Pendientes ({len(pending)}): " +
            (", ".join(f'"{t.title}"' for t in pending) if pending else "ninguna"),
        f"En progreso ({len(in_prog)}): " +
            (", ".join(f'"{t.title}"' for t in in_prog) if in_prog else "ninguna"),
        f"Completadas ({len(completed)}): " +
            (", ".join(f'"{t.title}"' for t in completed) if completed else "ninguna"),
    ]
    return "\n".join(lines)


@chatbot_bp.route("/", methods=["GET"])
@login_required
def chat_page():
    """Página principal del chatbot."""
    return render_template("chatbot/chat.html")


@chatbot_bp.route("/api/chat", methods=["POST"])
@csrf.exempt
@login_required
def api_chat():
    """
    Endpoint POST que recibe un mensaje y devuelve la respuesta de Groq.

    Si el mensaje está relacionado con tareas del usuario, se inyecta
    un resumen actualizado de la base de datos como contexto al modelo.

    Body JSON esperado:
        {
            "message": "¿Qué tareas tengo pendientes?",
            "history": [                          ← opcional
                {"role": "user",      "content": "..."},
                {"role": "assistant", "content": "..."}
            ]
        }

    Respuesta JSON:
        {"reply": "Tienes 3 tareas pendientes: ..."}
    """
    data = request.get_json(silent=True)

    if not data or not data.get("message", "").strip():
        return jsonify({"error": "El campo 'message' es requerido y no puede estar vacío."}), 400

    user_message = data["message"].strip()
    history = data.get("history", [])

    # Inyectar contexto de tareas si la pregunta lo requiere
    task_context = None
    if is_task_related(user_message):
        task_context = _build_task_context(current_user.id)

    try:
        reply = send_message(user_message, history, task_context=task_context)
    except EnvironmentError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": f"Error al contactar con Groq: {str(e)}"}), 502

    return jsonify({"reply": reply})
