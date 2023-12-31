from flask import Flask
from flask import request
from flask import jsonify
from flask import render_template
from flask_cors import CORS, cross_origin
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

from backend.blueprints.curso_blueprint import curso_blueprint
from backend.blueprints.usuario_blueprint import usuario_blueprint
from backend.blueprints.grupoUsuario_blueprint import grupoUsuario_blueprint
from backend.blueprints.profesor_blueprint import profesor_blueprint
from backend.blueprints.seccion_blueprint import seccion_blueprint
from backend.blueprints.estudiante_blueprint import estudiante_blueprint
from backend.blueprints.asistencia_blueprint import asistencia_blueprint
from backend.blueprints.horario_blueprint import horario_blueprint
from backend.blueprints.justificacion_blueprint import justificacion_blueprint
from backend.blueprints.participacion_blueprint import participacion_blueprint
from backend.blueprints.matricula_blueprint import matricula_blueprint
from backend.blueprints.tomarAsistencia_blueprint import tomarAsistencia_blueprint
from backend.blueprints.auxiliar_blueprint import auxiliar_blueprint
from backend.blueprints.login_blueprint import login_blueprint

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = 'Clave'
jwt = JWTManager(app)

app.register_blueprint(curso_blueprint)
app.register_blueprint(usuario_blueprint)
app.register_blueprint(grupoUsuario_blueprint)
app.register_blueprint(profesor_blueprint)
app.register_blueprint(seccion_blueprint)
app.register_blueprint(estudiante_blueprint)
app.register_blueprint(asistencia_blueprint)
app.register_blueprint(horario_blueprint)
app.register_blueprint(justificacion_blueprint)
app.register_blueprint(participacion_blueprint)
app.register_blueprint(matricula_blueprint)
app.register_blueprint(tomarAsistencia_blueprint)
app.register_blueprint(auxiliar_blueprint)
app.register_blueprint(login_blueprint)

cors = CORS(app)

if __name__ == "__main__":
    app.run(debug=True)