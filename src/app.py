
from flask  import Flask, render_template,request,redirect,url_for, flash, session
from flask_mysqldb import MySQL
from config import config
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user, logout_user, login_required

#Models:
from models.ModelUser import ModelUser

#Entities:
from models.entities.User import User

app=Flask(__name__)

csrf=CSRFProtect()
db=MySQL(app)

login_manager_app = LoginManager(app)

@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(db, id)

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET','POST'])

def login():
    
    if request.method=='POST':
        user = User(0, request.form['username'], request.form['password'])
        logged_user = ModelUser.login(db, user)
        if logged_user != None:
            if logged_user.password:
                login_user(logged_user)
                return redirect(url_for('inicio'))
            else:
                flash("Contraseña Incorrecta...")
                return render_template('auth/login.html')
        else:
            flash("Usuario no Encontrado...")
            return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')

@app.route('/logout')
def logout():
    logout_user()    
    return redirect(url_for('login'))

@app.route('/home')
@login_required
def home():
    return render_template('home.html')

@app.route('/inicio')
@login_required
def inicio():
    return render_template('auth/layout.html')

# @app.route('/protected')
# @login_required
# def protected():
#     return "<h1>Esta es una vista protegida, solo para usuarios autenticados.</h1>"

@app.route('/user')
def user():
 return render_template ('auth/user.html')
 
@app.route('/test')
def test():
 return render_template ('auth/test.html')

def status_401(error):
    return redirect(url_for('login'))


def status_404(error):
    return "<h1>Página no encontrada</h1>", 404   


if __name__== '__main__':
    app.config.from_object(config['development'])
    csrf.init_app(app)
    app.register_error_handler(401,status_401)
    app.register_error_handler(404,status_404)
    app.run()

