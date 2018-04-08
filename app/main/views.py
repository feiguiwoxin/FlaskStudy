from app.main import main
from flask import render_template,abort,flash,redirect,url_for,request
from app.models import user,role,Post,Permission
from app.main.forms import UserEditInfoForm,AdminEditInfoForm,PostForm
from flask_login import current_user,login_required
from app import db
from app.decorator_permission import admin_required

@main.route("/",methods = ('GET','POST'))
def index():
    form = PostForm()
    if current_user.can(Permission.WRITE_ARTICLES) \
        and form.validate_on_submit():
        post = Post(body = form.body.data,user = current_user._get_current_object())
        db.session.add(post)
        return redirect(url_for("main.index"))
    page = request.args.get("page", 1, type=int)
    pagination = Post.query.order_by(Post.create_time.desc()).paginate(page, per_page=15, error_out=False)
    posts = pagination.items
    return render_template("index.html", form = form, posts = posts, pagination = pagination)

@main.route("/user/<username>")
def userinfo(username):
    tmpuser = user.query.filter_by(username = username).first()
    if tmpuser is None:
        abort(404)
    page = request.args.get("page", 1, type=int)
    pagination = tmpuser.posts.order_by(Post.create_time.desc()).paginate(page, per_page=10, error_out=False)
    posts = pagination.items
    return render_template("userinfo.html", visted_user = tmpuser, posts = posts, pagination = pagination),200

@main.route("/editinfo", methods = ('GET', 'POST'))
@login_required
def editinfo():
    form = UserEditInfoForm()
    if form.validate_on_submit():
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash("用户信息已更新~~")
        return redirect(url_for("main.userinfo", username = current_user.username))
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template("edit_userinfo.html", form = form)


@main.route("/editinfo/<int:id>", methods = ('GET', 'POST'))
@login_required
@admin_required
def editinfo_admin(id):
    tmpuser = user.query.get_or_404(id)
    form = AdminEditInfoForm(tmpuser = tmpuser)
    if form.validate_on_submit():
        tmpuser.email = form.email.data
        tmpuser.username = form.username.data
        tmpuser.location = form.location.data
        tmpuser.about_me = form.about_me.data
        tmpuser.confirmed = form.confirmed.data
        tmpuser.role = role.query.get(form.role.data)
        flash("用户信息已更新~~")
        return redirect(url_for("main.userinfo", username = tmpuser.username))
    form.email.data = tmpuser.email
    form.username.data = tmpuser.username
    form.location.data = tmpuser.location
    form.about_me.data = tmpuser.about_me
    form.confirmed.data = tmpuser.confirmed
    form.role.data = tmpuser.role_id
    return render_template("edit_userinfo.html", form = form)

@main.route("/post/<int:id>")
def post(id):
    post = Post.query.get_or_404(id)
    return render_template("post.html", posts = [post])

@main.route("/edit_post/<int:id>", methods = ('GET', 'POST'))
@login_required
def edit_post(id):
    post = Post.query.get_or_404(id)
    if current_user != post.user and not current_user.is_administer():
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.body = form.body.data
        db.session.add(post)
        flash("博文修改完毕")
        return redirect(url_for("main.post", id = id))
    form.body.data = post.body
    return render_template("edit_post.html",form = form)