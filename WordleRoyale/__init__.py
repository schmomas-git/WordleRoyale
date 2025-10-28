from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object('config')
app.secret_key = 'WordleRoyaleSecretKey'
db = SQLAlchemy(app)

from WordleRoyale.views import *

if __name__ == '__main__':
    app.run()