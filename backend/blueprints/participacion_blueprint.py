from flask import Flask
from flask import Blueprint
from flask import request
from flask import jsonify
from werkzeug.utils import secure_filename
import json
from flask_cors import CORS, cross_origin 
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity 

from backend.models.mysql_participacion_model import participacionModel
model = participacionModel()

participacion_blueprint = Blueprint('participacion_blueprint', __name__)

@participacion_blueprint.route('/participacion', methods=['PUT'])
@jwt_required()
@cross_origin()
def create_participacion():
    content = model.create_participacion(request.json['nota_final'], request.json['id_horario'], request.json['id_estudiante'])    
    return jsonify(content)

@participacion_blueprint.route('/participacion', methods=['PATCH'])
@jwt_required()
@cross_origin()
def update_participacion():
    content = model.update_participacion(request.json['id_participacion'], request.json['nota_final'])    
    return jsonify(content)

@participacion_blueprint.route('/participacion', methods=['DELETE'])
@jwt_required()
@cross_origin()
def delete_participacion():
    return jsonify(model.delete_participacion(int(request.json['id_participacion'])))

@participacion_blueprint.route('/participacion', methods=['POST'])
@cross_origin()
def participacion():
    return jsonify(model.get_participacion(int(request.json['id_participacion'])))

@participacion_blueprint.route('/participacions', methods=['POST'])
@jwt_required()
@cross_origin()
def participacions():
    return jsonify(model.get_participacions())