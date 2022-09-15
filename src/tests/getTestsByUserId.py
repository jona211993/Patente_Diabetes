from run import app, db
from models.entities.Prueba import Prueba, tests_schema
from sqlalchemy import desc

def getTestByUserId(userId):
    userTests = Prueba.query.filter(Prueba.user_id == userId).order_by(desc(Prueba.id)).all()
    return tests_schema.jsonify(userTests)