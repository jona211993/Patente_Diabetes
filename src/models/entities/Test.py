from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from run import db, ma


class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    alimentation = db.Column(db.Float, nullable=False)
    genetical = db.Column(db.Float, nullable=False)
    glucose = db.Column(db.Float, nullable=False)
    physical_activity = db.Column(db.Float, nullable=False)

    absolute_value = db.Column(db.Float, nullable=False)
    low_pertenence_grade = db.Column(db.Float, nullable=False)
    mid_pertenence_grade = db.Column(db.Float, nullable=False)
    high_pertenence_grade = db.Column(db.Float, nullable=False)
    critical_pertenence_grade = db.Column(db.Float, nullable=False)

    result_label = db.Column(db.String(31), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def setAlimentation(self, alimentation):
        self.alimentation = alimentation
        return self

    def setGenetical(self, genetical):
        self.genetical = genetical
        return self

    def setGlucose(self, glucose):
        self.glucose = glucose
        return self

    def setPhysicalActivity(self, physicalActivity):
        self.physical_activity = physicalActivity
        return self

    def setAbsoluteValue(self, absoluteValue):
        self.absolute_value = absoluteValue
        return self

    def setLowPertenenceGrade(self, low_pertenence_grade):
        self.low_pertenence_grade = low_pertenence_grade
        return self

    def setMidPertenenceGrade(self, mid_pertenence_grade):
        self.mid_pertenence_grade = mid_pertenence_grade
        return self

    def setHighPertenenceGrade(self, high_pertenence_grade):
        self.high_pertenence_grade = high_pertenence_grade
        return self

    def setCriticalPertenenceGrade(self, critical_pertenence_grade):
        self.critical_pertenence_grade = critical_pertenence_grade
        return self

    def setResultLabel(self, result_label):
        self.result_label = result_label
        return self

    def setUserId(self, user_id):
        self.user_id = user_id
        return self


class TestSchema(ma.Schema):
    class Meta:
        fields = ('id', 'alimentation', 'genetical', 'glucose', 'physical_activity', 'absolute_value',
                  'low_pertenence_grade', 'mid_pertenence_grade', 'high_pertenence_grade', 'critical_pertenence_grade'
                  'absolute_value'
                  'low_pertenence_grade'
                  'mid_pertenence_grade'
                  'high_pertenence_grade'
                  'critical_pertenence_grade',
                  'result_label',
                  'user_id'
                  )


test_schema = TestSchema()
tests_schema = TestSchema(many=True)
