from flask import Flask
from flask import Blueprint
from flask import request
from flask import jsonify
from werkzeug.utils import secure_filename
import json
from flask_cors import CORS, cross_origin 
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity

from backend.models.mysql_grupoUsuario_model import grupoUsuarioModel
model = grupoUsuarioModel()

grupoUsuario_blueprint = Blueprint('grupoUsuario_blueprint', __name__)

@grupoUsuario_blueprint.route('/grupoUsuario', methods=['PUT'])
@cross_origin()
@jwt_required()
def create_grupoUsuario():
    content = model.create_grupoUsuario(request.json['nombre_grupo']) 
    return jsonify(content)

@grupoUsuario_blueprint.route('/grupoUsuario', methods=['PATCH'])
@jwt_required()
@cross_origin()
def update_grupoUsuario():
    content = model.update_grupoUsuario(request.json['id_grupo_usuario'], request.json['nombre_grupo'])     
    return jsonify(content)

@grupoUsuario_blueprint.route('/grupoUsuario', methods=['DELETE'])
@jwt_required()
@cross_origin()
def delete_grupoUsuario():
    return jsonify(model.delete_grupoUsuario(int(request.json['id_grupo_usuario'])))

@grupoUsuario_blueprint.route('/grupoUsuario', methods=['POST'])
@cross_origin()
def grupoUsuario():
    return jsonify(model.get_grupoUsuario(int(request.json['id_grupo_usuario'])))

@grupoUsuario_blueprint.route('/grupoUsuarios', methods=['POST'])
@jwt_required()
@cross_origin()
def grupoUsuarios():
    current_user = get_jwt_identity()
    return jsonify(model.get_grupoUsuarios())