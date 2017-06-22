from flask import Flask 
from config import config_dev
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_sqlalchemy import SQLALchemy
  

bootstrap=Bootstrap()
mail=Mail()
sqlalchemy=SQLALchemy()


def creat_app(config):
    
    app=Flask(__name__)
    
    bootstrap.init_app(app)
    mail.init_app(app)
    sqlalchemy.init_app(app)
    
    from .main improt main as main_blueprint
    from .auth import auth as auth_blueprint
    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint,url_prefix='/auth')


   
    return app
    
