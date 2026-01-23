from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, RegisterFormV2
from wtforms import StringField
from wtforms.validators import DataRequired
from flask_security.models import fsqla
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

app = Flask(__name__)
app.config.from_object('config')

db.init_app(app)
app.secret_key = 'WordleRoyaleSecretKey'

# Define models for Flask-Security
fsqla.FsModels.set_db_info(db)

class Role(db.Model, fsqla.FsRoleMixin):
    pass

class User(db.Model, fsqla.FsUserMixin):
    pass

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
class ExtendedRegisterForm(RegisterFormV2):
    username = StringField('Username', [DataRequired()])
security = Security(app, user_datastore, register_form=ExtendedRegisterForm)

from WordleRoyale.views import *

if __name__ == '__main__':
    app.run()