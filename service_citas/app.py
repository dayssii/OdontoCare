import os
from flask import Flask, jsonify
from models.models import db
from blueprints.citas_bp import citas_bp


def create_app():
    app = Flask(__name__)

    # Configuración 
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "DATABASE_URL", "sqlite:///db_citas.sqlite"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Inicializamos la base de datos 
    db.init_app(app)

    # Registramos el blueprint de citas 
    app.register_blueprint(citas_bp)

    # Creamos las tablas 
    with app.app_context():
        db.create_all()

    # Manejo de errores 
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": str(e)}), 404

    @app.errorhandler(500)
    def server_error(e):
        return jsonify({"error": "Error interno del servidor"}), 500

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5001, debug=True)