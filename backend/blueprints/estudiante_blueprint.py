from flask import Flask
from flask import Blueprint
from flask import request
from flask import jsonify
from werkzeug.utils import secure_filename
import json
from flask_cors import CORS, cross_origin
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity

from backend.models.mysql_estudiante_model import estudianteModel
model = estudianteModel()

estudiante_blueprint = Blueprint('estudiante_blueprint', __name__)

@estudiante_blueprint.route('/estudiante', methods=['PUT'])
@jwt_required()
@cross_origin()
def create_estudiante():
    content = model.create_estudiante(request.json['usuario_dni'], request.json['usuario_nombre'], request.json['usuario_apellido'], request.json['usuario_telefono'], request.json['usuario_correo'], request.json['usuario_contraseña'], request.json['usuario_ruta'])    
    return jsonify(content)

@estudiante_blueprint.route('/estudiante', methods=['PATCH'])
@jwt_required()
@cross_origin()
def update_estudiante():
    content = model.update_estudiante(request.json['usuario_dni'], request.json['usuario_nombre'], request.json['usuario_apellido'], request.json['usuario_telefono'], request.json['usuario_correo'], request.json['usuario_contraseña'], request.json['usuario_ruta'])     
    return jsonify(content)

@estudiante_blueprint.route('/estudiante', methods=['DELETE'])
@jwt_required()
@cross_origin()
def delete_estudiante():
    return jsonify(model.delete_estudiante(int(request.json['dni'])))

@estudiante_blueprint.route('/estudiante', methods=['POST'])
@cross_origin()
def estudiante():
    return jsonify(model.get_estudiante(int(request.json['dni'])))

@estudiante_blueprint.route('/estudiantes', methods=['POST'])
@jwt_required()
@cross_origin()
def estudiantes():
    return jsonify(model.get_estudiantes())