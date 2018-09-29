import datetime

class Base(object):
    SESSION_COOKIE_NAME = "session"
    SECRET_KEY = "flask"  # session加密处理需要.
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(days=7)  # session 保存时间.

class Dev(Base):
    DEBUG = True

class Prod(Base):
    DEBUG = False
