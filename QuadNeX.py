from turtle import home

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from config import Config
from werkzeug.security import generate_password_hash
from models.entities.User import User


QuadNeXApp   = Flask(__name__)
QuadNeXApp.config.from_object(Config['development'])
db           = MySQL(QuadNeXApp)
adminUsuarios = LoginManager(QuadNeXApp)

@adminUsuarios. user_loader
def agregarUsuario(id):
    return render_template('home.html')

@QuadNeXApp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        clave = request.form['clave']
        claveCifrada = generate_password_hash(clave)
        regUsuario = db.connection.cursor()
        regUsuario.execute("INSERT INTO usuario (nombre, correo, clave) VALUES (%s, %s, %s)", (nombre, correo, claveCifrada))
        
        db.connection.commit()
        regUsuario.close()¿
       
        return redirect(url_for('home'))
    
    @QuadNeXApp.route('/login', methods=['GET', 'POST'])
    def signin():
        if request.method == 'POST':    
           if request.method == 'POST':
                usuario = User(0, request.form['correo'], request.form['clave'])
                usuarioAutenticado = usuario.signin(db, usuario)
                if usuarioAutenticado is not None:
                    if usuarioAutenticado.clave:
                        login_user(usuarioAutenticado)
                        if usuarioAutenticado.perfil == 'A':
                            return render_template('admin.html')
                        else:
                            return render_template('user.html')
                    else:
                        flash('Contraseña incorrecta')
                        redirect(url_for('home'))
                else:
                    flash('Usuario inexistente')
                    redirect(url_for('home'))
                else:
                    return render_template('home.html')
                    

if __name__ == '__main__':
    QuadNeXApp.run(port=5000)