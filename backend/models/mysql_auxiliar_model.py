import datetime
import os

from werkzeug.utils import secure_filename
from backend.models.mysql_connection_pool import MySQLPool

class auxiliarModel:
    def __init__(self):        
        self.mysql_pool = MySQLPool()

    def seccionByHorario(self, nombre_seccion):
        params = {'nombre_seccion' : nombre_seccion}      
        rv = self.mysql_pool.execute("""select h.id_horario from Seccion s
                                    inner join Horario h on s.id_seccion = h.id_seccion
                                    where s.nombre_seccion = %(nombre_seccion)s;""", params)
        
        data = []
        content = {}
        for result in rv:
            content = {'id_horario': result[0]}
            data.append(content)
            content = {}
        return data

    def seccionByEstudiante(self, nombre_seccion):
        params = {'nombre_seccion' : nombre_seccion}      
        rv = self.mysql_pool.execute("""select concat(u.nombre, ' ', u.apellido) as estudiante, e.id_estudiante from Seccion s
                                    inner join Matricula m on s.id_seccion = m.id_seccion
                                    inner join Estudiante e on m.id_estudiante = e.id_estudiante 
                                    inner join Usuario u on e.dni = u.dni
                                    where s.nombre_seccion = %(nombre_seccion)s;""", params)
              
        data = []
        content = {}
        for result in rv:
            content = {'estudiante': result[0], 'id_estudiante': result[1]}
            data.append(content)
            content = {}
        return data

    def upload_file(self, file):
        # Ruta de la carpeta de destino para guardar las imágenes
        UPLOAD_FOLDER = 'D:/Proyecto/proyecto_final/imagenes'

        # Verificar si la carpeta de destino existe, si no, crearla
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)

        # Obtener el nombre de archivo seguro
        filename = secure_filename(file.filename)

        # Guardar el archivo en la carpeta de destino
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)

        return file_path