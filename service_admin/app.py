import os
from flask import Flask, jsonify
from models.models import db, Usuario
from blueprints.auth_bp import auth_bp
from blueprints.admin_bp import admin_bp
from werkzeug.security import generate_password_hash


def create_app():
    app = Flask(__name__)

    # Configuración 
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "DATABASE_URL", "sqlite:///db_admin.sqlite"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "odontocare-secret-key-2026-jwt-ok")

    # Inicializamos la base de datos 
    db.init_app(app)

    # Registramos los blueprints 
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)

    # Creamos las tablas y el admin inicial 
    with app.app_context():
        db.create_all()
        _crear_admin_inicial()

    # Manejo de errores 
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": str(e)}), 404

    @app.errorhandler(500)
    def server_error(e):
        return jsonify({"error": "Error interno del servidor"}), 500

    return app


def _crear_admin_inicial():
    """Crea un usuario admin por defecto si no existe ninguno."""
    if not Usuario.query.filter_by(rol="admin").first():
        admin = Usuario(
            username="admin",
            password=generate_password_hash("admin123"),
            rol="admin",
        )
        db.session.add(admin)
        db.session.commit()
        print("OK - Admin inicial creado: admin / admin123")


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)