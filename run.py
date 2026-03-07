import os
from app import create_app, db
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# Crear la aplicación
app = create_app(os.environ.get('FLASK_ENV', 'development'))


@app.shell_context_processor
def make_shell_context():
    """Contexto para la shell de Flask."""
    return {'db': db}


if __name__ == '__main__':
    # Configurar parámetros de ejecución
    debug = os.environ.get('FLASK_DEBUG', True)
    host = os.environ.get('FLASK_HOST', '127.0.0.1')
    port = int(os.environ.get('FLASK_PORT', 5001))
    
    print(f"\n{'='*50}")
    print(f"Flask Task Manager")
    print(f"{'='*50}")
    print(f"Ejecutando en: http://{host}:{port}")
    print(f"Debug mode: {debug}")
    print(f"{'='*50}\n")
    
    app.run(host=host, port=port, debug=debug)
