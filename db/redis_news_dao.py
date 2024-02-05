import redis
from db.redis_db import pool


class RedisNewsDao:
    def insert(self, _id, title, username, _type, content, is_top, created_time):
        """
        向Redis中保存审核过的新闻
        :param _id: 新闻ID
        :param title: 新闻标题
        :param username: 作者
        :param _type: 类型
        :param content: 新闻内容
        :param is_top: 是否置顶
        :param created_time: 作成时间
        """
        try:
            con = redis.Redis(connection_pool=pool)
            con.hmset(_id, {
                "title": title,
                "author": username,
                "type": _type,
                "content": content,
                "is_top": is_top,
                "created_time": created_time
            })
            # 如果非置顶，一天后就从缓存中清除
            if is_top == 0:
                con.expire(_id, 24*60*60)
        except Exception as e:
            print(e)
        finally:
            del con

    def delete(self, _id):
        """
        通过ID删除缓存的新闻
        :param _id: 新闻ID
        """
        try:
            con = redis.Redis(connection_pool=pool)
            con.delete(_id)
        except Exception as e:
            print(e)
        finally:
            del con