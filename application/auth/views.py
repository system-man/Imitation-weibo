# coding:utf-8

from . import auth
from ..models import User,Post,Role,Permission
from application import db
from .forms import RegisterForm,LoginForm,editprofileForm,admineditprofileForm,changepasswordForm,resetpasswordForm,requestresetpasswordForm
from ..email import send_mail
from flask import render_template,redirect,url_for,flash,request
from flask_login import login_user,current_user

@auth.route('/register',methods=['GET','POST'])
def register():
    form=RegisterForm()
    if form.validate_on_submit():
          user=User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data,
                    name=form.name.data,
                    location=form.location.data,
                    aboutme=form.aboutme.data)
          db.session.add(user)
          db.session.commit()
          token = user.generate_confirmation_token()     #注册后发送确认邮件
          send_mail(user.email,'confirm your registeration!','auth/mail/confirm',user=user,token=token)
          flash("A confirmation email has been sent to you!")
          return redirect(url_for('auth.login'))
    return render_template('auth/register.html',form=form)            
             
    
@auth.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
       user=User.query.filter_by(username=form.username.data).first()
       if user is not None and user.verify_password(form.password.data):
            login_user(user,form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
       flash("invalid password or username!")
    return render_template('auth/login.html',form=form)

          
from flask_login import current_user,login_required

@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    '''
    summary: 用户收到账户确认邮件，并确认
    return:再次登录
    '''
    if current_user.confirmed:
       return redirect(url_for('auth.login'))
    if current_user.confirm(token):
       flash("you have confirmed your account!")
    else:
       flash("The confirm link is not validate")
    return redirect(url_for('auth.login'))

#过滤未确认的用户
@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
       current_user.ping()
       if not current_user.confirmed and request.endpoint[:5] != 'auth.' and request.endpoint[:5] != 'static':
            return redirect(url_for('auth.unconfirmed'))

@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
          return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')

@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_mail(current_user.email,'confirm your registeration!','auth/mail/confirm',user=current_user,token=token)
    flash("a new confirmation email has been send to you!")
    return redirect(url_for('auth.login'))


from flask_login import logout_user

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash("you have logout your account!")
    return redirect(url_for('main.index'))

@auth.route('/change_password',methods=['GET','POST'])
@login_required
def change_password():
    form = changepasswordForm()
    if form.validate_on_submit():
       current_user.password = form.new_password.data
       db.session.add(current_user)
       db.session.commit()
       flash('your password has been changed succcessfully!')
       return redirect(url_for('auth.login'))
    return render_template('auth/change_password.html',form=form)       
    
@auth.route('/request_reset_password',methods=['GET','POST'])
def request_reset_password():
    form = requestresetpasswordForm()
    if not current_user.is_anonymous:
       return redirect(url_for('main.index'))
    if form.validate_on_submit():
       user=User.query.filter_by(email=form.email.data).first()
       if user:
          token = user.generate_confirmation_token()
          send_mail(user.email,'reset your password!','auth/mail/reset_password',user=user,token=token)
          flash("A resetpassword_email has been sent to you!")
          return redirect(url_for('auth.login'))
    return render_template('auth/request_resetpassword.html',form=form)

@auth.route('/reset_password/<token>',methods=['GET','POST'])
def reset_password(token):
   
    if not current_user.is_anonymous:
       return redirect(url_for('main.index'))
    form = resetpasswordForm()
    if form.validate_on_submit():
       user = User.query.filter_by(email=form.email.data).first()
       if user.reset_password(token=token,new_password=form.new_password.data):
          flash('your password has been reset!')
          return redirect(url_for('auth.login'))
       else:
          flash('The resetpassword email has been invalid! pleasemaile get a new email')
          return redirect(url_for('auth.request_reset_password'))
    return render_template('auth/reset_password.html',form=form)

@auth.route('/editprofile',methods=['GET','POST'])  #用户修改自己资料
@login_required
def edit_profile():
    form = editprofileForm()
    if form.validate_on_submit():
        current_user.username=form.username.data
        current_user.location=form.location.data
        current_user.aboutme=form.aboutme.data
        db.session.add(current_user)
        flash('your profile has been changed!')
        return redirect(url_for('main.user',username=current_user.username))
    form.username.data=current_user.username
    form.location.data=current_user.location
    form.aboutme.data=current_user.aboutme
    return render_template('auth/editprofile.html',form=form)



# 管理员对所有人资料的修改
from ..decorator import admin_required,permission_required
@auth.route('/admineditprofile/<int:id>',methods=['GET','POST'])
@login_required
@admin_required
def admin_editprofile(id):
    user=User.query.get_or_404(int(id))
    form=admineditprofileForm(user)
    if form.validate_on_submit():
        user.email=form.email.data
        user.username=form.username.data
        user.confirmed=form.confirmed.data
        user.role=Role.query.get(form.role.data)
        user.name=form.name.data
        user.location=form.location.data
        user.aboutme=form.aboutme.data
        db.session.add(user)
        flash('The profile has been updated!')
        return redirect(url_for('main.user',username=user.username))
    form.email.data=user.email
    form.username.data=user.username
    form.confirmed.data=user.confirmed
    form.role.data=user.role_id
    form.name.data=user.name
    form.location.data=user.location
    form.aboutme.data=user.aboutme
    return render_template('auth/admineditprofile.html',form=form,user=user)

@auth.route('/allprofiles')
@login_required
@admin_required
def show_all_people():
    administers=User.query.filter_by(role_id=2).all()
    moderators=User.query.filter_by(role_id=1).all()
    users=User.query.filter_by(role_id=3).all()

    return render_template('auth/allpeople.html', administers=administers, moderators=moderators, users=users)
