from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, Date, DateTime, create_engine, ForeignKey
from sqlalchemy.orm import relationship
Base = declarative_base()


class Depart(Base):
    __tablename__ = "depart"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(32), index=True, nullable=False)


class SQL_User(Base):
    __tablename__ = "sql_user"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(32), index=True, nullable=False)
    depart_id = Column(Integer, ForeignKey("depart.id"))
    dp = relationship("Depart", backref="dep")


class Student(Base):
    __tablename__ = "student"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(32), index=True, nullable=False)


class Course(Base):
    __tablename__ = "course"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(32), index=True, nullable=False)


class Student_Course(Base):
    __tablename__ = "student_course"
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey("student.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("course.id"), nullable=False)

engine = create_engine(
    "mysql+pymysql://lance:LANCEyuan88@127.0.0.1:3306/codepy?charset=utf8",
    max_overflow=0, # 超过连接池大小外最多创建的连接。
    pool_size=5, # 连接池大小
    pool_timeout=30, # 线程等待连接池最长时间，超时抛出异常.
    pool_recycle=-1, # 多久之后对线程池中的连接进行回收（重置）
)
Base.metadata.create_all(engine) # 连接数据库，并根据类在数据库中创建表.
# Base.metadata.drop_all(engine) # 连接数据库，并在数据库中删除对应的表.

if __name__ == "__main__":
    conn = engine.raw_connection() # 通过SQLAlchemy的engine对像执行原生的SQL语句.
    cursor = conn.cursor()
    cursor.execute("select * from sql_user")
    data = cursor.fetchall()
    print(data)
