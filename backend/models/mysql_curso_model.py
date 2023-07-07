from backend.models.mysql_connection_pool import MySQLPool

class cursoModel:
    def __init__(self):        
        self.mysql_pool = MySQLPool()

    def __del__(self):
        if hasattr(self, 'mysql_pool') and self.mysql_pool:
            self.mysql_pool.close()
            
    def get_curso(self, id_curso):    
        params = {'id_curso' : id_curso}      
        rv = self.mysql_pool.execute("""SELECT * from Curso where id_curso = %(id_curso)s""", params)                
        data = []
        content = {}
        for result in rv:
            content = {'id_curso': result[0], 'curso_nombre': result[1]}
            data.append(content)
            content = {}
        return data

    def get_cursos(self):  
        rv = self.mysql_pool.execute("SELECT * from Curso")  
        data = []
        content = {}
        for result in rv:
            content = {'id_curso': result[0], 'curso_nombre': result[1]}
            data.append(content)
            content = {}
        return data

    def create_curso(self, curso_nombre):    
        data = {
            'curso_nombre' : curso_nombre
        }  
        query = """insert into Curso(nombre_curso)
                values (%(curso_nombre)s)"""    
        cursor = self.mysql_pool.execute(query, data, commit=True)   

        data['id_curso'] = cursor.lastrowid
        return data
    
    def update_curso(self, id_curso ,nombre_curso):    
        data = {
            'id_curso' : id_curso,
            'nombre_curso' : nombre_curso
        }  
        query = """update Curso set nombre_curso = %(nombre_curso)s where id_curso = %(id_curso)s"""    
        cursor = self.mysql_pool.execute(query, data, commit=True)   

        result = {'result':1} 
        return result

    def delete_curso(self, id_curso):    
        params = {'id_curso' : id_curso}      
        query = """delete from Curso where id_curso = %(id_curso)s"""    
        self.mysql_pool.execute(query, params, commit=True)   

        data = {'result': 1}
        return data