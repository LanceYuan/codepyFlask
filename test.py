import redis

conn = redis.Redis(host="222.185.123.186", port=16379, db=0, password="LANCEyuan88")
data = conn.keys()
print(data)