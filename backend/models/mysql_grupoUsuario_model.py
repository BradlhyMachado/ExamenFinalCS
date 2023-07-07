from backend.models.mysql_connection_pool import MySQLPool

class grupoUsuarioModel:
    def __init__(self):        
        self.mysql_pool = MySQLPool()

    def __del__(self):
        if hasattr(self, 'mysql_pool') and self.mysql_pool:
            self.mysql_pool.close()
            
    def get_grupoUsuario(self, id_grupo):    
        params = {'id_grupo' : id_grupo}      
        rv = self.mysql_pool.execute("""SELECT * from GrupoUsuario where id_grupo = %(id_grupo)s""", params)                
        data = []
        content = {}
        for result in rv:
            content = {'id_grupo': result[0], 'nombre_grupo': result[1]}
            data.append(content)
            content = {}
        return data

    def get_grupoUsuarios(self):  
        rv = self.mysql_pool.execute("SELECT * from GrupoUsuario")  
        data = []
        content = {}
        for result in rv:
            content = {'id_grupo': result[0], 'nombre_grupo': result[1]}
            data.append(content)
            content = {}
        return data

    def create_grupoUsuario(self, nombre_grupo):    
        data = {
            'nombre_grupo' : nombre_grupo
        }  
        query = """insert into GrupoUsuario(nombre_grupo)
                values (%(nombre_grupo)s)"""    
        grupo_usuario = self.mysql_pool.execute(query, data, commit=True)   

        data['id_grupo'] = grupo_usuario.lastrowid
        return data
    
    def update_grupoUsuario(self, id_grupo ,nombre_grupo):    
        data = {
            'id_grupo' : id_grupo,
            'nombre_grupo' : nombre_grupo
        }  
        query = """update GrupoUsuario set nombre_grupo = %(nombre_grupo)s where id_grupo = %(id_grupo)s"""    
        grupo_usuario = self.mysql_pool.execute(query, data, commit=True)   

        result = {'result':1} 
        return result

    def delete_grupoUsuario(self, id_grupo):    
        params = {'id_grupo' : id_grupo}      
        query = """delete from GrupoUsuario where id_grupo = %(id_grupo)s"""    
        self.mysql_pool.execute(query, params, commit=True)   

        data = {'result': 1}
        return data