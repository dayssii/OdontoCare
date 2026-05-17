# Gestión operativa de citas
## Importaciones
import os
import requests
from flask import Blueprint, request, jsonify
from models.models import db, Cita

## URL del servicio admin, se configura por variable de entorno
ADMIN_SERVICE_URL = os.environ.get("ADMIN_SERVICE_URL", "http://localhost:5000")

## Creamos el blueprint de citas
citas_bp = Blueprint("citas", __name__, url_prefix="/citas")


## Funciones helper que llaman al servicio admin para validar datos
def _get_headers():
    """Pasa el token del usuario actual al servicio admin."""
    return {"Authorization": request.headers.get("Authorization", "")}


def verificar_doctor(id_doctor):
    """Pregunta al service_admin si el doctor existe."""
    try:
        r = requests.get(
            f"{ADMIN_SERVICE_URL}/admin/doctores/{id_doctor}",
            headers=_get_headers(), timeout=5
        )
        return r.json() if r.status_code == 200 else None
    except Exception:
        return None


def verificar_paciente(id_paciente):
    """Pregunta al service_admin si el paciente existe y está ACTIVO."""
    try:
        r = requests.get(
            f"{ADMIN_SERVICE_URL}/admin/pacientes/{id_paciente}",
            headers=_get_headers(), timeout=5
        )
        if r.status_code == 200:
            data = r.json()
            return data if data.get("estado") == "ACTIVO" else None
    except Exception:
        return None


def verificar_centro(id_centro):
    """Pregunta al service_admin si el centro existe."""
    try:
        r = requests.get(
            f"{ADMIN_SERVICE_URL}/admin/centros/{id_centro}",
            headers=_get_headers(), timeout=5
        )
        return r.json() if r.status_code == 200 else None
    except Exception:
        return None


## Endpoints: POST/ citas (Agendar cita)
@citas_bp.route("", methods=["POST"])
def agendar_cita():
    """Agenda una nueva cita médica."""
    data = request.get_json()

    # comprobamos campos obligatorios
    campos = ["fecha", "motivo", "id_paciente", "id_doctor", "id_centro"]
    if not all(data.get(c) for c in campos):
        return jsonify({"error": f"Campos requeridos: {campos}"}), 400

    # validamos consultando al service_admin
    if not verificar_doctor(data["id_doctor"]):
        return jsonify({"error": "Doctor no encontrado"}), 404

    if not verificar_paciente(data["id_paciente"]):
        return jsonify({"error": "Paciente no encontrado o inactivo"}), 404

    if not verificar_centro(data["id_centro"]):
        return jsonify({"error": "Centro médico no encontrado"}), 404

    # evitamos doble reserva del mismo doctor en la misma fecha y hora
    conflicto = Cita.query.filter_by(
        id_doctor=data["id_doctor"],
        fecha=data["fecha"],
        estado="Programada",
    ).first()
    if conflicto:
        return jsonify({"error": "El doctor ya tiene una cita en esa fecha y hora"}), 409

    # creamos la cita
    cita = Cita(
        fecha=data["fecha"],
        motivo=data["motivo"],
        id_paciente=data["id_paciente"],
        id_doctor=data["id_doctor"],
        id_centro=data["id_centro"],
        id_usuario_registra=1,  # por ahora fijo, luego lo sacaremos del token
        estado="Programada",
    )
    db.session.add(cita)
    db.session.commit()
    return jsonify({"mensaje": "Cita agendada correctamente", "cita": cita.to_dict()}), 201


## Endpoints: GET / citas (Listar citas)
@citas_bp.route("", methods=["GET"])
def listar_citas():
    """Lista todas las citas con filtros opcionales."""
    query = Cita.query

    # filtros por query params
    for filtro, columna in [
        ("id_doctor", Cita.id_doctor),
        ("id_centro", Cita.id_centro),
        ("id_paciente", Cita.id_paciente),
        ("estado", Cita.estado),
    ]:
        valor = request.args.get(filtro)
        if valor:
            query = query.filter(columna == valor)

    # filtro por fecha parcial (ej: 2025-09)
    fecha = request.args.get("fecha")
    if fecha:
        query = query.filter(Cita.fecha.startswith(fecha))

    citas = query.all()
    return jsonify([c.to_dict() for c in citas]), 200


## Endpoints: GET/ citas/<id> (Detalle de cita)
@citas_bp.route("/<int:id>", methods=["GET"])
def obtener_cita(id):
    """Devuelve una cita por su ID."""
    cita = Cita.query.get_or_404(id, description="Cita no encontrada")
    return jsonify(cita.to_dict()), 200


## Endpoints: PUT / citas/<id> (Cancelar cita)
@citas_bp.route("/<int:id>", methods=["PUT"])
def cancelar_cita(id):
    """Cancela una cita existente."""
    cita = Cita.query.get_or_404(id, description="Cita no encontrada")

    if cita.estado == "Cancelada":
        return jsonify({"error": "La cita ya está cancelada"}), 400

    cita.estado = "Cancelada"
    db.session.commit()
    return jsonify({
        "mensaje": f"Cita {id} cancelada correctamente",
        "cita": cita.to_dict(),
    }), 200