from db.type_dao import TypeDao


class TypeService:
    __type_dao = TypeDao()

    def search_all_list(self):
        """查询新闻类型的列表"""
        return self.__type_dao.search_list()
