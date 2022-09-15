from run import app, db
from models.entities.Prueba import Prueba, pruebas_esquema
from sqlalchemy import desc

def getTestByUserId(userId):
    userTests = Prueba.query.filter(Prueba.usuario_id == userId).order_by(desc(Prueba.id)).all()
    return pruebas_esquema.jsonify(userTests)