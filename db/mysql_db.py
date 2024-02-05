import mysql.connector.pooling


# 数据库配置信息
__config = {
    "host": "192.168.0.104",
    "port": 3306,
    "user": "sysapl",
    "password": "root",
    "database": "vega"
}

# 初始化连接池
try:
    pool = mysql.connector.pooling.MySQLConnectionPool(
        **__config, pool_size=10)
except Exception as e:
    print(e)
