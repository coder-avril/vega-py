from db.mysql_db import pool

class RoleDao:
    def search_all_list(self):
        """
        查询角色列表
        :return: 角色列表
        """
        con = None
        try:
            con = pool.get_connection()
            cursor = con.cursor()
            sql = "SELECT id, role FROM t_role"
            cursor.execute(sql)
            return cursor.fetchall()
        except Exception as e:
            print(e)
        finally:
            if "con" in dir():
                con.close()
