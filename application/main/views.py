from application import app
from . import main
from .forms import PostForm
from flask import render_template,url_for,redirect,session,abort,request,current_app
from flask_login import current_user
from application.models import Post
from application import db



@main.route('/',methods=['POST','GET'])
def index:
    from = PostForm()
    if form.validate_on_submit:
         post=Post(
                  body=form.body.data,
                  auth=current_user._get_current_object()
         )
         db.session.add(post)
         db.session.commit()
         
         return redirect(url_for('main.index'))

