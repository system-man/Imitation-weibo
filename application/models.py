# coding:utf-8

from application import db
from flask_login import UserMixin,AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import login_manager   #用以加载用户的回调函数
from datetime import datetime

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app, request


class Permission:
    Follow=0x01
    Comment=0x02
    Write_article=0x04
    Moderator=0x08
    Administer=0x80

class Role(db.Model):
    __tablename__='roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permission=db.Column(db.Integer)
    users = db.relationship('User', backref='role',lazy='dynamic')


    @staticmethod
    def insert_role():
        roles={'USER':(Permission.Follow|Permission.Comment|Permission.Write_article, True),
               'MODERATOR':(Permission.Follow|Permission.Comment|Permission.Write_article|Permission.Moderator, False),
               'ADMINISTER':(0xff,False)
               }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role=Role(name=r)
            role.default=roles[r][1]
            role.permission=roles[r][0]
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return '<Role %r>' % self.name


class User(UserMixin, db.Model):
    __tablename__= 'users'
    id=db.Column(db.Integer, primary_key=True)
    email=db.Column(db.String(64),unique=True, index=True)
    username=db.Column(db.String(64),unique=True, index=True)
    password=db.Column(db.String(128))
    password_hash=db.Column(db.String(128))
    confirmed=db.Column(db.Boolean, default=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    name=db.Column(db.String(64))
    location=db.Column(db.String(128))
    aboutme=db.Column(db.Text(),nullable=True)
    member_since=db.Column(db.DateTime(),default=datetime.utcnow)
    last_seen=db.Column(db.DateTime(),default=datetime.utcnow)
    posts=db.relationship('Post',backref='author',lazy='dynamic')




    def __init__(self,**kwargs):
        super(User,self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['FLASKY_ADMIN']:
                self.role=Role.query.filter_by(name='ADMINISTER').first()
            if self.role is None:
                self.role=Role.query.filter_by(default=True).first()
#        if self.email is not None and self.avatar_hash is None:
#            self.avatar_hash=hashlib.md5(self.email.encode('utf-8')).hexdigest()

#    def generate_hash_url(self,size=100,default='identicon',rating='g'):
#        if request.is_secure:
#            url='https://secure.gravatar.com'
#        else:
#            url='http://wwww.gravatar.com'
#        hash=self.avatar_hash or hsahlib.md5(self.email.encode('utf-8')).hexdigest()
#        return '{url}{hash}?s={size}&d={default}&r={rating}'.format(url=url,hash=hash,size=size,default=default,rating=rating)

    def ping(self):
        self.last_seen=datetime.utcnow()
        db.session.add(self)



    def __repr__(self):
        return '<User %r' % self.email


    @property
    def password(self):
        raise AttributeError("password is not readable")

    @password.setter
    def password(self,password):
        self.password_hash=generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    def reset_password(self,token,new_password):
       s=Serializer(current_app.config['SECRET_KEY'])
       try:
           data=s.loads(token)
       except:
           return False
       if data.get('confirme') != self.id:
           return False
       self.password=new_password
       db.session.add(self)
       return True

    def generate_confirmation_token(self, expiration=3600):
       s=Serializer(current_app.config['SECRET_KEY'],expiration)
       return s.dumps({'confirme':self.id})

    def confirm(self,token):
       s=Serializer(current_app.config['SECRET_KEY'])
       try:
           data=s.loads(token)
       except:
           return False
       if data.get('confirme') != self.id:
           return False
       self.confirmed = True
       db.session.add(self)
       return True

    def can(self,permission):
        return self.role is not None and (self.role.permission & permission) == permission

    def is_administer(self):
        return self.can(Permission.Administer)


class AnonymousUser(AnonymousUserMixin):
    def can(self,permission):
        return False

    def is_administer(self):
        return False

login_manager.anonymous_user=AnonymousUser




class Post(db.Model):
    __tablename__='posts'
    id = db.Column(db.Integer,primary_key=True)
    body=db.Column(db.Text())
    timestamp=db.Column(db.DateTime(),index=True,default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))

