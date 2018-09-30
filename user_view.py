from flask import Blueprint

uv = Blueprint('uv', __name__)

@uv.route("/user/")
def user():
    return "blue print user info."
