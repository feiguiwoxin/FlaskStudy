from wtforms import StringField,TextAreaField,SubmitField,SelectField,BooleanField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired,Email,ValidationError,Length,Regexp
from app.models import role,user
from flask_pagedown.fields import PageDownField


class UserEditInfoForm(FlaskForm):
    location = StringField("地址：")
    about_me = TextAreaField("关于自己:")
    submit = SubmitField("提交")

class AdminEditInfoForm(FlaskForm):
    username = StringField("用户名:",validators=[DataRequired(),Length(1,20),
                Regexp('^[a-zA-Z][0-9a-zA-Z_.]*$',message='用户名只允许字母，数字或一些通用符号')])
    email = StringField("邮箱:",validators=[DataRequired(),Email()])
    role = SelectField("权限级别",coerce=int)
    location = StringField("地址：")
    about_me = TextAreaField("关于自己:")
    confirmed = BooleanField("已激活")
    submit = SubmitField("提交")

    def __init__(self, tmpuser, *args, **kwargs):
        super(AdminEditInfoForm, self).__init__(*args, **kwargs)
        self.role.choices = [(tmprole.id, tmprole.name)
                             for tmprole in role.query.order_by(role.name).all()]
        self.tmpuser = tmpuser

    def validate_email(self, field):
        if field.data != self.tmpuser.email \
            and user.query.filter_by(email = field.data).first():
            raise ValidationError("该email已被人注册，无法使用")

    def validate_username(self, field):
        if field.data != self.tmpuser.username \
            and user.query.filter_by(username = field.data).first():
            raise ValidationError("该用户名已被人注册，无法使用")

class PostForm(FlaskForm):
    body = PageDownField("想写点什么？", validators=[DataRequired()])
    submit = SubmitField("提交")

class CommmentForm(FlaskForm):
    body = StringField('请输入您的评论', validators=[DataRequired()])
    submit = SubmitField("提交")

