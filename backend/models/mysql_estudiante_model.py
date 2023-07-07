from backend.models.mysql_connection_pool import MySQLPool
from backend.models.mysql_usuario_model import usuarioModel

class estudianteModel:
    def __init__(self):        
        self.mysql_pool = MySQLPool()

    def __del__(self):
        if hasattr(self, 'mysql_pool') and self.mysql_pool:
            self.mysql_pool.close()
            
    def get_estudiante(self, dni):    
        params = {'dni' : dni}      
        rv = self.mysql_pool.execute("""SELECT * from Estudiante e inner join Usuario u on e.dni = u.dni where e.dni = %(dni)s""", params)                
        data = []
        content = {}
        for result in rv:
            content = {'id_estudiante': result[0], 'estudiante_dni': result[1], 'estudiante_nombre': result[3]}
            data.append(content)
            content = {}
        return data

    def get_estudiantes(self):  
        rv = self.mysql_pool.execute("SELECT * from Estudiante e inner join Usuario u on e.dni = u.dni")  
        data = []
        content = {}
        for result in rv:
            content = {'id_estudiante': result[0], 'estudiante_dni': result[1], 'nombre': result[3], 'apellidos': result[4], 'telefono': result[5], 'correo': result[6], 'contraseña': result[7], 'ruta': result[9]}
            data.append(content)
            content = {}
        return data

    def create_estudiante(self, dni, usuario_nombre, usuario_apellido, usuario_telefono, usuario_correo, usuario_contraseña, usuario_ruta):    
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
            'usuario_id_grupo': 3,
            'usuario_ruta' : usuario_ruta
        }
        model = usuarioModel()
        model.create_usuario(**usuario_data)
        #----------------------

        query = """insert into Estudiante(dni)
                values (%(dni)s)"""    
        estudiante = self.mysql_pool.execute(query, data, commit=True)   

        data['id_estudiante'] = estudiante.lastrowid
        return data
    
    
    def update_estudiante(self, dni, usuario_nombre, usuario_apellido, usuario_telefono, usuario_correo, usuario_contraseña, usuario_ruta):    
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
    

    def delete_estudiante(self, dni):    
        params = {'dni' : dni}      
        
        query = """delete from Estudiante where dni = %(dni)s"""    
        self.mysql_pool.execute(query, params, commit=True)   

        model = usuarioModel()
        model.delete_usuario(dni)

        data = {'result': 1}
        return data