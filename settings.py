import datetime
import redis

class Base(object):
    SESSION_COOKIE_NAME = "session"
    SECRET_KEY = "flask"  # session加密处理需要.
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(days=7)  # session 保存时间.
    SESSION_TYPE = "redis"
    SESSION_REDIS = redis.Redis(host="222.185.123.186", port=16379, db=1, password="LANCEyuan88") # 配置redis作为session存储.

class Dev(Base):
    DEBUG = True

class Prod(Base):
    DEBUG = False
