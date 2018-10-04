from flask import Flask, request, redirect, render_template, session, url_for, jsonify, make_response, views
from functools import wraps
from flask_session import Session
from wtforms import Form
from wtforms.fields import simple
from wtforms.fields import html5
from wtforms.fields import core
from wtforms import widgets
from wtforms import validators
from DBpool import DataBase

app = Flask(__name__)
# app.config["DEBUG"] = True # 修改flask配置文件.
app.config.from_object("settings.Dev") # 通过setting.py配置
Session(app)

HOME_DATA = {
    1: {"name": "Lance", "age": 32, "gender": 1},
    2: {"name": "Lily", "age": 26, "gender": 0},
    3: {"name": "Father", "age": 62, "gender": 1},
    4: {"name": "Mather", "age": 61, "gender": 0},
}


# @app.before_request          # Flask 自带给所有视图装饰函数.
# def authBeforeRequest():
#     prev_url = request.path
#     if request.path == "/login/":
#         return None          # return None继续执行后面视图函数.
#     if session.get("user"):  # 从Session中获取用户、如果存在说明已认证、继续后续操作。
#         return None
#     return redirect("/login/?next={}".format(prev_url))

@app.before_request  # 所有请求之前执行的操作, 没有参数，没有返回值。继续后续视图函数操作.
def f1Before():
    print("before request.")

@app.after_request   # 所有请求之后执行的操作,必须接收1个参数Response,必须返回一个Response.
def f2After(response):
    print("after request.")
    return response


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


def homeFunc():
    return "HTML模板调用函数，并渲染返回数据."

@app.template_global()
def tmpFunc():
    return "template_global HTML直接调用，不需要在视图中显示的传递."


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


# strict_slashes: URL是否必须输入/结束符.
@app.route('/home/', methods=['GET', 'POST'], endpoint="homeInfo", strict_slashes=False)
@login_required
def home():
    # 将函数返回给前端HTML，前端HTML渲染时执行函数.
    return render_template('home.html', homeInfo=HOME_DATA, func=homeFunc)


@app.route('/detail/<int:nid>/', methods=['GET', 'POST'])
def detail(nid):
    data = HOME_DATA[nid]
    return render_template("detail.html", data=data)


@app.route('/delete/<int:nid>/', methods=['GET', 'POST'],)
def delete(nid):
    del HOME_DATA[nid]
    return redirect(url_for("homeInfo"))


# CBV: method指定请求的方式, decorators 基于CBV的装饰器.
class UserInfo(views.MethodView):
    methods = ["GET", "POST"]
    decorators = [login_required,]
    def get(self, *args, **kwargs):
        id = kwargs.get("nid")
        return "GET METHODS {}".format(id)
    def post(self, *args, **kwargs):
        id = kwargs.get("nid")
        return "POST METHODS {}".format(id)

# URL和CBV绑定. as_view参数指定endpoints名称.
app.add_url_rule("/user/<int:nid>/", None, view_func=UserInfo.as_view("UserInfo"))

class appMiddleWare(object):   # Flask中间件，在视图执行之前和之后自定义操作.
    def __init__(self, app):
        self.app = app
    def __call__(self, *args, **kwargs):
        print("befor")
        newApp = self.app(*args, **kwargs)
        print("after")
        return newApp


class RegisterForm(Form):
    name = simple.StringField(
        label='用户名',
        validators=[
            validators.DataRequired(message="用户名不能为空")
        ],
        widget=widgets.TextInput(),
        render_kw={'class': 'form-control'},
        default='alex'
    )

    pwd = simple.PasswordField(
        label='密码',
        validators=[
            validators.DataRequired(message='密码不能为空.')
        ],
        widget=widgets.PasswordInput(),
        render_kw={'class': 'form-control'}
    )

    pwd_confirm = simple.PasswordField(
        label='重复密码',
        validators=[
            validators.DataRequired(message='重复密码不能为空.'),
            validators.EqualTo('pwd', message="两次密码输入不一致") # 校验密码一致
        ],
        widget=widgets.PasswordInput(),
        render_kw={'class': 'form-control'}
    )

    email = html5.EmailField(
        label='邮箱',
        validators=[
            validators.DataRequired(message='邮箱不能为空.'),
            validators.Email(message='邮箱格式错误')
        ],
        widget=widgets.TextInput(input_type='email'),
        render_kw={'class': 'form-control'}
    )

    gender = core.RadioField(
        label='性别',
        choices=(
            (1, '男'),
            (2, '女'),
        ),
        coerce=int # int("1") 前端提交数据默认为字符串类型,coerce设置后端接收到后为int.
    )
    city = core.SelectField(
        label='城市',
        choices=(
            ('bj', '北京'),
            ('sh', '上海'),
        )
    )

    hobby = core.SelectMultipleField(
        label='爱好',
        choices=(
            (1, '篮球'),
            (2, '足球'),
        ),
        coerce=int
    )

    favor = core.SelectMultipleField(
        label='喜好',
        choices=(
            (1, '篮球'),
            (2, '足球'),
        ),
        widget=widgets.ListWidget(prefix_label=False),
        option_widget=widgets.CheckboxInput(),
        coerce=int,
        default=[1, ]
    )

@app.route("/wtlogin/", methods=["GET", "POST"])
def wtLogin():
    if request.method == "GET":
        forms = RegisterForm()
        return render_template("wtlogin.html", forms=forms)
    forms = RegisterForm(formdata=request.form)
    if forms.validate():
        data = forms.data  # 验证成功后获取到的数据.
        return jsonify(data)
    else:
        return render_template("wtlogin.html", forms=forms) # 提交错误时返回页面并提示错误信息.


class Userforms(Form):
    id = simple.StringField()
    service = core.SelectField(
        choices=(),
    )

    def __init__(self, *args, **kwargs):
        super(Userforms, self).__init__(*args, **kwargs)
        conn = DataBase()
        self.service.choices=conn.get_all("select * from userform", []) # 数据变化时,动态更新前端数据. 类的静态字段初始化时生产.


@app.route("/db/")
def db():
    forms = Userforms()
    return render_template("user_forms.html", forms=forms)

if __name__ == '__main__':
    app.wsgi_app = appMiddleWare(app.wsgi_app)
    app.run()
