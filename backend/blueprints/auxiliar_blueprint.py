from flask import Flask
from flask import Blueprint
from flask import request
from flask import jsonify
from werkzeug.utils import secure_filename
import json
from flask_cors import CORS, cross_origin 

from backend.models.mysql_auxiliar_model import auxiliarModel
model = auxiliarModel()

auxiliar_blueprint = Blueprint('auxiliar_blueprint', __name__)
@auxiliar_blueprint.route('/seccionByHorario', methods=['POST'])
def seccionByHorario():
    content = model.seccionByHorario(request.json['nombre_seccion'])    
    return jsonify(content)

@auxiliar_blueprint.route('/seccionByEstudiante', methods=['POST'])
def seccionByEstudiante():
    content = model.seccionByEstudiante(request.json['nombre_seccion'])    
    return jsonify(content)

@auxiliar_blueprint.route('/uploadFile', methods=['POST'])
def uploadFile():
    file = request.files['foto']
    data = model.upload_file(file)
    return jsonify(data), 201