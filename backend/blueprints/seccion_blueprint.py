from flask import Flask
from flask import Blueprint
from flask import request
from flask import jsonify
from werkzeug.utils import secure_filename
import json
from flask_cors import CORS, cross_origin
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity 

from backend.models.mysql_seccion_model import seccionModel
model = seccionModel()

seccion_blueprint = Blueprint('seccion_blueprint', __name__)

@seccion_blueprint.route('/seccion', methods=['PUT'])
@jwt_required()
@cross_origin()
def create_seccion():
    content = model.create_seccion(request.json['nombre_seccion'], request.json['id_curso'])    
    return jsonify(content)

@seccion_blueprint.route('/seccion', methods=['PATCH'])
@jwt_required()
@cross_origin()
def update_seccion():
    content = model.update_seccion(request.json['id_seccion'], request.json['nombre_seccion'], request.json['id_curso'])     
    return jsonify(content)

@seccion_blueprint.route('/seccion', methods=['DELETE'])
@jwt_required()
@cross_origin()
def delete_seccion():
    return jsonify(model.delete_seccion(int(request.json['id_seccion'])))

@seccion_blueprint.route('/seccion', methods=['POST'])
@cross_origin()
def seccion():
    return jsonify(model.get_seccion(int(request.json['id_seccion'])))

@seccion_blueprint.route('/seccions', methods=['POST'])
@jwt_required()
@cross_origin()
def seccions():
    return jsonify(model.get_seccions())