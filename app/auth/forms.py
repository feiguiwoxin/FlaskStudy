from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField,BooleanField
from wtforms.validators import DataRequired,Email,EqualTo,ValidationError,Regexp,Length
from app.models import user
from flask_login import current_user

class RegisterForm(FlaskForm):
    email = StringField("邮箱:",validators=[DataRequired(),Email()])
    username = StringField("用户名:",validators=[DataRequired(),Length(1,20),
                Regexp('^[a-zA-Z][0-9a-zA-Z_.]*$',message='用户名只允许字母，数字或一些通用符号')])
    password = PasswordField("密码:",validators=[DataRequired(),EqualTo('repeatpassword', message="密码不一致")])
    repeatpassword = PasswordField("重复密码:",validators=[DataRequired(),Length(3,9,"密码长度必须在3-9位之间")])
    submit = SubmitField("提交")

    def validate_email(self, field):
        if user.query.filter_by(email = field.data).first():
            raise ValidationError("该email已被人注册，无法使用")

    def validate_username(self, field):
        if user.query.filter_by(username = field.data).first():
            raise ValidationError("该用户名已被人注册，无法使用")

class LoginForm(FlaskForm):
    username = StringField("用户名:", validators=[DataRequired()])
    password = PasswordField("密码:", validators=[DataRequired()])
    remember_box = BooleanField("保持登录状态？")
    submit = SubmitField("提交")

class ChangePwdForm(FlaskForm):
    password = PasswordField('旧密码', validators=[DataRequired()])
    new_password = PasswordField('新密码', validators=[DataRequired(), Length(3, 9, "密码长度必须在3-9位之间")])
    new_password2 = PasswordField('确认新密码', validators=[DataRequired(), EqualTo('new_password', "密码不一致")])
    submit = SubmitField("提交")

class ChangeEmailForm(FlaskForm):
    email = StringField("邮箱", validators=[DataRequired(),Email()])
    submit = SubmitField("提交")

    def __init__(self, type, *args, **kwargs):
        super(ChangeEmailForm, self).__init__(*args, **kwargs)
        self.type = type

    def validate_email(self, field):
        if self.type == 1:
            if field.data == current_user.email:
                raise ValidationError("请不要使用旧邮箱！")
            else:
                if user.query.filter_by(email = field.data).first():
                    raise ValidationError("该邮箱已被其他用户使用,请更换邮箱")
        elif self.type == 2:
            if not user.query.filter_by(email = field.data).first():
                raise ValidationError("对不起，找不到使用该邮箱注册的用户")

class ResetForgetPwdForm(FlaskForm):
    new_password = PasswordField('新密码', validators=[DataRequired(), Length(3, 9, "密码长度必须在3-9位之间")])
    new_password2 = PasswordField('确认新密码', validators=[DataRequired(), EqualTo('new_password', "密码不一致")])
    submit = SubmitField("提交")
