import datetime
import os

from flask_jwt_extended import create_access_token
from backend.models.mysql_connection_pool import MySQLPool

class loginModel:
    def __init__(self):        
        self.mysql_pool = MySQLPool()

    def login(self, usuario_correo, usuario_contrasena):
        retorno = {}
        query = """
        SELECT concat(u.nombre, ' ', u.apellido) AS usuario, u.dni, g.nombre_grupo
        FROM Usuario u
        INNER JOIN GrupoUsuario g ON u.id_grupo = g.id_grupo 
        WHERE u.correo = %(usuario_correo)s
        AND u.contrasena = %(usuario_contrasena)s;
        """
        data = {
            'usuario_correo': usuario_correo,
            'usuario_contrasena': usuario_contrasena
        }

        cursor = self.mysql_pool.execute(query, data)

        if cursor:
            access_token = create_access_token(identity=usuario_correo)
            retorno['estado'] = True
            retorno['token'] = access_token=access_token
            retorno['usuario'] = cursor[0][0]
            retorno['dni'] = cursor[0][1]
            retorno['nombre_grupo'] = cursor[0][2]
            return retorno
        else:
            retorno['estado'] = False
            retorno['token'] = None
            retorno['usuario'] = None
            retorno['dni'] = None
            retorno['nombre_grupo'] = None
            return retorno