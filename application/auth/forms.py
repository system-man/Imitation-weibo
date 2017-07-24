# coding:utf-8

from flask_wtf import FlaskForm
from wtforms import PasswordField,StringField,TextAreaField,SubmitField,BooleanField,SelectField
from wtforms.validators import Required,Length,Email,Regexp,EqualTo
from wtforms import ValidationError
from ..models import User,Post,Role

class RegisterForm(FlaskForm):
      email = StringField('email', validators=[Required(), Length(1, 64), Email()])
      username=StringField('username',validators=[Required(),Length(1,64),Regexp(r'^[A-Za-z][0-9A-Za-z_.]*$',0,'username must start with a letter and only has letters,numbers,dots,and underscores')])
      password=PasswordField('password',validators=[Required(),EqualTo('password2',message="password must match")])
      password2=PasswordField('Confirm password',validators=[Required()])
      name=StringField('realname',validators=[Length(1,64)])
      location=StringField('address')
      aboutme=TextAreaField()
      submit=SubmitField('register')

      def validate_email(self,field):     #函数名需定义为validate_xxxx
          if User.query.filter_by(email=field.data).first():
             raise ValidationError("Email has been used!")
      
      def validata_username(self,field):
          if User.query.filter_by(username=field.data).first():
             raise ValidationError("username had been registered!")

class LoginForm(FlaskForm):
      email=StringField('email',validators=[Required(), Length(1,64), Email()])
      username=StringField('username',validators=[Required(), Length(1,64)])
      password=PasswordField('password',validators=[Required()])
      remember_me=BooleanField('keep me log in')
      submit=SubmitField('login')

class editprofileForm(FlaskForm):
     username=StringField('username')
     location=StringField('address',validators=[Length(1,64),Required()])
     aboutme=TextAreaField('about yourself')
     submit=SubmitField('save all information')

  
class admineditprofileForm(FlaskForm):
    email = StringField('email', validators=[Required(), Length(1, 64), Email()])
    username = StringField('username', validators=[Required(), Length(1, 64), Regexp('^[A-Za-z][0-9A-Za-z_.]*$', 0, 'username must start with a letter and only have letters,numbers,dots and underscores')])
    role = SelectField('Role',coerce=int)  #角色角色用数字表示
    name = StringField('realname', validators=[Length(1, 64)])
    location = StringField('address')
    aboutme = TextAreaField()
    confirmed =BooleanField('confirmed')
    submit = SubmitField('SAVE')

    def __init__(self,user,*args,**kwargs):
        super(admineditprofileForm,self).__init__(*args,**kwargs)
        self.role.choices=[(role.id,role.name) for role in Role.query.order_by(Role.name).all()]
        self.user=user

    def validate_email(self,field):       ##这里函数名必须定义为validate_XXX(self,field）
        if field.data != self.user.email and User.query.filter_by(email=field.data).first():
            raise ValidationError("email had been used!")

    def validate_username(self,field):
        if field.data != self.user.username and User.query.filter_by(username=field.data).first():
            raise ValidationError("username had been used!")

class changepasswordForm(FlaskForm):
      current_password=PasswordField('password',validators=[Required()])
      new_password=PasswordField('password',validators=[Required(),EqualTo('new_password2',message="password must match")])
      new_password2=PasswordField('password',validators=[Required()])
      submit = SubmitField('Save')

      def validate_current_password(self,field):
          if not current_user.verify_password(field.data):
             raise ValidationError('the current password is invalid!')

class requestresetpasswordForm(FlaskForm):
      email = StringField('email', validators=[Required(), Length(1, 64), Email()])
      submit = SubmitField('Get resetpassword_email')
      
      def validate_email(self,field):
          user = User.query.filter_by(email=field.data).first()
          if user is None:
               raise ValidationError('please confirm you have registered!')

class resetpasswordForm(FlaskForm):
      email = StringField('email', validators=[Required(), Length(1, 64), Email()])
      new_password=PasswordField('password',validators=[Required(),EqualTo('new_password2',message="password must match")])
      new_password2=PasswordField('password',validators=[Required()])
      submit = SubmitField('Reset')

      def validate_email(self,field):
             user = User.query.filter_by(email=field.data).first()
             if user is None:
                raise ValidationError('the email address should be right!')

                       
