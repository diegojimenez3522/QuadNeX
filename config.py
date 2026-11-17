class Config:
    SECRET_KEY = 'julieth'
    DEBUG      = True
    # Quien se registre con este correo queda como Administrador (perfil 'A').
    # Cámbialo por el correo del administrador de QuadNeX.
    ADMIN_CORREO = 'diego.jimenez3522@alumnos.udg.mx'

class DevelopmentConfig(Config):
    MYSQL_HOST     = 'localhost'
    MYSQL_USER     = 'root'
    MYSQL_PASSWORD = ''
    MYSQL_DB       = 'quadnex'

config = {
    'development' : DevelopmentConfig
}
