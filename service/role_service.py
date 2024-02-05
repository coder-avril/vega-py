from db.role_dao import RoleDao

class RoleService:
    __role_dao = RoleDao()

    def search_all_list(self):
        return self.__role_dao.search_all_list()
