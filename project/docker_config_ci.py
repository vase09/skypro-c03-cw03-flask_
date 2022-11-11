import base64


class BaseConfig:
    SECRET_KEY = "you-will-never-guess"
    JSON_AS_ASCII = False

    ITEMS_PER_PAGE = 12

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET = 'you-will-never-guess'
    JWT_ALGORITHM = 'HS256'
    TOKEN_EXPIRE_MINUTES = 15
    TOKEN_EXPIRE_DAYS = 130

    PWD_HASH_SALT = base64.b64decode("salt")
    PWD_HASH_ITERATIONS = 100_000

    RESTX_JSON = {'ensure_ascii': False, 'indent': 2}


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = "postgresql://$DB_USER:$DB_PASSWORD@pg/$DB_NAME"
