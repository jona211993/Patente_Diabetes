class Config:
    SECRET_KEY = 'B!1weNAt1T%kvhU'


class DevelopmentConfig(Config):
    DEBUG = True
    MYSQL_HOST = '127.0.0.1'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = '1234'
    MYSQL_DB = 'flask_login'


config = {
    'development': DevelopmentConfig
}
