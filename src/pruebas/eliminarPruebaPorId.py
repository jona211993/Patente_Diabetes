from run import app, db
from models.entities.Prueba import Prueba, prueba_esquema

def eliminarPruebaPorId(testId):
    prueba = Prueba.query.get(testId)

    if(prueba==None):
        return {
            "message": "Ya se eliminó esta prueba"
        }

    db.session.delete(prueba)
    db.session.commit()
    return prueba_esquema.jsonify(prueba)