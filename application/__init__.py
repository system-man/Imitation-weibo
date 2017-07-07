from flask import Flask 
from config import config_dev
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_sqlalchemy import SQLALchemy
from flask_login import LoginMnanger  
from flask_moment import Moment


moment=Moment()
login_manager=LoginManager()
bootstrap=Bootstrap()
mail=Mail()
db=SQLALchemy()


def creat_app(config_name):
    
    app=Flask(__name__)
    app.config.from_object(config_dev[config_name])
    config_dev[config_name].init(app)

    moment.init(app)
    login_manager.init(app)
    login_manager.session_protection=strong
    login_manager.login_view='auth.login'

    bootstrap.init_app(app)
    mail.init_app(app)
    db.init_app(app)
    
   
    from .main import main as main_blueprint
    from .auth import auth as auth_blueprint
    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint,url_prefix='/auth')
   
    return app
