from SQL_ORM import SQL_User, engine
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()
# 数据增加操作.
# obj = SQL_User(name="Lance")
# session.add(obj)
# session.add_all([
#     SQL_User(name="Lily"),
#     SQL_User(name="Yuan"),
# ])

# 查
result = session.query(SQL_User).all()
for row in result:
    print("1=====>",row.id, row.name)

result = session.query(SQL_User).filter(SQL_User.id > 1)
print(result) # 显示执行的SQL语句.
for row in result:
    print("2=====>",row.id, row.name)

result = session.query(SQL_User).filter(SQL_User.id >= 2).first()
print("3=====>", result.id, result.name)


# 删除操作
session.query(SQL_User).filter(SQL_User.id == 3).delete()

# 改操作
# session.query(SQL_User).filter(SQL_User.id == 1).update({SQL_User.name: "LanceYuan"}) # 通过类属性修改.
session.query(SQL_User).filter(SQL_User.id == 1).update({"name": "Lance"}) # 字段名称修改.
# 字符串在原数据上相加必须加上synchronize_session
session.query(SQL_User).filter(SQL_User.id == 1).update({"name": SQL_User.name+"Yuan"}, synchronize_session=False)

session.commit()
session.close()