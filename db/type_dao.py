from db.mysql_db import pool


class TypeDao:
    def search_list(self):
        """
        查询新闻类型的列表
        :return:
        """
        con = None
        try:
            con = pool.get_connection()
            cursor = con.cursor()
            sql = "SELECT id, type FROM t_type ORDER BY id"
            cursor.execute(sql)
            ret = cursor.fetchall()
            return ret
        except Exception as e:
            print(e)
        finally:
            if "con" in dir():
                con.close()
