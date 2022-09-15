from .entities.Usuario import Usuario
from run import db


class ModeloUsuario():

    @classmethod
    def loginA(self, dbA, usuario):
        try:
            cursor = dbA.connection.cursor()
            sql = """SELECT id, nombre_usuario, contrasenia, nombres FROM usuario 
                    WHERE nombre_usuario = '{}'""".format(usuario.nombre_usuario)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                usuario = Usuario(row[0], row[1], Usuario.check_password(
                    row[2], usuario.contrasenia), row[3])
                return usuario
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def login(self, nombre_usuario, contrasenia):
        try:
            usuario = Usuario.query.get(nombre_usuario == nombre_usuario)

            if usuario != None:
                if(usuario.contrasenia == contrasenia):
                    return usuario
                else:
                    return 1
            else:
                return 1
        except Exception as ex:
            print(ex)
            raise Exception(ex)

    @classmethod
    def obtener_por_id(self, db, id):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT id, nombre_usuario, nombres FROM usuario WHERE id = {}".format(
                id)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                return Usuario(row[0], row[1], None, row[2])
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
