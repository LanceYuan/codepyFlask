from SQL_ORM import SQL_User, engine, Depart
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()

# 外键连表查询，返回2个对象.
result = session.query(SQL_User, Depart).join(Depart).all()

# 连表查询指定字段,默认会通过Foreign字段on条件
result = session.query(SQL_User.id, SQL_User.name, Depart.title).join(Depart).filter(SQL_User.id>1)
for row in result:
    print("1=====>", row)

# join的时候指定on的条件.
result = session.query(SQL_User.id, SQL_User.name, Depart.title).join(Depart, SQL_User.depart_id == Depart.id).all()
for row in result:
    print("2=====>", row)

# 通过relation查找外键关联对象.
result = session.query(SQL_User).join(Depart).all()
for row in result:
    print("3=====>", row.id, row.name, row.dp.title)

# 通过relation的backref反向查找指定部门人员.
result = session.query(Depart).filter(Depart.title == "技术").first()
for row in result.dep:
    print("4=====>", row.id, row.name)

# 通过relation创建数据.
# obj = SQL_User(name="JOY", dp=Depart(title="IT"))
# session.add(obj)

session.commit()
session.close()