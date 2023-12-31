from flask import Flask
from flask import Blueprint
from flask import request
from flask import jsonify
from werkzeug.utils import secure_filename
import json
from flask_cors import CORS, cross_origin
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity 

from backend.models.mysql_horario_model import horarioModel
model = horarioModel()

horario_blueprint = Blueprint('horario_blueprint', __name__)

@horario_blueprint.route('/horario', methods=['PUT'])
@jwt_required()
@cross_origin()
def create_horario():
    content = model.create_horario(request.json['dia_semana'], request.json['hora_inicio'], request.json['hora_fin'], request.json['id_seccion'])    
    return jsonify(content)

@horario_blueprint.route('/horario', methods=['PATCH'])
@jwt_required()
@cross_origin()
def update_horario():
    content = model.update_horario(request.json['id_horario'], request.json['dia_semana'], request.json['hora_inicio'], request.json['hora_fin'], request.json['id_seccion'])     
    return jsonify(content)

@horario_blueprint.route('/horario', methods=['DELETE'])
@jwt_required()
@cross_origin()
def delete_horario():
    return jsonify(model.delete_horario(int(request.json['id_horario'])))

@horario_blueprint.route('/horario', methods=['POST'])
@cross_origin()
def horario():
    return jsonify(model.get_horario(int(request.json['id_horario'])))

@horario_blueprint.route('/horarios', methods=['POST'])
@jwt_required()
@cross_origin()
def horarios():
    return jsonify(model.get_horarios())