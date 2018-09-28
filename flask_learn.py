from flask import Flask, request, redirect, render_template, session, url_for, jsonify, make_response
from functools import wraps


app = Flask(__name__)
print(app.config)
# app.config["DEBUG"] = True # 修改flask配置文件.
app.config.from_object("settings.Dev") # 通过setting.py配置

HOME_DATA = {
    1: {"name": "Lance", "age": 32, "gender": 1},
    2: {"name": "Lily", "age": 26, "gender": 0},
    3: {"name": "Father", "age": 62, "gender": 1},
    4: {"name": "Mather", "age": 61, "gender": 0},
}


@app.before_request          # Flask 自带给所有视图装饰函数.
def authBeforeRequest():
    prev_url = request.path
    if request.path == "/login/":
        return None          # return None继续执行后面视图函数.
    if session.get("user"):  # 从Session中获取用户、如果存在说明已认证、继续后续操作。
        return None
    return redirect("/login/?next={}".format(prev_url))

# 自定义认证函数.
def login_required(func):
    @wraps(func)
    def inner(*args, **kwargs):
        prev_url = request.path
        user = session.get("user")
        if user:
            res = func(*args, **kwargs)
            return res
        else:
            return redirect("/login/?next={}".format(prev_url))
    return inner

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/login/', methods=['GET', 'POST'], endpoint="login") # endpoint反向生产URL.默认函数名.
def login():
    prev_url = request.args.get("next", "/index/1/") # 获取登陆之前的URL.
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username.lower() == 'admin' and password == 'pass':
            session["user"] = username
            return redirect(prev_url)
        else:
            return redirect('/login/')
    return render_template('login.html')


@app.route('/index/<int:nid>/') # URL传参.
def index(nid):
    print(url_for("index", nid=nid)) # url_for反向生产URL注意传递参数.
    session_user = session.get("user", None)
    if session_user:
        response = make_response(render_template('index.html'))
        response.headers["name"] = "lance" # 设置响应头部信息.
        response.set_cookie("key", "val")  # 设置响应Cookie.
        return response
    else:
        return redirect('/login/')


@app.route('/data/', methods=['GET', 'POST'])
def data():
    data = request.data.decode("utf8")
    print(data)
    print(request.form)
    response = make_response(jsonify(data))
    return response


@app.route('/home/', methods=['GET', 'POST'], endpoint="homeInfo")
@login_required
def home():
    return render_template('home.html', homeInfo=HOME_DATA)


@app.route('/detail/<int:nid>/', methods=['GET', 'POST'])
def detail(nid):
    data = HOME_DATA[nid]
    return render_template("detail.html", data=data)


@app.route('/delete/<int:nid>/', methods=['GET', 'POST'])
def delete(nid):
    del HOME_DATA[nid]
    return redirect(url_for("homeInfo"))

if __name__ == '__main__':
    app.run()
