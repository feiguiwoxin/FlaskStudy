from app import mail
from flask_mail import Message
from threading import Thread
from flask import current_app,render_template

def send_async_mail(app, msg):
    with app.app_context():
        mail.send(msg)

def sendmail(subject, to, email_model_addr, token):
    app = current_app._get_current_object()
    msg = Message(subject=subject,sender=current_app.config["MAIL_USERNAME"],recipients=[to])
    msg.html = render_template(email_model_addr, token = token)
    t = Thread(target=send_async_mail,args=[app, msg])
    t.start()