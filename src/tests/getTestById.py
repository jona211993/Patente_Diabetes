from models.entities.Prueba import Prueba, prueba_esquema

def getTestById(testId):
    test = Prueba.query.get(testId)

    if(test == None):
        return {
            "message": "No existe una Prueba con el ID ingresado"
        }
    return prueba_esquema.jsonify(test)