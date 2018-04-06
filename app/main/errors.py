from app.main import main
from flask import render_template

@main.app_errorhandler(404)
def error404(e):
    return render_template("404.html"),404

@main.app_errorhandler(403)
def error403(e):
    return render_template("403.html"),403

@main.app_errorhandler(500)
def error500(e):
    return render_template("500.html"),500
