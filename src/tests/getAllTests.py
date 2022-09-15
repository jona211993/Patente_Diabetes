from run import app, db
from models.entities.Prueba import Prueba, tests_schema
from sqlalchemy import desc

def getAllTests():
    allTests = Prueba.query.order_by(desc(Prueba.id)).all()
    return tests_schema.jsonify(allTests)