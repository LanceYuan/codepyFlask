import datetime

class Base(object):
    SESSION_COOKIE_NAME = "session"
    SECRET_KEY = "flask"  # session加密处理需要.
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(seconds=60)  # session 保存时间.

class Dev(Base):
    DEBUG = True

class Prod(Base):
    DEBUG = False
