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
# session.query(SQL_User).filter(SQL_User.id == 3).delete()

# 改操作
# session.query(SQL_User).filter(SQL_User.id == 1).update({SQL_User.name: "LanceYuan"}) # 通过类属性修改.
session.query(SQL_User).filter(SQL_User.id == 1).update({"name": "Lance"}) # 字段名称修改.
# 字符串在原数据上相加必须加上synchronize_session
session.query(SQL_User).filter(SQL_User.id == 1).update({"name": SQL_User.name+"Yuan"}, synchronize_session=False)

# 查找指定字段.
result = session.query(SQL_User.id, SQL_User.name).all() # 获取指定字段.
print(result)

# SQL： select sql_user.id,sql_user.name as cname from sql_user;
result = session.query(SQL_User.id, SQL_User.name.label("cname")).all()
for row in result:
    print("4=====>", row)

# filter 多个条件之间且的关系.
result = session.query(SQL_User.id, SQL_User.name).filter(SQL_User.id>=1, SQL_User.name=="LanceYuan")
for row in result:
    print("5=====>", row)

# SQL查询中的between.
result = session.query(SQL_User.id, SQL_User.name).filter(SQL_User.id.between(1,3), SQL_User.name=="Lily")
for row in result:
    print("6=====>", row)

# SQL查询中的in操作.
result = session.query(SQL_User.id, SQL_User.name).filter(SQL_User.id.in_([1,2,3]))
for row in result:
    print("7=====>", row)

# SQL查询中的in操作的子查询.
result = session.query(SQL_User.id, SQL_User.name).filter(SQL_User.id.in_(session.query(SQL_User.id).filter(SQL_User.id>1)))
for row in result:
    print("8=====>", row)

# SQL查询中的and、or操作.
from sqlalchemy import and_, or_
result = session.query(SQL_User.id, SQL_User.name).filter(and_(SQL_User.id>=1, SQL_User.name=="LanceYuan"))
for row in result:
    print("9=====>", row)

result = session.query(SQL_User.id, SQL_User.name).filter(or_(SQL_User.id>2, SQL_User.name=="LanceYuan"))
for row in result:
    print("10=====>", row)
# and和or的嵌套操作.
result = session.query(SQL_User.id, SQL_User.name).filter(
    or_(
        SQL_User.id>2,
        and_(SQL_User.id<4, SQL_User.name=="Lily"),
    )
)
for row in result:
    print("11=====>", row)

# filter_by传递的为参数，内部调用的是filter.
result = session.query(SQL_User.id, SQL_User.name).filter_by(name="Lily")
for row in result:
    print("12=====>", row)

# SQL中通配符操作
result = session.query(SQL_User.id, SQL_User.name).filter(SQL_User.name.like("L%"))
for row in result:
    print("13=====>", row)

# 查询切片操作
result = session.query(SQL_User.id, SQL_User.name)[1:3]
for row in result:
    print("14=====>", row)

# SQL 排序操作.
result = session.query(SQL_User.id, SQL_User.name).order_by(SQL_User.id.desc())
for row in result:
    print("15=====>", row)

# 分组,默认选择第一条数据.
result = session.query(SQL_User.id, SQL_User.name, SQL_User.depart_id).group_by(SQL_User.depart_id)
for row in result:
    print("16=====>", row)

# 分组+聚合函数.
from sqlalchemy import func
result = session.query(SQL_User.id, SQL_User.name, func.count(SQL_User.depart_id)).group_by(SQL_User.depart_id)
for row in result:
    print("17=====>", row)

# 分组+聚合筛选. 根据部门分组，且部门中人数大于1的结果.
result = session.query(SQL_User.id, SQL_User.name, func.count(SQL_User.depart_id)).group_by(SQL_User.depart_id).having(func.count(SQL_User.depart_id)>1)
for row in result:
    print("18=====>", row)

# SQL union 联合查询. union去重，union_all不去重.
q1 = session.query(SQL_User.id, SQL_User.name).filter(SQL_User.id>1)
q2 = session.query(SQL_User.id, SQL_User.name).filter(SQL_User.id<4)
result1 = q1.union(q2)
result2 = q1.union_all(q2)
for row in result1:
    print("19=====>", row)
for row in result2:
    print("20=====>", row)
session.commit()
session.close()