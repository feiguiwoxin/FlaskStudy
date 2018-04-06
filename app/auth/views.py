from app.auth import auth
from app.auth.forms import RegisterForm,LoginForm,ChangePwdForm,ChangeEmailForm,ResetForgetPwdForm
from flask import render_template,redirect,url_for,flash,request
from app.models import user,ForgetPwdUser
from app import db
from flask_login import login_user,logout_user,current_user,login_required
from app.email import sendmail

@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.visted()
    if current_user.is_authenticated \
        and not current_user.confirmed \
        and request.endpoint[:5] != "auth." \
        and request.endpoint != "static":
        return redirect(url_for("auth.unconfirmed"))

@auth.route("/unconfirmed")
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for("main.index"))
    return render_template("auth/unconfirmed.html")

@auth.route("/resend_confirmed")
@login_required
def resend_confirmed():
    if current_user.confirmed:
        return redirect(url_for("main.index"))
    sendmail("demo小站：新用户激活", current_user.email, "/email/email.html", current_user.generator_confirmed_token())
    flash('激活邮件已重发，请尽快登录邮箱处理(有效期1小时).')
    return redirect(url_for('main.index'))


@auth.route("/login", methods = ('GET', 'POST'))
def login():
    form = LoginForm()
    if form.validate_on_submit():
        myuser = user.query.filter_by(username = form.username.data).first()
        if myuser is None:
            flash("用户名不存在")
        else:
            if myuser.verify_password(form.password.data):
                login_user(myuser, form.remember_box.data)
                return redirect(request.args.get('next') or url_for("main.index"))
            else:
                flash("密码错误")
        return redirect(url_for("auth.login"))
    return render_template("auth/login.html",form = form)

@auth.route("/register", methods=('GET', 'POST'))
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if user.query.filter_by(username = form.username.data).first():
            flash("邮箱已被注册")
            return redirect(url_for("auth.register"))
        myuser = user(email = form.email.data, username = form.username.data,password = form.password.data)
        db.session.add(myuser)
        db.session.commit()
        sendmail("demo小站:新用户激活", myuser.email, "email/email.html",myuser.generator_confirmed_token())
        flash("已向您的注册邮箱发送激活邮件，请前往激活(有效期1小时)")
        return redirect(url_for("main.index"))
    return render_template("auth/register.html",form = form)

@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.index"))

@auth.route("/confirmed/<token>")
@login_required
def confirmed(token):
    if current_user.confirmed:
        return redirect(url_for("main.index"))
    elif current_user.confirmed_email(token):
        flash("激活成功")
    else:
        flash("您的链接已过期或不可用")

    return redirect(url_for("main.index"))

@auth.route("/confirmed_change_email/<token>")
@login_required
def confirmed_change_email(token):
    if current_user.new_email != "nomail":
        if current_user.confirmed_email(token):
            flash("新邮箱已激活")
            return redirect(url_for("main.userinfo", username = current_user.username))
    flash("链接已过期或不可用")
    return redirect(url_for("main.index"))

@auth.route("/changepassword",methods = ('GET','POST'))
@login_required
def change_password():
    form = ChangePwdForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            if current_user.verify_password(form.new_password.data):
                flash("新老密码一致，请更换新密码")
                return redirect(url_for("auth.change_password"))
            current_user.password = form.new_password.data
            flash("修改密码成功，请重新登录")
            logout_user()
            return redirect(url_for("auth.login"))
        else:
            flash("旧密码错误，修改失败")
            return redirect(url_for("auth.change_password"))
    return render_template("auth/change_password.html", form = form)

@auth.route("/changeemail",methods = ('GET','POST'))
@login_required
def change_email():
    form = ChangeEmailForm(1)
    if form.validate_on_submit():
        current_user.new_email = form.email.data
        sendmail("Demo小站：新邮箱激活" ,current_user.new_email,"/email/change_email_model.html",
                 current_user.generator_confirmed_token(email = current_user.new_email))
        flash("已向新邮箱发送激活链接，在激活之前，新邮箱不可用,激活有效期1小时")
        return redirect(url_for("main.index"))
    return render_template("auth/email_form.html", form = form)

@auth.route("/forgetpassword",methods = ('GET', 'POST'))
def forget_password():
    form = ChangeEmailForm(2)
    if form.validate_on_submit():
        tmpuser = user.query.filter_by(email = form.email.data).first()
        sendmail("Demo小站：重置密码", form.email.data, "email/reset_forget_password.html",
                 ForgetPwdUser.generator_forgetpwd_token(tmpuser.id))
        flash("已向你的注册邮箱发送重置密码链接，请前往重置密码(有效期10分钟)")
        return redirect(url_for("auth.login"))
    return render_template("auth/email_form.html", form = form)

@auth.route("/confirmed_forgetpwd/<token>", methods = ('GET', 'POST'))
def confirmed_forgetpwd(token):
    form = ResetForgetPwdForm()
    if form.validate_on_submit():
        tmpuser = ForgetPwdUser.confirm_forgetpwd(token)
        if tmpuser is not None:
            tmpuser.password = form.new_password.data
            flash("重置密码成功，请使用新密码登录")
            return redirect(url_for("auth.login"))
        else:
            flash("链接已过期或不可用")
            return redirect(url_for("main.index"))
    return render_template("auth/reset_forgetpwd.html", form = form)

