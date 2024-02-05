from db.news_dao import NewsDao
from db.redis_news_dao import RedisNewsDao
from db.mongo_news_dao import MongoNewsDao


class NewsService:
    __news_dao = NewsDao()
    __redis_news_dao = RedisNewsDao()
    __mongo_news_dao = MongoNewsDao()

    def search_unrevised_list(self, page):
        return self.__news_dao.search_unrevised_list(page)

    def search_unrevised_list_total_count(self):
        return self.__news_dao.search_unrevised_list_total_count()

    def search_all_list(self, page):
        return self.__news_dao.search_all_list(page)

    def search_all_list_total_count(self):
        return self.__news_dao.search_all_list_total_count()

    def update_target_news(self, _id, target):
        return self.__news_dao.update_target_news(_id, target)

    def delete_by_id(self, _id):
        content_id = self.__news_dao.search_content_id(_id)
        self.__news_dao.delete_by_id(_id)
        self.__mongo_news_dao.delete_by_id(content_id)

    def insert(self, title, editor_id, type_id, content, is_top):
        """添加新闻（增加新闻正文的存储"""
        self.__mongo_news_dao.insert(title, content)
        content_id = self.__mongo_news_dao.search_id(title)
        self.__news_dao.insert(title, editor_id, type_id, content_id, is_top)

    def search_cache_target(self, _id):
        """查找需要缓存的新闻记录"""
        return self.__news_dao.search_cache_target(_id)

    def cache_target_news(self, _id, title, username, _type, content, is_top, created_time):
        """向Redis中保存审核过的新闻"""
        self.__redis_news_dao.insert(_id, title, username, _type, content, is_top, created_time)

    def delete_cache(self, _id):
        """删除缓存的新闻"""
        self.__redis_news_dao.delete(_id)

    def search_by_id(self, _id):
        """根据ID查找新闻"""
        return self.__news_dao.search_by_id(_id)

    def update(self, _id, title, type_id, content, is_top):
        """更改新闻内容"""
        content_id = self.__news_dao.search_content_id(_id)
        self.__mongo_news_dao.update(content_id, title, content)
        self.__news_dao.update(_id, title, type_id, content_id, is_top)
        # 内容既然被更改，需要从Redis缓存中移除
        self.delete_cache(_id)

    def search_content_by_id(self, _id):
        return self.__mongo_news_dao.search_content_by_id(_id)
