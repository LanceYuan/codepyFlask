from SQL_ORM import Student, Course, Student_Course, engine
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()

# 增加基础数据.
# session.add_all([
#     Student(name="lance"),
#     Student(name="lily"),
#     Course(title="Python"),
#     Course(title="Go"),
# ])

# 为ID1学生绑定2门课程.
# session.add_all([
#     Student_Course(student_id=1, course_id=1),
#     Student_Course(student_id=1, course_id=2),
# ])
# session.add(Student_Course(student_id=2, course_id=1))

# 查询所有学生关联的课程名称，注意isouter=True保证查询到所有数据.
result = session.query(Student_Course.id, Student.name, Course.title).join(Student, Student_Course.student_id==Student.id, isouter=True).join(Course, Student_Course.course_id==Course.id).order_by(Student_Course.id.desc())
for row in result:
    print("1=====>", row)

# 查询lance用户选择的所有课程名称.
result = session.query(Student_Course.id, Student.name, Course.title).join(Student, Student_Course.student_id==Student.id, isouter=True).join(Course, Student_Course.course_id==Course.id).filter(Student.name=="lance").order_by(Student_Course.id.desc())
for row in result:
    print("2=====>", row)
# 通过relationship简化查询.
stu_obj = session.query(Student).filter(Student.name=="lance").first()
for row in stu_obj.course_list:
    print("3=====>", stu_obj.name, row.title)
cor_obj = session.query(Course).filter(Course.title=="Python").first()
for row in cor_obj.student_list:
    print("4=====>", cor_obj.title, row.name)

# 通过relationship新增数据. 增加课程、增加2学生，并都选择新的课程.
# cor_obj = Course(title="java")
# cor_obj.student_list = [
#     Student(name="s1"),
#     Student(name="s2"),
# ]
# session.add(cor_obj)

# SQLalchemy 执行原生SQL.
cursor = session.execute("select * from student")
data = cursor.fetchall()
print(data)

session.commit()
session.close()