# coding:utf-8

from flask_wtf import FlaskForm
from wtforms import PasswordField,StringField,TextAreaField,SubmitField,BooleanField
from wtfforms.validators import Required,Length,Email,Regexp,Equalto
from wtfforms import ValidationError
from ..models import User,Post,Role

class RegisterForm(FlaskForm):
      email = StringField('email', validators=[Required(), Length(1, 64), Email()])
      username=StringField('username',validators=[Required(),Length(1,64),Regexp(r'^[A-Za-z][0-9A-Za-z_.]*$',0,'username must start with a letter and only has letters,numbers,dots,and underscores')])
      password=PasswordFiels('password',validators=[Required(),EqualTo('password2',message="password must match")])
      password2=PasswordField('Confirm password',validators=[Required()])
      name=StringField('realname',validators=[Length(1,64)])
      locationn=StringField('address')
      aboutme=TextAreaField()
      submit=SubmitField('register')

      def validate_email(self,field):     #函数名需定义为validate_xxxx
          if User.query.filter_by(email=field.data).first():
             raise ValidationError("Email has been used!")
      
      def validata_username(self,field):
          if User.query.filter_by(username=field.data).first():
             raise ValidationError("username had been registered!")

class loginForm(FlaskForm):
      email=StringField('email',validators=[Required(), Length(1,64), Email()])
      username=StringField('username',validators=[Required(), Length(1,64)])
      password=PasswordField('password',validators=[Required()])
      remember_me=BooleanField('keep me log in')
      submit=SubmitField('login')



         
