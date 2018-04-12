from flask import Blueprint

bp = Blueprint('flaskr', __name__)

from . import flaskr
