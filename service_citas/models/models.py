from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

# Creamos la tabla de citas médicas
class Cita(db.Model):
    __tablename__ = "citas"

    id_cita = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.String(20), nullable=False)  # formato "YYYY-MM-DD HH:MM"
    motivo = db.Column(db.String(300), nullable=False)
    estado = db.Column(db.String(15), default="Programada")  # Programada, Cancelada, Completada
    id_paciente = db.Column(db.Integer, nullable=False)  # no FK porque está en otra base de datos
    id_doctor = db.Column(db.Integer, nullable=False)    # no FK porque está en otra base de datos
    id_centro = db.Column(db.Integer, nullable=False)    # no FK porque está en otra base de datos
    id_usuario_registra = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            "id_cita": self.id_cita,
            "fecha": self.fecha,
            "motivo": self.motivo,
            "estado": self.estado,
            "id_paciente": self.id_paciente,
            "id_doctor": self.id_doctor,
            "id_centro": self.id_centro,
            "id_usuario_registra": self.id_usuario_registra,
        }