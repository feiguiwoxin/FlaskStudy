from app.main import main
from flask import render_template,abort,flash,redirect,url_for
from app.models import user,role
from app.main.forms import UserEditInfoForm,AdminEditInfoForm
from flask_login import current_user,login_required
from app import db
from app.decorator_permission import admin_required

@main.route("/")
def index():
    return render_template("index.html")

@main.route("/user/<username>")
def userinfo(username):
    tmpuser = user.query.filter_by(username = username).first()
    if tmpuser is None:
        abort(404)
    return render_template("userinfo.html", visted_user = tmpuser),200

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
    return render_template("editinfo.html", form = form)


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
    return render_template("editinfo.html", form = form)