from pymongo import MongoClient

try:
    client = MongoClient(
        host="192.168.0.104",
        port=27017,
        username="admin",
        password="test1234"
    )
except Exception as e:
    print(e)