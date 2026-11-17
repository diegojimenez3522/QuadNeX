from flask import Flask, flash, jsonify, render_template, request, redirect, session, url_for
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

# ---------------------------------------------------------------
# Catálogo de la portada. Mientras la tabla `producto` no tenga
# datos, los productos en tendencia se definen aquí.
# ---------------------------------------------------------------
PRODUCTOS = [
    {'id': 1, 'nombre': 'Neumático Maxxis Bighorn', 'descripcion': 'Tacos agresivos para lodo, roca y arena.',
     'compatible': 'Can-Am · Polaris · CFMOTO', 'precio': 2950, 'precio_anterior': None, 'tag': ('popular', 'Popular'),
     'imagen': 'https://images.unsplash.com/photo-1621939514649-280e73a5c8c4?auto=format&fit=crop&w=600&q=70',
     'alt': 'Neumático todo terreno Maxxis Bighorn para ATV'},
    {'id': 2, 'nombre': 'Amortiguador Off-Road Performance', 'descripcion': 'Ajuste de rebote para terrenos exigentes.',
     'compatible': 'Polaris · Yamaha · Honda', 'precio': 4380, 'precio_anterior': None, 'tag': ('new', 'Nuevo'),
     'imagen': 'https://images.unsplash.com/photo-1568605114967-8130f3a36994?auto=format&fit=crop&w=600&q=70',
     'alt': 'Amortiguador de alto desempeño para suspensión Off-Road'},
    {'id': 3, 'nombre': 'Winche eléctrico 4500 LB', 'descripcion': 'Cable sintético y control remoto inalámbrico.',
     'compatible': 'Universal 4x4', 'precio': 5720, 'precio_anterior': None, 'tag': None,
     'imagen': 'https://images.unsplash.com/photo-1449965408869-eaa3f722e40d?auto=format&fit=crop&w=600&q=70',
     'alt': 'Winche eléctrico de 4500 libras para vehículo 4x4'},
    {'id': 4, 'nombre': 'Barra LED 32"', 'descripcion': 'Iluminación de alto alcance resistente al agua.',
     'compatible': 'Universal ATV / UTV', 'precio': 2480, 'precio_anterior': 3100, 'tag': ('offer', 'Oferta'),
     'imagen': 'https://images.unsplash.com/photo-1520031441872-6d2d4b1b0f0d?auto=format&fit=crop&w=600&q=70',
     'alt': 'Barra de luces LED de 32 pulgadas para vehículo todo terreno'},
    {'id': 5, 'nombre': 'Kit de suspensión Off-Road', 'descripcion': 'Mayor recorrido y absorción de impactos.',
     'compatible': 'Kawasaki · Suzuki · Arctic Cat', 'precio': 7150, 'precio_anterior': None, 'tag': None,
     'imagen': 'https://images.unsplash.com/photo-1601362840469-51e4d8d58785?auto=format&fit=crop&w=600&q=70',
     'alt': 'Kit de suspensión reforzada Off-Road'},
    {'id': 6, 'nombre': 'Aceite sintético 10W-50', 'descripcion': 'Fórmula sintética para máxima protección del motor.',
     'compatible': 'Todas las marcas', 'precio': 480, 'precio_anterior': None, 'tag': None,
     'imagen': 'https://images.unsplash.com/photo-1635784063271-aac89c5c8b31?auto=format&fit=crop&w=600&q=70',
     'alt': 'Aceite sintético 10W-50 para motor de ATV o UTV'},
]
PRODUCTOS_POR_ID = {p['id']: p for p in PRODUCTOS}
CANTIDAD_MAXIMA = 99

# ---------------------------------------------------------------
# Carrito: se guarda en la sesión como {"id_producto": cantidad}
# ---------------------------------------------------------------
def obtener_carrito():
    carrito = session.get('carrito', {})
    # Descarta productos que ya no existan en el catálogo
    return {k: v for k, v in carrito.items() if k.isdigit() and int(k) in PRODUCTOS_POR_ID}

def guardar_carrito(carrito):
    session['carrito'] = carrito
    session.modified = True

def resumen_carrito():
    carrito = obtener_carrito()
    items = []
    for id_str, cantidad in carrito.items():
        p = PRODUCTOS_POR_ID[int(id_str)]
        items.append({
            'id': p['id'],
            'nombre': p['nombre'],
            'imagen': p['imagen'],
            'precio': p['precio'],
            'cantidad': cantidad,
            'subtotal': p['precio'] * cantidad,
        })
    return {
        'items': items,
        'cantidad': sum(i['cantidad'] for i in items),
        'total': sum(i['subtotal'] for i in items),
    }

@QuadNeXApp.context_processor
def inyectar_carrito():
    return {'carrito_cantidad': sum(obtener_carrito().values())}

@QuadNeXApp.template_filter('mxn')
def formato_mxn(valor):
    return f'${valor:,.0f}'

def leer_producto_y_cantidad():
    datos = request.get_json(silent=True) or request.form
    try:
        id_producto = int(datos.get('id_producto'))
        cantidad = int(datos.get('cantidad', 1))
    except (TypeError, ValueError):
        return None, None
    if id_producto not in PRODUCTOS_POR_ID:
        return None, None
    return id_producto, cantidad

@QuadNeXApp.route('/carrito', methods=['GET'])
def carrito_ver():
    return jsonify(resumen_carrito())

@QuadNeXApp.route('/carrito/agregar', methods=['POST'])
def carrito_agregar():
    id_producto, cantidad = leer_producto_y_cantidad()
    if id_producto is None or cantidad < 1:
        return jsonify({'error': 'Producto no válido'}), 400
    carrito = obtener_carrito()
    clave = str(id_producto)
    carrito[clave] = min(carrito.get(clave, 0) + cantidad, CANTIDAD_MAXIMA)
    guardar_carrito(carrito)
    return jsonify(resumen_carrito())

@QuadNeXApp.route('/carrito/actualizar', methods=['POST'])
def carrito_actualizar():
    id_producto, cantidad = leer_producto_y_cantidad()
    if id_producto is None:
        return jsonify({'error': 'Producto no válido'}), 400
    carrito = obtener_carrito()
    clave = str(id_producto)
    if cantidad < 1:
        carrito.pop(clave, None)
    else:
        carrito[clave] = min(cantidad, CANTIDAD_MAXIMA)
    guardar_carrito(carrito)
    return jsonify(resumen_carrito())

@QuadNeXApp.route('/carrito/eliminar', methods=['POST'])
def carrito_eliminar():
    id_producto, _ = leer_producto_y_cantidad()
    if id_producto is None:
        return jsonify({'error': 'Producto no válido'}), 400
    carrito = obtener_carrito()
    carrito.pop(str(id_producto), None)
    guardar_carrito(carrito)
    return jsonify(resumen_carrito())

@QuadNeXApp.route('/carrito/vaciar', methods=['POST'])
def carrito_vaciar():
    guardar_carrito({})
    return jsonify(resumen_carrito())

@QuadNeXApp.route('/')
def home():
    return render_template('home.html', productos=PRODUCTOS)

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
    return render_template('admin.html', productos=PRODUCTOS)

@QuadNeXApp.route('/home_user', methods=['GET', 'POST'])
@login_required
def home_user():
    return render_template('user.html', productos=PRODUCTOS)

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
