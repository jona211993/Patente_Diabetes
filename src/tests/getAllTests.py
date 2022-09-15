from run import app, db
from models.entities.Prueba import Prueba, pruebas_esquema
from sqlalchemy import desc

def getAllTests():
    allTests = Prueba.query.order_by(desc(Prueba.id)).all()
    return pruebas_esquema.jsonify(allTests)