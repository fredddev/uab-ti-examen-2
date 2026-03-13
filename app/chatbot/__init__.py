from flask import Blueprint

chatbot_bp = Blueprint('chatbot', __name__, url_prefix='/chatbot')

from app.chatbot import routes  # noqa: E402, F401
