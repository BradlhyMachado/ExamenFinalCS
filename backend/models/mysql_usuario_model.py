from flask import json
import requests
import re
import ast
import numpy as np

from backend.models.mysql_connection_pool import MySQLPool

class usuarioModel:
    def __init__(self):        
        self.mysql_pool = MySQLPool()
    
    """def __del__(self):
        if hasattr(self, 'mysql_pool') and self.mysql_pool:
            self.mysql_pool.close()"""

    def get_usuario(self, usuario_dni):    
        params = {'usuario_dni' : usuario_dni}      
        rv = self.mysql_pool.execute("SELECT * from Usuario U inner join GrupoUsuario GU on U.id_grupo = GU.id_grupo where dni=%(usuario_dni)s", params)                
        data = []
        content = {}
        for result in rv:
            content = {'usuario_dni': result[0], 'usuario_nombre': result[1], 'usuario_apellido': result[2], 'usuario_telefono': result[3], 'usuario_correo': result[4], "usuario" : result[-1], "usuario_vector" : result[8], "usuario_ruta" : result[7]}
            data.append(content)
            content = {}
        return data

    def get_usuarios(self):  
        rv = self.mysql_pool.execute("SELECT * from Usuario U inner join GrupoUsuario GU on U.id_grupo = GU.id_grupo")  
        data = []
        content = {}
        for result in rv:
            content = {'usuario_dni': result[0], 'usuario_nombre': result[1], 'usuario_apellido': result[2], 'usuario_telefono': result[3], 'usuario_correo': result[4], "usuario" : result[-1], "usuario_vector" : result[8], "usuario_ruta" : result[7]}
            data.append(content)
            content = {}
        return data

    def create_usuario(self, usuario_dni ,usuario_nombre, usuario_apellido, usuario_telefono, usuario_correo, usuario_contraseña, usuario_id_grupo, usuario_ruta):    
        #########################################################################
        ruta = usuario_ruta
        with open(ruta, "rb") as archivo:
            response = requests.post("http://localhost:81/openfaceAPI", files={"file": archivo})
        aux = response.text                         
        usuario_vector = json.loads(aux)['result']
        #########################################################################
        data = {
            'usuario_dni' : usuario_dni,
            'usuario_nombre' : usuario_nombre,
            'usuario_apellido' : usuario_apellido,
            'usuario_telefono': usuario_telefono,
            'usuario_correo': usuario_correo,
            'usuario_contraseña': usuario_contraseña,
            'usuario_id_grupo' : usuario_id_grupo,
            'usuario_vector' : usuario_vector,
            'usuario_ruta' : usuario_ruta
        } 
        query = """insert into Usuario(dni, nombre, apellido, telefono, correo, contrasena, id_grupo, vector, ruta) 
            values (%(usuario_dni)s, %(usuario_nombre)s, %(usuario_apellido)s, %(usuario_telefono)s, %(usuario_correo)s, %(usuario_contraseña)s, %(usuario_id_grupo)s, %(usuario_vector)s, %(usuario_ruta)s)"""    
        cursor = self.mysql_pool.execute(query, data, commit=True)   

        data['usuario_dni'] = cursor.lastrowid
        return data

    def update_usuario(self, usuario_dni ,usuario_nombre, usuario_apellido, usuario_telefono, usuario_correo, usuario_contraseña, usuario_id_grupo, usuario_ruta):    
        #########################################################################
        ruta = usuario_ruta
        with open(ruta, "rb") as archivo:
            response = requests.post("http://localhost:81/openfaceAPI", files={"file": archivo})
        aux = response.text                         
        usuario_vector = json.loads(aux)['result']
        #########################################################################
        data = {
            'usuario_dni' : usuario_dni,
            'usuario_nombre' : usuario_nombre,
            'usuario_apellido' : usuario_apellido,
            'usuario_telefono': usuario_telefono,
            'usuario_correo': usuario_correo,
            'usuario_contraseña': usuario_contraseña,
            'usuario_id_grupo' : usuario_id_grupo,
            'usuario_vector' : usuario_vector,
            'usuario_ruta' : usuario_ruta
        }  
        query = """update Usuario set nombre = %(usuario_nombre)s, apellido = %(usuario_apellido)s, telefono= %(usuario_telefono)s, 
        correo = %(usuario_correo)s, contrasena = %(usuario_contraseña)s, id_grupo = %(usuario_id_grupo)s, vector = %(usuario_vector)s, ruta = %(usuario_ruta)s where dni = %(usuario_dni)s"""    
        cursor = self.mysql_pool.execute(query, data, commit=True)   

        result = {'result':1} 
        return result

    def delete_usuario(self, usuario_dni):    
        params = {'usuario_dni' : usuario_dni}      
        query = """delete from Usuario where dni = %(usuario_dni)s"""    
        self.mysql_pool.execute(query, params, commit=True)   

        result = {'result': 1}
        return result 