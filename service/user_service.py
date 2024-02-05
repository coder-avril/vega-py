from db.user_dao import UserDao

class UserService:
    __user_dao = UserDao()

    def login(self, username, password):
        return self.__user_dao.login(username, password)

    def search_user_role(self, username):
        return self.__user_dao.search_user_role(username)

    def insert(self, username, password, email, role_id):
        self.__user_dao.insert(username, password, email, role_id)

    def search_page_list(self, page):
        return self.__user_dao.search_page_list(page)

    def search_total_count(self):
        return self.__user_dao.search_total_count()

    def update(self, _id, username, password, email, role_id):
        self.__user_dao.update(_id, username, password, email, role_id)

    def delete_by_id(self, _id):
        self.__user_dao.delete_by_id(_id)

    def search_user_id(self, username):
        """查找用户名对应的用户ID"""
        return self.__user_dao.search_user_id(username)
