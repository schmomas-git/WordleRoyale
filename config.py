import secrets

SECRET_KEY = secrets.token_hex(16)
SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'

salt = b'(Y>\x9e\xf3E\xfe)'