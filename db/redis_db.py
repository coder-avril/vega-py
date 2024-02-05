import redis


# 初始化Redis连接池
try:
    pool = redis.ConnectionPool(
        host="192.168.0.104",
        port=6379,
        password="sysapl",
        db=1,
        max_connections=25
    )
except Exception as e:
    print(e)