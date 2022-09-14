
from flask import render_template, request, redirect, url_for, flash,jsonify
from config import config

#from flask_wtf.csrf import CSRFProtect

import matplotlib.pyplot as plt
import skfuzzy as fuzz
import numpy as np
from flask import Flask, request, flash
from models.ModelUser import ModelUser
from flask_login import LoginManager, login_user, logout_user, login_required


from run import app, db, login_manager,bd


from models.entities.User import User, users_schema
from models.entities.Test import Test, test_schema, tests_schema
from tests.createTest import createTest
from tests.deleteTestById import deleteTestById
from tests.getAllTests import getAllTests
from tests.getTestById import getTestById
from tests.getTestsByUserId import getTestByUserId
from users.login import loginNormal


db.create_all()

# csrf = CSRFProtect()


@login_manager.user_loader
def load_user(id):
    return ModelUser.get_by_id(db, id)


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'GET':
        return render_template('auth/login.html')

    elif request.method == 'POST':
        print(request.form)

        # user = User(0, request.form['username'], request.form['password'])

        # user = User.setUsername(request.form['username']).setPassword(
        #     request.form['password'])
        logged_user = ModelUser.login(
            request.form['username'], request.form['password'])
        if logged_user == None:
            print("Usuario no Encontrado...")
            return render_template('auth/login.html')

        else:
            # print(logged_user)
            # flash('Logged in successfully.')
            # login_user(logged_user)
            return redirect(url_for('user'))
        # else:
        #     print("Contraseña Incorrecta...")
        #     return render_template('auth/login.html')


@app.route('/login-json', methods=['GET', 'POST'])
@login_manager.user_loader
def loginJson(user):
    if request.method != 'POST':
        return render_template('auth/login.html')

    body = request.json

    logged_user = loginNormal(body['username'], body['password'])
    if logged_user == None:
        flash("Usuario no Encontrado...")
        return render_template('auth/login.html')

    if logged_user.password:
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

# @app.route('/protected')
# @login_required
# def protected():
#     return "<h1>Esta es una vista protegida, solo para usuarios autenticados.</h1>"


@app.route('/user')
def user():
    return render_template('auth/user.html')


@app.route('/test')
def test():
    return render_template('auth/test.html')


def status_401(error):
    return redirect(url_for('login'))


def status_404(error):
    return "<h1>Página no encontrada</h1>", 404


@app.route('/user/tests/<userId>', methods=['GET'])
def getTestsByUserId(userId):
    return getTestByUserId(userId)


@app.route('/test/<testId>', methods=['GET', 'DELETE'])
def getTestByIdController(testId):
    if request.method == 'GET':
        return getTestById(testId)
    elif request.method == 'DELETE':
        return deleteTestById(testId)


@app.route('/tests', methods=['GET'])
def getAllTestsController():
    return getAllTests()


@app.route('/lista')
def lista():
    cur=bd.connection.cursor()
    cur.execute('SELECT*FROM test')
    data=cur.fetchall()
    
    return render_template('auth/lista_tests.html',tests=data)


@app.route('/make-diagnosis', methods=['POST'])
def makeDiagnosis():
    body = request.form

    alimentation = (int(body['alimentation1']) + int(body['alimentation2']) +
                    int(body['alimentation3']) + int(body['alimentation4']) + int(body['alimentation5'])) / 5
    genetical = (int(body['genetical1']) + int(body['genetical2']) + int(
        body['genetical3']) + int(body['genetical4']) + int(body['genetical5']))
    glucose = int(body['glucose'])
    physicalActivity = (int(body['physicalActivity1']) + int(
        body['physicalActivity2']) + int(body['physicalActivity3'])) / 3

    newJson = {
        "alimentation": alimentation,
        "glucose": glucose,
        "genetical": genetical,
        "physicalActivity": physicalActivity
    }
    data=createTest(newJson)
    #createTest(newJson)
    return render_template('auth/result_bajo.html',data=data)


if __name__ == '__main__':
    app.config.from_object(config['development'])
    # csrf.init_app(app)
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)
    app.run()
