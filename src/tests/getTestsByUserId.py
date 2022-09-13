from run import app, db
from models.entities.Test import Test, tests_schema
from sqlalchemy import desc

def getTestByUserId(userId):
    userTests = Test.query.filter(Test.user_id == userId).order_by(desc(Test.id)).all()
    return tests_schema.jsonify(userTests)