from werkzeug.security import check_password_hash
from flask_login import UserMixin

class User(UserMixin):
    @classmethod
    def __init__(self, id, nombre, correo, clave, perfil)-> None:
        self.id = id
        self.nombre = nombre
        self.correo = correo
        self.clave = clave
        self.perfil = perfil
        @classmethod
        def validarClave(self, ClaveCifrada, clave):
        return check_password_hash(clave.clave, clave)