from run import app, db
from models.entities.Prueba import Prueba, test_schema

def deleteTestById(testId):
    test = Prueba.query.get(testId)

    if(test==None):
        return {
            "message": "Ya se eliminó esta prueba"
        }

    db.session.delete(test)
    db.session.commit()
    return test_schema.jsonify(test)