# coding: utf-8
from . import main
from .forms import PostForm,CommentForm
from flask import render_template,flash,url_for,redirect,session,abort,request,current_app,make_response
from flask_login import current_user,login_required
from application.models import Post,Permission,User,Comment
from application import db
from ..decorator import permission_required


@main.route('/',methods=['GET','POST'])
def index():
    form = PostForm()
    if current_user.can(Permission.Write_article) and form.validate_on_submit():
         post=Post(
                  body=form.body.data,
                  author=current_user._get_current_object()
         )
         db.session.add(post)
         db.session.commit()
         
         return redirect(url_for('main.index'))
         #为了显示某页中的记录， 要把 all() 换成 Flask-SQLAlchemy 提供的 paginate() 方法。
         #页数是 paginate() 方法的第一个参数，也是唯一必需的参数。可选参数 per_page 用来指定每页显示的记录数量；
         #如果没有指定，则默认显示 20 个记录。
         #另一个可选参数为 error_out，当其设为 True 时（默认值），如果请求的页数超出了范围，则会返回 404 错误；
         #如果设为 False，页数超出范围时会返回一个空列表。
    show_followed=False
    page= request.args.get('page',1,type=int)
    if current_user.is_authenticated:
          show_followed = bool(request.cookies.get('show_followed',''))
    if show_followed:
          query=current_user.followed_posts
    else:
          query=Post.query
    pagination=query.order_by(Post.timestamp.desc()).paginate(page,per_page=current_app.config['FLASK_POSTS_PER_PAGE'],error_out=False)
    posts=pagination.items

    return render_template('main/index.html',
        show_followed=show_followed,
        form=form,posts=posts,
        pagination=pagination)

@main.route('/all')
@login_required
def show_all():
    resp=make_response(redirect(url_for('main.index')))
    resp.set_cookie('show_followed','',max_age=30*24*60*60)
    return resp

@main.route('/followed')
@login_required
def show_followed():
    resp=make_response(redirect(url_for('main.index')))
    resp.set_cookie('show_followed','1',max_age=30*24*60*60)
    return resp

@main.route('/user/<username>')
def user(username):
    user=User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    page= request.args.get('page',1,type=int)
    pagination=user.posts.order_by(Post.timestamp.desc()).paginate(page,per_page=current_app.config['FLASK_POSTS_PER_PAGE'],error_out=False)       
    posts=pagination.items
    return render_template('main/user.html',user=user,posts=posts,pagination=pagination)

@main.route('/follow/<username>')
@login_required
@permission_required(Permission.Follow)
def follow(username):
    user=User.query.filter_by(username=username).first()
    if user is None:
       flash("the user does not exists!")
       return redirect(url_for('main.index'))
    if current_user.is_following(user):
       return redirect(url_for('main.user',username=username))
    current_user.follow(user)
    flash('you have successfully follow %s' % user.username)
    return redirect(url_for('main.user', username=username))

@main.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user=User.query.filter_by(username=username).first()
    if user is None:
       flash("the user does not exists!")
       return redirect(url_for('main.index'))
    if not current_user.is_following(user):
       flash('you have not followed th user yet!')
       return redirect(url_for('main.user',username=username))
    current_user.unfollow(user)
    flash('you have successfully unfollow %s' % username)
    return redirect(url_for('main.user', username=username))


@main.route('/followers/<username>')
def followers(username):
    user=User.query.filter_by(username=username).first()
    if user is None:
       flash('the user does not exists!')
       return redirect(url_for('main.index'))
    page = request.args.get('page',1,type=int)
    pagination=user.followers.paginate(
           page,per_page=current_app.config['FLASK_POSTS_PER_PAGE'],
           error_out=False)
    follows = [{'user':item.follower,'timestamp':item.timestamp} for item in pagination.items]
    return render_template(
         'main/follows.html',title='粉丝',user=user,
         endpoint='main.followers',pagination=pagination,
         follows=follows)

@main.route('/followed-by/<username>')
def followed(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('the user does not exists!')
        return redirect(url_for('main.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followed.paginate(
        page, per_page=current_app.config['FLASK_POSTS_PER_PAGE'],
        error_out=False)
    follows = [{'user': item.followed, 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template(
        'main/follows.html', user=user, title="关注",
        endpoint='main.followed', pagination=pagination,
        follows=follows)

@main.route('/post/<int:id>',methods=['GET','POST'])
def post(id):
    post=Post.query.get_or_404(id)
    form=CommentForm()
    if form.validate_on_submit():
       comment = Comment(
             body = form.body.data,post=post,author=current_user._get_current_object())
       db.session.add(comment)
       return redirect(url_for('main.post', id=post.id))
    comments=post.comments.order_by(Comment.timestamp.desc()).all()
    return render_template('main/post.html',posts=[post],comments=comments,form=form)



