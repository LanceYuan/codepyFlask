from DBUtils.PooledDB import PooledDB
import pymysql
POOL = PooledDB(
    creator=pymysql, # 使用链接数据库的模块
    maxconnections=6, # 连接池允许的最大连接数,0或None表示不限制
    mincached=2, # 初始时链接池中至少创建的空闲链接，0表示不创建
    maxcached=5, # 链接池中最多闲置的链接，0或None表示不限制
    maxshared=3, # 链接池中最多共享的链接数据
    blocking=True, # 连接池中如果没有可用连接后是否阻塞等待。True 等待、False不等待报错
    maxusage=None, # 一个链接最多被重复使用的次数，None表示不限制
    setsession=[], # 会话前执行的命令列表
    ping=0, # 检查服务是否可用
    # pymysql 连接配置
    host="127.0.0.1",
    user="lance",
    password="LANCEyuan88",
    database="codepy",
    charset="utf8"
)


class DataBase(object):
    def conn(self):
        conn = POOL.connection()
        # cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor = conn.cursor()
        # cursor.execute("select * from app01_book")
        return conn, cursor
    def get_one(self, sql, args):
        conn, cursor = self.conn()
        cursor.execute(sql, args)
        data = cursor.fetchone()
        cursor.close()
        conn.close()
        return data
    def get_all(self, sql, args):
        conn, cursor = self.conn()
        cursor.execute(sql, args)
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return data

