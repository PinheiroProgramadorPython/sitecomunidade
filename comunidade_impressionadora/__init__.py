from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os
import sqlalchemy


app = Flask(__name__)


app.config['SECRET_KEY'] = '8b9e12f9daab8500ed774606121e0608'
if os.getenv('DATABASE_URL'):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site_comunidade.db'
database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'alert alert-info'


from comunidade_impressionadora import models
try:
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    inspector = inspect(engine)

    with app.app_context():
        if not inspector.has_table('usuario'):
            database.create_all()
except:
    print(f"Erro ao verificar/criar o banco")
        
from comunidade_impressionadora import routes
