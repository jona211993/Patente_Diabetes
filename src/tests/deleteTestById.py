from run import app, db
from models.entities.Prueba import Prueba, prueba_esquema

def deleteTestById(testId):
    test = Prueba.query.get(testId)

    if(test==None):
        return {
            "message": "Ya se eliminó esta prueba"
        }

    db.session.delete(test)
    db.session.commit()
    return prueba_esquema.jsonify(test)