from backend.models.mysql_connection_pool import MySQLPool
from backend.models.mysql_usuario_model import usuarioModel

class profesorModel:
    def __init__(self):        
        self.mysql_pool = MySQLPool()

    def get_profesor(self, id_profesor):    
        params = {'id_profesor' : id_profesor}      
        rv = self.mysql_pool.execute("""SELECT * from Profesor e inner join Usuario u on e.dni = u.dni where id_profesor = %(id_profesor)s""", params)                
        data = []
        content = {}
        for result in rv:
            content = {'id_profesor': result[0], 'profesor_dni': result[1], 'nombre': result[3], 'apellidos': result[4]}
            data.append(content)
            content = {}
        return data

    def get_profesors(self):  
        rv = self.mysql_pool.execute("SELECT * from Profesor p inner join Usuario u on p.dni = u.dni")  
        data = []
        content = {}
        for result in rv:
            content = {'id_profesor': result[0], 'profesor_dni': result[1], 'nombre': result[3], 'apellidos': result[4], 'telefono': result[5], 'correo': result[6], 'contraseña': result[7], 'ruta': result[9]}
            data.append(content)
            content = {}
        return data

    def create_profesor(self, dni, usuario_nombre, usuario_apellido, usuario_telefono, usuario_correo, usuario_contraseña, usuario_ruta):    
        data = {
            'dni' : dni
        }  

        #Crear usuario
        usuario_data = {
            'usuario_dni': dni,
            'usuario_nombre': usuario_nombre,
            'usuario_apellido': usuario_apellido,
            'usuario_telefono': usuario_telefono,
            'usuario_correo': usuario_correo,
            'usuario_contraseña': usuario_contraseña,
            'usuario_id_grupo': 2,
            'usuario_ruta' : usuario_ruta
        }
        model = usuarioModel()
        model.create_usuario(**usuario_data)
        #----------------------
        
        query = """insert into Profesor(dni)
                values (%(dni)s)"""    
        profesor = self.mysql_pool.execute(query, data, commit=True)

        data['id_profesor'] = profesor.lastrowid
        return data
    
    def update_profesor(self, dni, usuario_nombre, usuario_apellido, usuario_telefono, usuario_correo, usuario_contraseña, usuario_ruta):    
        usuario_data = {
            'usuario_dni' : dni,
            'usuario_nombre' : usuario_nombre,
            'usuario_apellido' : usuario_apellido,
            'usuario_telefono': usuario_telefono,
            'usuario_correo': usuario_correo,
            'usuario_contraseña': usuario_contraseña,
            'usuario_id_grupo' : 2,
            'usuario_ruta' : usuario_ruta
        }
        model = usuarioModel()
        model.update_usuario(**usuario_data)
        
        result = {'result':1} 
        return result

    def delete_profesor(self, dni):    
        params = {'dni' : dni}      

        query = """delete from Profesor where dni = %(dni)s"""    
        self.mysql_pool.execute(query, params, commit=True)   

        model = usuarioModel()
        model.delete_usuario(dni)

        data = {'result': 1}
        return data