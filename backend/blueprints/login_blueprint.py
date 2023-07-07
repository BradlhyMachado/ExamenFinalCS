from flask import Flask
from flask import Blueprint
from flask import request
from flask import jsonify
from werkzeug.utils import secure_filename
import json
from flask_cors import CORS, cross_origin 

from backend.models.login_model import loginModel
model = loginModel()

login_blueprint = Blueprint('login_blueprint', __name__)

@login_blueprint.route('/login', methods=['POST'])
def login():
    content = model.login(request.json['usuario_correo'], request.json['usuario_contrasena'])    
    return jsonify(content)