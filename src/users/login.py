from models.entities.Usuario import Usuario
from run import db


def loginNormal(nombre_usuario, contrasenia):
    usuario = Usuario.query.get(nombre_usuario == nombre_usuario)
    print("USAWEA", usuario)
    if usuario != None:
        return usuario
    else:
        return None
