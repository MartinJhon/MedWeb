import redis
r  = redis.Redis(host='localhost',port=6379,decode_responses=True)
# print(r.get('name'))
#
# print(r.set('name','lisi'))
#
# print(r.get('name'))
#
# print(r.mget('name','age','age'))

# print(r.hgetall('stu001'))
# print(r.hget('stu001','name'))
# r.hset('stu002','iphone','12345656788')
# print(r.hgetall('stu002'))
# r.lpush('list1','kkk')
# print(r.lrange('list1',0,-1))
# print(r.rpop('list1'))
a = r.lrange('list1',0,-1)

for i in a:
    print(i)
c = r.smembers('myset')
print(c)

b = r.hgetall('stu001')
print(b)
