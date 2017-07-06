# coding:utf-8
import os

basedir=os.path.abspath(os.path.dirname(__file__))

class Config:

    SECRET_KEY = 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN=True
    SQLALCHEMY_TRACK_MODIFICATIONS=True

    FLASKY_ADMIN='jczx32yp@qq.com'
    FLASK_POSTS_PER_PAGE= 20

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG=True
    MAIL_SERVER='smtp.qq.com'
    MAIL_PORT=587
    MAIL_USE_TLS=True
    MAIL_USE_SSL=False
    MAIL_USERNAME='jczx32yp@qq.com'
    MAIL_PASSWORD='csohwbozzhexbhaj'
    FLASKY_MAIL_SUBJECT_PREFIX='[FLASKY]'
    FLASKY_MAIL_SENDER='jczx32yp@qq.com'
    SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(basedir, 'data.sqlite')



config_dev={
   'development':DevelopmentConfig
}
