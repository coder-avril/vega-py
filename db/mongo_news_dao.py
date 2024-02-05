from bson import ObjectId
from db.mongo_db import client

class MongoNewsDao:
    # 添加新闻正文记录
    def insert(self, title, content):
        try:
            client.vega.news.insert_one({"title": title, "content": content})
        except Exception as e:
            print(e)

    # 查找新闻的主键值
    def search_id(self, title):
        try:
            news = client.vega.news.find_one({"title": title})
            return str(news["_id"])
        except Exception as e:
            print(e)

    # 更新新闻
    def update(self, _id, title, content):
        try:
            client.vega.news.update_one(
                {"_id": ObjectId(_id)},
                {"$set": {"title": title, "content": content}}
            )
        except Exception as e:
            print(e)

    def search_content_by_id(self, _id):
        try:
            news = client.vega.news.find_one({"_id": ObjectId(_id)})
            return news["content"]
        except Exception as e:
            print(e)

    def delete_by_id(self, _id):
        try:
            client.vega.news.delete_one({"_id": ObjectId(_id)})
        except Exception as e:
            print(e)