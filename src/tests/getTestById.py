from models.entities.Test import Test, test_schema

def getTestById(testId):
    test = Test.query.get(testId)

    if(test == None):
        return {
            "message": "No existe una Prueba con el ID ingresado"
        }
    return test_schema.jsonify(test)