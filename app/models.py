from app import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin,AnonymousUserMixin
from app import loginmanager
from itsdangerous import TimedJSONWebSignatureSerializer as JsonSecret
from flask import current_app
from datetime import datetime

class user(db.Model,UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.VARCHAR(20))
    location = db.Column(db.String(64))
    about_me = db.Column(db.TEXT())
    register_time = db.Column(db.DateTime(),default=datetime.now)
    last_time = db.Column(db.DateTime(),default=datetime.now)
    email = db.Column(db.VARCHAR(20),unique=True)
    new_email = db.Column(db.VARCHAR(20),default="nomail")
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.BOOLEAN, default=False)
    role_id = db.Column(db.Integer,db.ForeignKey("roles.id"))

    def __init__(self, **kwargs):
        super(user, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config["MAIL_USERNAME"]:
                self.role = role.query.filter_by(permission = 0xff).first()
            else:
                self.role = role.query.filter_by(default = True).first()

    def can(self,permissions):
        return self.role is not None and (self.role.permission & permissions == permissions)

    def is_administer(self):
        return self.can(Permission.ADMINISTER)

    def visted(self):
        self.last_time = datetime.now()
        db.session.add(self)
        db.session.commit()


    @property
    def password(self):
        return AttributeError("password can not readable")

    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generator_confirmed_token(self, expire = 3600, email = ""):
        secret = JsonSecret(current_app.config["SECRET_KEY"], expire)
        if email == "":
            return secret.dumps({"confirmed":self.id})
        else:
            return secret.dumps({"new_email":email})

    def confirmed_email(self, token):
        secret = JsonSecret(current_app.config["SECRET_KEY"])
        try:
            data = secret.loads(token)
        except:
            return False
        if data.get("confirmed") == self.id:
            self.confirmed = True
            db.session.add(self)
            return True
        elif data.get("new_email") == self.new_email:
            self.email = self.new_email
            self.new_email = "nomail"
            db.session.add(self)
            return True
        else:
            return False
class role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer,primary_key=True)
    default = db.Column(db.BOOLEAN,default=False)
    name = db.Column(db.String(64))
    permission = db.Column(db.Integer)
    user = db.relationship("user", backref = "role", lazy = 'dynamic')

    @staticmethod
    def insert_roles():
        roles = {
            'User':(Permission.FOLLOW|
                    Permission.COMMENT|
                    Permission.WRITE_ARTICLES, True),
            'Moderator':(Permission.FOLLOW|
                         Permission.COMMENT|
                         Permission.WRITE_ARTICLES|
                         Permission.MODRATE_COMMENTS,False),
            'Adminster':(0xff,False)
        }
        for r in roles:
            tmprole = role.query.filter_by(name = r).first()
            if tmprole is None:
                tmprole = role(name = r)
            tmprole.permission = roles[r][0]
            tmprole.default = roles[r][1]
            db.session.add(tmprole)
        db.session.commit()

class Permission:
    FOLLOW = 0x01
    COMMENT = 0x02
    WRITE_ARTICLES = 0x04
    MODRATE_COMMENTS = 0x08
    ADMINISTER = 0x80

class AnonymousUser(AnonymousUserMixin):
    def can(self,permission):
        return False
    def is_administer(self):
        return False

class ForgetPwdUser():
    @classmethod
    def generator_forgetpwd_token(cls, id, expire = 600):
        secret = JsonSecret(current_app.config["SECRET_KEY"], expire)
        return secret.dumps({"forget_user_id":id})

    @classmethod
    def confirm_forgetpwd(cls, token):
        secret = JsonSecret(current_app.config["SECRET_KEY"])
        try:
            data = secret.loads(token)
        except:
            return None
        id = data.get("forget_user_id")
        if id is not None:
            tmpuser = user.query.get_or_404(id)
            return tmpuser
        return None


@loginmanager.user_loader
def load_user(user_id):
    return user.query.get(int(user_id))