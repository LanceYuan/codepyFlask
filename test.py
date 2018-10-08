import redis

conn = redis.Redis(host="222.185.123.186", port=16379, db=0, password="LANCEyuan88")
data = conn.keys()
print(data)

class Foo(object):
    INSTANCE = None
    def __init__(self, *args, **kwargs):
        super(Foo, self).__init__(*args, **kwargs)
    def __new__(cls, *args, **kwargs):
        if Foo.INSTANCE:
            return Foo.INSTANCE
        else:
            super(Foo, cls).__new__(cls)

obj1 = Foo(name="Lance")
obj2 = Foo()
print(id(obj1), id(obj2))
