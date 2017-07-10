# coding:utf-8

from application import mail
from flask_mail import Message
from flask import render_template
from threading import Thread
from flask import current_app,render_template

def send_async_mail(app,msg):
    with app.app_context():   #创建程序上下文
         mail.send(msg)

def send_mail(recipient,subject,template,**kwargs):
    app=current_app._get_current_object()
    msg=Message(subject=app.config['FLASKY_MAIL_SUBJECT_PREFIX']+subject,sender=app.config['FLASKY_MAIL_SENDER'],recipients=[recipient])
    msg.body=render_template(template+'.txt',**kwargs)
    msg.html=render_template(template+'.html',**kwargs)
    thr =Thread(target=send_async_mail,args=[app,msg])
    thr.start()
    return thr
