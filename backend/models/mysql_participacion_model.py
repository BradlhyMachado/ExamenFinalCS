import datetime

from backend.models.mysql_connection_pool import MySQLPool

class participacionModel:
    def __init__(self):        
        self.mysql_pool = MySQLPool()
            
    def get_participacion(self, id_participacion):    
        params = {'id_participacion' : id_participacion}      
        rv = self.mysql_pool.execute("""SELECT p.id_participacion, p.nota_final, s.nombre_seccion, concat(u.nombre, ' ', u.apellido) as estudiante from Participacion p 
                                    inner join Horario h on p.id_horario = h.id_horario 
                                    inner join Seccion s on h.id_seccion = s.id_seccion
                                    inner join Estudiante e on p.id_estudiante = e.id_estudiante
                                    inner join Usuario u on e.dni = u.dni where p.id_participacion=%(id_participacion)s""", params)              
        data = []
        content = {}
        for result in rv:
            content = {'id_participacion': result[0], 'fecha': result[1], 'nota_final': result[2], 'id_horario': result[3], 'nombre_seccion': result[11]}
            data.append(content)
            content = {}
        return data

    def get_participacions(self):  
        rv = self.mysql_pool.execute("""SELECT p.id_participacion, p.nota_final, s.nombre_seccion, concat(u.nombre, ' ', u.apellido) as estudiante from Participacion p 
                                    inner join Horario h on p.id_horario = h.id_horario 
                                    inner join Seccion s on h.id_seccion = s.id_seccion
                                    inner join Estudiante e on p.id_estudiante = e.id_estudiante
                                    inner join Usuario u on e.dni = u.dni""")  
        data = []
        content = {}
        for result in rv:
            content = {'id_participacion': result[0], 'nota_final': result[1], 'nombre_seccion': result[2], 'estudiante': result[3]}
            data.append(content)
            content = {}
        return data

    def create_participacion(self, nota_final, id_horario, id_estudiante):    
        data = {
            'fecha' : datetime.date.today().strftime('%Y-%m-%d'),
            'nota_final' : nota_final,
            'id_horario' : id_horario,
            'id_estudiante' : id_estudiante
        }  
        query = """insert into Participacion(fecha, nota_final, id_horario, id_estudiante) 
        values (%(fecha)s, %(nota_final)s, %(id_horario)s, %(id_estudiante)s)""" 
        cursor = self.mysql_pool.execute(query, data, commit=True)   

        data['id_participacion'] = cursor.lastrowid
        return data

    def update_participacion(self, id_participacion, nota_final):    
        data = {
            'id_participacion' : id_participacion,
            'nota_final' : nota_final
        }  
        query = """update Participacion set nota_final = %(nota_final)s
                    where id_participacion = %(id_participacion)s"""    
        cursor = self.mysql_pool.execute(query, data, commit=True)   
        result = {'result':1} 
        return result

    def delete_participacion(self, id_participacion):    
        params = {'id_participacion' : id_participacion}      
        query = """delete from Participacion where id_participacion = %(id_participacion)s"""    
        self.mysql_pool.execute(query, params, commit=True)   
        result = {'result': 1}
        return result 