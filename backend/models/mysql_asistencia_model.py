from backend.models.mysql_connection_pool import MySQLPool

class asistenciaModel:
    def __init__(self):        
        self.mysql_pool = MySQLPool()

    def __del__(self):
        if hasattr(self, 'mysql_pool') and self.mysql_pool:
            self.mysql_pool.close()
            
    def get_asistencia(self, id_asistencia):    
        params = {'id_asistencia' : id_asistencia}      
        rv = self.mysql_pool.execute("SELECT * from Asistencia A inner join Usuario U on A.dni = U.dni where A.id_asistencia = %(id_asistencia)s", params)                
        data = []
        content = {}
        for result in rv:
            content = {'id_asistencia': result[0], 'fecha': str(result[1]), 'hora_entrada': str(result[2]), 'dni': result[3], "Nombre" : result[6] + result[7]}
            data.append(content)
            content = {}
        return data

    def get_asistencias(self):  
        rv = self.mysql_pool.execute("SELECT * from Asistencia A inner join Usuario U on A.dni = U.dni")  
        data = []
        content = {}
        for result in rv:
            content = {'id_asistencia': result[0], 'fecha': str(result[1]), 'hora_entrada': str(result[2]), 'dni': result[3], "Nombre" : result[6] + result[7]}
            data.append(content)
            content = {}
        return data

    def create_asistencia(self, fecha, hora_entrada, hora_salida, dni, id_horario):    
        data = {
            'fecha' : fecha,
            'hora_entrada' : hora_entrada,
            'hora_salida': hora_salida,
            'dni': dni,
            'id_horario': id_horario
        }  
        query = """insert into Asistencia(fecha, hora_entrada, hora_salida, dni, id_horario) 
            values (%(fecha)s, %(hora_entrada)s, %(hora_salida)s, %(dni)s, %(id_horario)s)"""    
        cursor = self.mysql_pool.execute(query, data, commit=True)   

        data['id_asistencia'] = cursor.lastrowid
        return data

    def update_asistencia(self, id_asistencia, fecha, hora_entrada, hora_salida, dni, id_horario):    
        data = {
            'id_asistencia' : id_asistencia,
            'fecha' : fecha,
            'hora_entrada' : hora_entrada,
            'hora_salida': hora_salida,
            'dni': dni,
            'id_horario': id_horario
        }   
        query = """update Asistencia set fecha = %(fecha)s, hora_entrada = %(hora_entrada)s, hora_salida= %(hora_salida)s, 
        dni = %(dni)s, id_horario = %(id_horario)s where id_asistencia = %(id_asistencia)s"""    
        cursor = self.mysql_pool.execute(query, data, commit=True)   

        result = {'result':1} 
        return result

    def delete_asistencia(self, id_asistencia):    
        params = {'id_asistencia' : id_asistencia}      
        query = """delete from Asistencia where id_asistencia = %(id_asistencia)s"""    
        self.mysql_pool.execute(query, params, commit=True)   

        result = {'result': 1}
        return result 