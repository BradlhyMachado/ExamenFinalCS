from backend.models.mysql_connection_pool import MySQLPool
import requests
from flask import request
from flask import json
import ast
import re
import datetime
import numpy as np

from backend.models.mysql_usuario_model import usuarioModel
from backend.models.mysql_asistencia_model import asistenciaModel

class tomarAsistenciaModel:
    def __init__(self):        
        self.mysql_pool = MySQLPool()

    def crear_asistencia(self, dni, foto):    
        id_horario = self.validar_horario_clases(dni)
        
        if id_horario is None:
            data = {
                'horario': False,
                'dist': 2
            }
        else:
            response = requests.post("http://localhost:81/openfaceAPI", files=dict(file=foto))
            aux = response.text                         
            vectorInp = json.loads(aux)['result']

            modelo = usuarioModel()
            alumno = modelo.get_usuario(dni)
            vectorInt = alumno[0]["usuario_vector"]

            #vecstr1 = re.sub("\s+", ',', vectorInp)
            #vecstr2 = re.sub("\s+", ',', vectorInt)
            vecstr1 =vectorInp.replace('[', '').replace(']', '').split()
            vecstr2 =vectorInt.replace('[', '').replace(']', '').split()
            
            try:
                #vector1 = np.array(ast.literal_eval(vecstr1))
                #vector2 = np.array(ast.literal_eval(vecstr2))
                vector1 = np.array([float(numeric_string) for numeric_string in vecstr1])
                vector2 = np.array([float(numeric_string) for numeric_string in vecstr2])

                dist = np.linalg.norm(vector1-vector2)

                if (dist < 0.6):
                    data = {
                        'fecha' : datetime.date.today().strftime('%Y-%m-%d'),
                        'hora_entrada' : datetime.datetime.now().strftime('%H:%M:%S'),
                        'dni': dni,
                        'id_horario': id_horario
                    }

                    query = """insert into Asistencia(fecha, hora_entrada, dni, id_horario) 
                    values (%(fecha)s, %(hora_entrada)s, %(dni)s, %(id_horario)s)"""
                    cursor = self.mysql_pool.execute(query, data, commit=True)

                    if cursor is not None:
                        data['id_asistencia'] = cursor.lastrowid
                    else:
                        raise Exception("Error: Cursor is None in create_asistencia")

                data['horario'] = True
                data['dist'] = dist

            except (SyntaxError, ValueError) as e:
                data = {}
                return data
        return data
    
    def validar_horario_clases(self, dni):
        current_datetime = datetime.datetime.now()
        current_day_of_week = current_datetime.strftime('%A')
        current_time = current_datetime.strftime('%H:%M:%S')

        query = """
        SELECT h.id_horario
        FROM Usuario u
        INNER JOIN Estudiante e ON u.dni = e.dni
        INNER JOIN Matricula m ON e.id_estudiante = m.id_estudiante
        INNER JOIN Seccion s ON m.id_seccion = s.id_seccion
        INNER JOIN Horario h ON s.id_seccion = h.id_seccion
        WHERE u.dni = %(dni)s
        AND h.dia_semana = %(current_day_of_week)s
        AND %(current_time)s >= h.hora_inicio
        AND %(current_time)s <= h.hora_fin
        """

        data = {
            'dni': dni,
            'current_day_of_week': current_day_of_week,
            'current_time': current_time
        }

        cursor = self.mysql_pool.execute(query, data)
        result = cursor

        if result:
            return result[0][0] if result[0][0] else None
        else:
            return None