
from flask import render_template, request, redirect, url_for, flash, jsonify, make_response
from config import config

#from flask_wtf.csrf import CSRFProtect

import matplotlib.pyplot as plt
import skfuzzy as fuzz
import numpy as np
from flask import Flask, request, flash
from models.ModeloUsuario import ModeloUsuario
from flask_login import LoginManager, login_user, logout_user, login_required


from run import app, db, login_manager, bd


from models.entities.Usuario import Usuario, usuarios_esquema
from models.entities.Prueba import Prueba, prueba_esquema, pruebas_esquema
from pruebas.crearPrueba import crearPrueba
from pruebas.eliminarPruebaPorId import eliminarPruebaPorId
from pruebas.obtenerTodasPruebas import obtenerTodasPruebas
from pruebas.obtenerPruebaPorId import obtenerPruebaPorId
from pruebas.obtenerPruebaPorIdDelUsuario import obtenerPruebaPorIdDelUsuario
from users.login import loginNormal


#db.drop_all()
db.create_all()

# csrf = CSRFProtect()


@login_manager.user_loader
def load_user(id):
    return ModeloUsuario.obtener_por_id(db, id)


@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/a')
def a():
    return render_template('auth/result_bajo.html')


@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'GET':
        return render_template('auth/login.html')

    elif request.method == 'POST':
        print(request.form)
        
        logged_user = ModeloUsuario.login(
            request.form['nombre_usuario'], request.form['contrasenia'])
        if logged_user == None:
            print("Usuario no Encontrado...")
            return render_template('auth/login.html')

        else:
           
            return redirect(url_for('usuario'))
        

@app.route('/login-json', methods=['GET', 'POST'])
@login_manager.user_loader
def loginJson(usuario):
    if request.method != 'POST':
        return render_template('auth/login.html')

    body = request.json

    logged_user = loginNormal(body['nombre_usuario'], body['contrasenia'])
    if logged_user == None:
        flash("Usuario no Encontrado...")
        return render_template('auth/login.html')

    if logged_user.contrasenia:
        login_user(logged_user)
        return redirect(url_for('inicio'))
    else:
        flash("Contraseña Incorrecta...")
        return render_template('auth/login.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/inicio')
# @login_required
def inicio():
    return render_template('auth/layout.html')



@app.route('/usuario')
def usuario():
    return render_template('auth/usuario.html')


@app.route('/prueba')
def prueba():
    return render_template('auth/prueba.html')


def status_401(error):
    return redirect(url_for('login'))


def status_404(error):
    return "<h1>Página no encontrada</h1>", 404


@app.route('/usuario/tests/<userId>', methods=['GET'])
def getTestsByUserId(userId):
    return obtenerPruebaPorIdDelUsuario(userId)


@app.route('/prueba/<testId>', methods=['GET', 'DELETE'])
def getTestByIdController(testId):
    if request.method == 'GET':
        return obtenerPruebaPorId(testId)
    elif request.method == 'DELETE':
        return eliminarPruebaPorId(testId)


@app.route('/tests', methods=['GET'])
def getAllTestsController():
    return obtenerTodasPruebas()


@app.route('/lista')
def lista():
    cur = bd.connection.cursor()
    cur.execute('SELECT*FROM prueba')
    data = cur.fetchall()

    return render_template('auth/lista_tests.html', tests=data)

@app.route('/results/<id>', methods=['GET'])
def getResultDiagnosisView(id):
    data=  obtenerPruebaPorId(id)
    jsonData = data.get_json()
    route = ''
   
    if(jsonData['texto_resultado'] == 'RIESGO BAJO'):
        route = 'result_bajo.html'
    elif(jsonData['texto_resultado'] == 'RIESGO NORMAL'):
        route = 'result_normal.html'
    elif(jsonData['texto_resultado'] == 'RIESGO ALTO'):
        route = 'result_alto.html'
    elif(jsonData['texto_resultado'] == 'RIESGO CRITICO'):
        route = 'result_critico.html'

    return render_template('auth/' + route, data=jsonData) 


@app.route('/make-diagnosis', methods=['POST'])
def makeDiagnosis():
    body = request.form

    comida = (int(body['alimentation1']) + int(body['alimentation2']) +
                    int(body['alimentation3']) + int(body['alimentation4']) + int(body['alimentation5'])) / 5
    herencia = (int(body['genetical1']) + int(body['genetical2']) + int(
        body['genetical3']) + int(body['genetical4']) + int(body['genetical5']))
    glucosa = int(body['glucosa'])
    ejercicio = (int(body['physicalActivity1']) + int(
        body['physicalActivity2']) + int(body['physicalActivity3'])) / 3

    newJson = {
        "comida": comida,
        "glucosa": glucosa,
        "herencia": herencia,
        "ejercicio": ejercicio,
        "name": body['name'],
        "edad": body['edad'],
        "numero_documento_dni": body['numero_documento_dni']
    }
    data =  crearPrueba(newJson)
    jsonData = data.get_json()
    # crearPrueba(newJson)
    return redirect(url_for('.getResultDiagnosisView', id=jsonData['id']))
    # return render_template('auth/result_bajo.html', data=data)



if __name__ == '__main__':
    app.config.from_object(config['development'])
    # csrf.init_app(app)
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)
    app.run()
