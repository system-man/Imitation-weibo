from application import app
from . import main
from .forms import PostForm
from flask import render_template,url_for,redirect,session,abort,request,current_app
from flask_login import current_user
from application.models import Post,Permission,User
from application import db



@main.route('/',methods=['POST','GET'])
def index:
    form = PostForm()
    if current_user.can(Permission.Writer_article) and form.validate_on_submit:
         post=Post(
                  body=form.body.data,
                  author=current_user._get_current_object()
         )
         db.session.add(post)
         db.session.commit()
         
         return redirect(url_for('main.index'))
         # 为了显示某页中的记录， 要把 all() 换成 Flask-SQLAlchemy 提供的 paginate() 方法。
         # 页数是 paginate() 方法的第一个参数，也是唯一必需的参数。可选参数 per_page 用来指定每页显示的记录数量；
         # 如果没有指定，则默认显示 20 个记录。
         # 另一个可选参数为 error_out，当其设为 True 时（默认值），如果请求的页数超出了范围，则会返回 404 错误；
         # 如果设为 False，页数超出范围时会返回一个空列表。
         page= request.args.get('page',1,type=int)
         pagination=Post.query.order_by(Post.timestamp.desc()).paginate(page,per_page=current_app.config['FLASK_POSTS_PER_PAGE'],error_out=False)        posts=pagination.items
    return render_template('main/index.html',form=form,posts=posts,Permission=Permission,pagination=pagination)



@main.route('/user/<username>')
def user(username):
    user=User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    page= request.args.get('page',1,type=int)
    pagination=Post.query.order_by(Post.timestamp.desc()).paginate(page,per_page=current_app.config['FLASK_POSTS_PER_PAGE'],error_out=False)       
    posts=pagination.items
    return render_template('main/user.html',user=user,posts=posts,pagination=pagination)


@main.route('/post/<int:id>'):
def psot(id):
    post=Post.query.get_or_404(id)
    #在此处展示该文章的评论
         return redirect(url_for('main.post',id=post.id))
    return render_template('main/post.html',post=[post],coments=coments)



