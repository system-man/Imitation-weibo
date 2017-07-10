# coding:utf-8

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import Required

class PostForm(FlaskForm):
     #发布微博的表单类
     body = TextAreaField("what is on your mind?",validators=[Required()])
     submit= SubmitField("发布微博")



class ComentForm(FlaskForm):
     '''
     评论表单
     '''
     body = StringField("say something~",validators=[Required()])
     submit= SubmitField("评论")

