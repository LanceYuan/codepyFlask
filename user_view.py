from flask import Blueprint

uv = Blueprint('uv', __name__)

# 只有当前蓝图才应用当前before_request
@uv.before_request
def admin_request():
    print("admin request.")


@uv.route("/user/")
def user():
    return "blue print user info."
