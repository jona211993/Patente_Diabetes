from run import app, db
from models.entities.Test import Test, tests_schema
from sqlalchemy import desc

def getAllTests():
    allTests = Test.query.order_by(desc(Test.id)).all()
    return tests_schema.jsonify(allTests)