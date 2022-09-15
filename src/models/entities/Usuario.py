
from flask_login import UserMixin
# from werkzeug.security import generate_password_hash, check_password_hash
from run import db, ma


class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    nombre_usuario = db.Column(db.String(70), nullable=False, unique=True)
    contrasenia = db.Column(db.String(255))
    nombres = db.Column(db.String(255))
    numero_documento_dni = db.Column(db.String(8), nullable=False)
    edad = db.Column(db.Integer, nullable=False)
    correo_electronico = db.Column(db.String(255), unique=True, nullable=False)
    sexo = db.Column(db.String(1), nullable=False)
    tests = db.relationship('Prueba', backref='usuario', lazy=True)

    def __init__(self, id, nombre_usuario, contrasenia, nombres="") -> None:
        self.id = id
        self.nombre_usuario = nombre_usuario
        self.contrasenia = contrasenia
        self.nombres = nombres


    def setId(self, id):
        self.id = id
        return self

    def setNombreUsuario(self, nombre_usuario):
        self.nombre_usuario = nombre_usuario
        return self

    def setContrasenia(self, contrasenia):
        self.contrasenia = contrasenia
        return self

    def setNombres(self, nombres):
        self.nombres = nombres
        return self

    def setNumeroDocumentoDni(self, numero_documento_dni):
        self.numero_documento_dni = numero_documento_dni
        return self

    def setEdad(self, edad):
        self.edad = edad
        return edad

    def setCorreoElectronico(self, correo_electronico):
        self.correo_electronico = correo_electronico
        return self

    def setSexo(self, sexo):
        self.sexo = sexo
        return self

    def __repr__(self):
        return f'<Usuario {self.correo_electronico}>'

    def set_password(self, contrasenia):
        self.contrasenia = generate_password_hash(contrasenia)

    def check_password(self, contrasenia):
        return check_password_hash(self.contrasenia, contrasenia)

    def guardar(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    @staticmethod
    def obtener_por_id(id):
        return Usuario.query.get(id)

    @staticmethod
    def obtener_por_correo_electronico(correo_electronico):
        return Usuario.query.filter_by(correo_electronico=correo_electronico).first()

    @classmethod
    def check_password(self, hashed_password, contrasenia):
        return check_password_hash(hashed_password, contrasenia)


class UsuarioEsquema(ma.Schema):
    class Meta:
        fields = ('id', 'nombre_usuario', 'nombres', 'numero_documento_dni',
                  'edad', 'correo_electronico', 'sexo', 'tests')


usuario_esquema = UsuarioEsquema()
usuarios_esquema = UsuarioEsquema(many=True)
