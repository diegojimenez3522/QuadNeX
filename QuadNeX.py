from flask import Flask, flash, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash

from config import config
from models.entities.ModelUser import ModelUser
from models.entities.User import User

QuadNeXApp = Flask(__name__)
QuadNeXApp.config.from_object(config['development'])
db = MySQL(QuadNeXApp)

adminUsuarios = LoginManager(QuadNeXApp)
adminUsuarios.login_view = 'home'
adminUsuarios.login_message = 'Inicia sesión para continuar'

@adminUsuarios.user_loader
def load_user(id):
    return ModelUser.get_by_id(db, id)

def es_admin():
    return current_user.is_authenticated and current_user.perfil == 'A'

@QuadNeXApp.route('/')
def home():
    return render_template('home.html')

@QuadNeXApp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        nombre = request.form['nombre'].strip()
        correo = request.form['correo'].strip()
        clave = request.form['clave']
        if clave != request.form.get('confirmar', clave):
            flash('Las contraseñas no coinciden')
            return redirect(url_for('home'))
        if ModelUser.get_by_correo(db, correo) is not None:
            flash('Ese correo ya está registrado')
            return redirect(url_for('home'))
        claveCifrada = generate_password_hash(clave)
        perfil = 'A' if correo.lower() == QuadNeXApp.config['ADMIN_CORREO'].lower() else 'U'
        regUsuario = db.connection.cursor()
        regUsuario.execute("INSERT INTO usuario (nombre, correo, clave, perfil) VALUES (%s, %s, %s, %s)", (nombre, correo, claveCifrada, perfil))
        db.connection.commit()
        regUsuario.close()
        flash('Cuenta creada, ya puedes iniciar sesión')
    return redirect(url_for('home'))

@QuadNeXApp.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        usuario = User(0, None, request.form['correo'], request.form['clave'], None)
        usuarioAutenticado = ModelUser.sign_in(db, usuario)
        if usuarioAutenticado is not None:
            if usuarioAutenticado.clave:
                login_user(usuarioAutenticado, remember=bool(request.form.get('recordarme')))
                if usuarioAutenticado.perfil == 'A':
                    return redirect(url_for('home_admin'))
                return redirect(url_for('home_user'))
            flash('Contraseña incorrecta')
        else:
            flash('Usuario inexistente')
    return redirect(url_for('home'))

@QuadNeXApp.route('/signout', methods=['GET', 'POST'])
def signout():
    logout_user()
    return redirect(url_for('home'))

@QuadNeXApp.route('/home_admin', methods=['GET', 'POST'])
@login_required
def home_admin():
    if not es_admin():
        return redirect(url_for('home_user'))
    return render_template('admin.html')

@QuadNeXApp.route('/home_user', methods=['GET', 'POST'])
@login_required
def home_user():
    return render_template('user.html')

@QuadNeXApp.route('/operaciones', methods=['GET'])
@login_required
def operaciones():
    if not es_admin():
        return redirect(url_for('home_user'))
    busqueda = request.args.get('q', '').strip()
    selUsuario = db.connection.cursor()
    if busqueda:
        patron = f'%{busqueda}%'
        selUsuario.execute("SELECT id, nombre, correo, perfil FROM usuario WHERE nombre LIKE %s OR correo LIKE %s ORDER BY id", (patron, patron))
    else:
        selUsuario.execute("SELECT id, nombre, correo, perfil FROM usuario ORDER BY id")
    usuarios = selUsuario.fetchall()
    selUsuario.close()
    return render_template('operaciones.html', usuarios=usuarios, busqueda=busqueda)

@QuadNeXApp.route('/operaciones/agregar', methods=['POST'])
@login_required
def operaciones_agregar():
    if not es_admin():
        return redirect(url_for('home_user'))
    nombre = request.form['nombre'].strip()
    correo = request.form['correo'].strip()
    clave = request.form['clave']
    perfil = 'A' if request.form.get('perfil') == 'A' else 'U'
    if ModelUser.get_by_correo(db, correo) is not None:
        flash('Ese correo ya está registrado')
        return redirect(url_for('operaciones'))
    insUsuario = db.connection.cursor()
    insUsuario.execute("INSERT INTO usuario (nombre, correo, clave, perfil) VALUES (%s, %s, %s, %s)", (nombre, correo, generate_password_hash(clave), perfil))
    db.connection.commit()
    insUsuario.close()
    flash('Usuario agregado')
    return redirect(url_for('operaciones'))

@QuadNeXApp.route('/operaciones/editar/<int:id>', methods=['POST'])
@login_required
def operaciones_editar(id):
    if not es_admin():
        return redirect(url_for('home_user'))
    nombre = request.form['nombre'].strip()
    correo = request.form['correo'].strip()
    clave = request.form.get('clave', '')
    perfil = 'A' if request.form.get('perfil') == 'A' else 'U'
    if id == current_user.id and perfil != 'A':
        flash('No puedes quitarte el perfil de administrador')
        return redirect(url_for('operaciones'))
    existente = ModelUser.get_by_correo(db, correo)
    if existente is not None and existente.id != id:
        flash('Ese correo ya pertenece a otro usuario')
        return redirect(url_for('operaciones'))
    updUsuario = db.connection.cursor()
    if clave:
        updUsuario.execute("UPDATE usuario SET nombre = %s, correo = %s, clave = %s, perfil = %s WHERE id = %s", (nombre, correo, generate_password_hash(clave), perfil, id))
    else:
        updUsuario.execute("UPDATE usuario SET nombre = %s, correo = %s, perfil = %s WHERE id = %s", (nombre, correo, perfil, id))
    db.connection.commit()
    updUsuario.close()
    flash('Usuario actualizado')
    return redirect(url_for('operaciones'))

@QuadNeXApp.route('/operaciones/eliminar/<int:id>', methods=['POST'])
@login_required
def operaciones_eliminar(id):
    if not es_admin():
        return redirect(url_for('home_user'))
    if id == current_user.id:
        flash('No puedes eliminar tu propia cuenta')
        return redirect(url_for('operaciones'))
    delUsuario = db.connection.cursor()
    try:
        delUsuario.execute("DELETE FROM usuario WHERE id = %s", (id,))
        db.connection.commit()
        flash('Usuario eliminado')
    except Exception:
        db.connection.rollback()
        flash('No se puede eliminar: el usuario tiene pedidos, carritos o reseñas asociados')
    finally:
        delUsuario.close()
    return redirect(url_for('operaciones'))

if __name__ == '__main__':
    QuadNeXApp.run(port=5000, debug=True)
