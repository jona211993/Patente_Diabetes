from models.entities.Prueba import Prueba, test_schema

def getTestById(testId):
    test = Prueba.query.get(testId)

    if(test == None):
        return {
            "message": "No existe una Prueba con el ID ingresado"
        }
    return test_schema.jsonify(test)