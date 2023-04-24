import os
from flask import Flask
from flask_login import LoginManager, current_user
from flask_uploads import DOCUMENTS, IMAGES, TEXT, UploadSet, configure_uploads
from flask_cors import CORS
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
from datetime import timedelta
from .models import User, Competition, CompetitionUser, db
from App.database import db
from App.controllers import ( create_user, get_all_users_json, get_all_users )


from App.database import init_db

from App.controllers import (
    setup_jwt
)

from App.views import views

login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
  return User.query.get(user_id)

@login_manager.unauthorized_handler
def unauthorized():
    flash('Unauthorized!')
    return redirect(url_for('get_login_page'))

def add_views(app):
    for view in views:
        app.register_blueprint(view)


def loadConfig(app, config):
    app.config['ENV'] = os.environ.get('ENV', 'DEVELOPMENT')
    delta = 7
    if app.config['ENV'] == "DEVELOPMENT":
        app.config.from_object('App.config')
        delta = app.config['JWT_ACCESS_TOKEN_EXPIRES']
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
        app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
        app.config['DEBUG'] = os.environ.get('ENV').upper() != 'PRODUCTION'
        app.config['ENV'] = os.environ.get('ENV')
        delta = os.environ.get('JWT_ACCESS_TOKEN_EXPIRES', 7)
        
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=int(delta))
    app.config["JWT_TOKEN_LOCATION"] = ["headers"]
        
    for key, value in config.items():
        app.config[key] = config[key]

def create_app(config={}):
    app = Flask(__name__, static_url_path='/static')
    CORS(app)
    loadConfig(app, config)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['SEVER_NAME'] = '0.0.0.0'
    app.config['PREFERRED_URL_SCHEME'] = 'https'
    app.config['UPLOADED_PHOTOS_DEST'] = "App/uploads"
    photos = UploadSet('photos', TEXT + DOCUMENTS + IMAGES)
    login_manager.init_app(app)
    login_manager.login_view = "login_page"
    configure_uploads(app, photos)
    add_views(app)
    init_db(app)
    setup_jwt(app)
    app.app_context().push()
    with app.app_context():
        db.drop_all()
        db.create_all()
        bob = create_user('bob', 'bobpass', True)
        db.session.add(bob)

        with open('competitions.csv', newline='', encoding='latin-1') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                competition = Competition(name=row['name'], category=row['category'], winner=row['winner'], runnerup=row['runnerup'], description=row['description'])
                db.session.add(competition)
            db.session.commit()
        print('database intialized')
    return app

app = create_app()
