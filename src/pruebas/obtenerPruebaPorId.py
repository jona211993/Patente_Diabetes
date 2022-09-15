from models.entities.Prueba import Prueba, prueba_esquema

def obtenerPruebaPorId(testId):
    prueba = Prueba.query.get(testId)

    if(prueba == None):
        return {
            "message": "No existe una Prueba con el ID ingresado"
        }
    return prueba_esquema.jsonify(prueba)