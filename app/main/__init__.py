from flask import Blueprint
from app.models import Permission

main = Blueprint('main',__name__)

@main.app_context_processor
def insert_permission():
    return dict(Permission = Permission)

from app.main import errors,views
