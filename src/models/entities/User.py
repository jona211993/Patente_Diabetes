
from flask_login import UserMixin
# from werkzeug.security import generate_password_hash, check_password_hash
from run import db, ma


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(70), nullable=False, unique=True)
    password = db.Column(db.String(255))
    fullname = db.Column(db.String(255))
    documentNumber = db.Column(db.String(8), nullable=False)
    edad = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    sex = db.Column(db.String(1), nullable=False)
    tests = db.relationship('Prueba', backref='user', lazy=True)

    def __init__(self, id, username, password, fullname="") -> None:
        self.id = id
        self.username = username
        self.password = password
        self.fullname = fullname


    def setId(self, id):
        self.id = id
        return self

    def setUsername(self, username):
        self.username = username
        return self

    def setPassword(self, password):
        self.password = password
        return self

    def setFullname(self, fullname):
        self.fullname = fullname
        return self

    def setNumeroDocumentoDni(self, documentNumber):
        self.documentNumber = documentNumber
        return self

    def setEdad(self, edad):
        self.edad = edad
        return edad

    def setEmail(self, email):
        self.email = email
        return self

    def setSex(self, sex):
        self.sex = sex
        return self

    def __repr__(self):
        return f'<User {self.email}>'

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_by_id(id):
        return User.query.get(id)

    @staticmethod
    def get_by_email(email):
        return User.query.filter_by(email=email).first()

    @classmethod
    def check_password(self, hashed_password, password):
        return check_password_hash(hashed_password, password)


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'fullname', 'documentNumber',
                  'edad', 'email', 'sex', 'tests')


user_schema = UserSchema()
users_schema = UserSchema(many=True)
