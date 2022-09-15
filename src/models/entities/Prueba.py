from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from run import db, ma


class Prueba(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    nombre = db.Column(db.String(255), nullable = False)
    numero_documento_dni = db.Column(db.String(8), nullable = False)
    edad = db.Column(db.Integer, nullable = False)

    comida = db.Column(db.Float, nullable=False)
    herencia = db.Column(db.Float, nullable=False)
    glucosa = db.Column(db.Float, nullable=False)
    ejercicio = db.Column(db.Float, nullable=False)

    valor_absoluto = db.Column(db.Float, nullable=False)
    grado_pertenencia_bajo = db.Column(db.Float, nullable=False)
    grado_pertenencia_normal = db.Column(db.Float, nullable=False)
    grado_pertenencia_alto = db.Column(db.Float, nullable=False)
    grado_pertenencia_critico = db.Column(db.Float, nullable=False)

    texto_resultado = db.Column(db.String(31), nullable=False)

    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)

    def setNombre(self, nombre):
        self.nombre = nombre
        return self

    def setNumeroDocumentoDni(self, numero_documento_dni):
        self.numero_documento_dni = numero_documento_dni
        return self


    def setEdad(self, edad):
        self.edad = edad
        return self

    def setComida(self, comida):
        self.comida = comida
        return self

    def setHerencia(self, herencia):
        self.herencia = herencia
        return self

    def setGlucosa(self, glucosa):
        self.glucosa = glucosa
        return self

    def setEjercicio(self, ejercicio):
        self.ejercicio = ejercicio
        return self

    def setValorAbsoluto(self, absoluteValue):
        self.valor_absoluto = absoluteValue
        return self

    def setGradoPertenenciaBajo(self, grado_pertenencia_bajo):
        self.grado_pertenencia_bajo = grado_pertenencia_bajo
        return self

    def setGradoPertenenciaNormal(self, grado_pertenencia_normal):
        self.grado_pertenencia_normal = grado_pertenencia_normal
        return self

    def setGradoPertenenciaAlto(self, grado_pertenencia_alto):
        self.grado_pertenencia_alto = grado_pertenencia_alto
        return self

    def setGradoPertenenciaCritico(self, grado_pertenencia_critico):
        self.grado_pertenencia_critico = grado_pertenencia_critico
        return self

    def setTextoResultado(self, texto_resultado):
        self.texto_resultado = texto_resultado
        return self

    def setUsuarioId(self, usuario_id):
        self.usuario_id = usuario_id
        return self


class PruebaEsquema(ma.Schema):
    class Meta:
        fields = ('id', 'nombre', 'numero_documento_dni', 'edad', 'comida', 'herencia', 'glucosa', 'ejercicio', 'valor_absoluto',
                  'grado_pertenencia_bajo', 'grado_pertenencia_normal', 'grado_pertenencia_alto', 'grado_pertenencia_critico'
                  'valor_absoluto'
                  'grado_pertenencia_bajo'
                  'grado_pertenencia_normal'
                  'grado_pertenencia_alto'
                  'grado_pertenencia_critico',
                  'texto_resultado',
                  'usuario_id'
                  )


prueba_esquema = PruebaEsquema()
pruebas_esquema = PruebaEsquema(many=True)
