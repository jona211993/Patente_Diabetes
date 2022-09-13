from run import app, db
from models.entities.Test import Test, test_schema

def deleteTestById(testId):
    test = Test.query.get(testId)

    if(test==None):
        return {
            "message": "Ya se eliminó esta prueba"
        }

    db.session.delete(test)
    db.session.commit()
    return test_schema.jsonify(test)