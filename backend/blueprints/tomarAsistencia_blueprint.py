from flask import Flask
from flask import Blueprint
from flask import request
from flask import jsonify
from werkzeug.utils import secure_filename
import json
from flask_cors import CORS, cross_origin 

from backend.models.tomarAsistencia_model import tomarAsistenciaModel

tomarAsistencia_blueprint = Blueprint('tomarAsistencia_blueprint', __name__)
@tomarAsistencia_blueprint.route('/tomarAsistencia', methods=['POST'])
def crear_asistencia():
    dni = request.form['dni']
    foto = request.files['foto']
    tm = tomarAsistenciaModel()
    data = tm.crear_asistencia(dni, foto)
    return jsonify(data), 201