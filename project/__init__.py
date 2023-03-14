from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
# init SQLAlchemy so we can use it later in our models

from sqlalchemy import create_engine
import os

db = SQLAlchemy()
migrate = Migrate()

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static/media')
MEDIA_ROOT = "/static/media/"

ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'media')
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


    # replace here with the mysql connection string
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://tn243:0j1YqHL4CRkI@db.ethereallab.app:3306/tn243' # eg 'mysql:....'

    # app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:rKskryi2PwcsvCsFmGEV@containers-us-west-42.railway.app:5789/railway' # eg 'mysql:....'


    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    # migrate = Migrate(app, db)

    migrate.init_app(app, db)




    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .department import department as department_blueprint
    app.register_blueprint(department_blueprint)

    from .services import services as services_blueprint
    app.register_blueprint(services_blueprint)

    from .doctors import doctors as doctors_blueprint
    app.register_blueprint(doctors_blueprint)

    from .appointment import appointment as appointment_blueprint
    app.register_blueprint(appointment_blueprint)

    from .patients import patients as patients_blueprint
    app.register_blueprint(patients_blueprint)

    # blueprint for doctor
    # from .doctor import doctor as doctor_blueprint
    # app.register_blueprint(doctor_blueprint)

    return app