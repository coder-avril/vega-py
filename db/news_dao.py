from db.mysql_db import pool


class NewsDao:
    def search_unrevised_list(self, page):
        """
        查询待审批的分页新闻数据
        :param page: 指定页面
        :return: 检索到的新闻数据
        """
        con = None
        try:
            con = pool.get_connection()
            cursor = con.cursor()
            sql = "SELECT n.id, n.title, t.type, u.username FROM t_news n INNER JOIN t_type t " \
                  "ON n.type_id=t.id INNER JOIN t_user u " \
                  "ON n.editor_id=u.id WHERE n.state='待审批' ORDER BY n.created_time " \
                  "DESC LIMIT %s,%s"
            cursor.execute(sql, ((page-1)*10, 10))
            return cursor.fetchall()
        except Exception as e:
            print(e)
        finally:
            if "con" in dir():
                con.close()

    def search_unrevised_list_total_count(self):
        """
        查询待审批的新闻数据的总页数
        :return: 总页数
        """
        con = None
        try:
            con = pool.get_connection()
            cursor = con.cursor()
            sql = "SELECT CEIL(COUNT(*)/10) FROM t_news WHERE state='待审批'"
            cursor.execute(sql)
            return cursor.fetchone()[0]
        except Exception as e:
            print(e)
        finally:
            if "con" in dir():
                con.close()

    def search_all_list(self, page):
        """
        查询当前页面的所有新闻数据
        :param page: 指定页面
        :return: 检索到的新闻
        """
        con = None
        try:
            con = pool.get_connection()
            cursor = con.cursor()

            sql = "SELECT n.id, n.title, t.type, u.username FROM t_news n INNER JOIN t_type t " \
                  "ON n.type_id=t.id INNER JOIN t_user u " \
                  "ON n.editor_id=u.id ORDER BY n.created_time " \
                  "DESC LIMIT %s,%s"

            cursor.execute(sql, ((page-1)*10, 10))
            return cursor.fetchall()
        except Exception as e:
            print(e)
        finally:
            if "con" in dir():
                con.close()

    def search_all_list_total_count(self):
        """
        查询所有新闻数据的总页数
        :return: 总页数
        """
        con = None
        try:
            con = pool.get_connection()
            cursor = con.cursor()
            sql = "SELECT CEIL(COUNT(*)/10) FROM t_news"
            cursor.execute(sql)
            return cursor.fetchone()[0]
        except Exception as e:
            print(e)
        finally:
            if "con" in dir():
                con.close()

    def update_target_news(self, _id, target):
        """
        更新对象状态的指定id的新闻数据为【已审批】
        :param _id: 新闻数据的id
        :param target: 状态（"待审批"等等
        """
        con = None
        try:
            con = pool.get_connection()
            # 手动开启事务
            con.start_transaction()
            cursor = con.cursor()
            sql = "UPDATE t_news SET state=%s WHERE id=%s AND state=%s"
            cursor.execute(sql, ("已审批", _id, target))
            con.commit()
        except Exception as e:
            if "con" in dir():
                con.rollback()
            print(e)
        finally:
            if "con" in dir():
                con.close()

    def delete_by_id(self, _id):
        """
        删除指定id的新闻数据
        :param _id: 新闻数据的id
        """
        con = None
        try:
            con = pool.get_connection()
            # 手动开启事务
            con.start_transaction()
            cursor = con.cursor()
            sql = "DELETE FROM t_news WHERE id=%s"
            cursor.execute(sql, [_id])
            con.commit()
        except Exception as e:
            if "con" in dir():
                con.rollback()
            print(e)
        finally:
            if "con" in dir():
                con.close()

    def insert(self, title, editor_id, type_id, content_id, is_top):
        """
        添加新闻
        :param title: 新闻标题
        :param editor_id: 编辑ID
        :param type_id: 类型ID
        :param content_id: 内容ID
        :param is_top: 是否置顶
        """
        con = None
        try:
            con = pool.get_connection()
            con.start_transaction()
            cursor = con.cursor()
            sql = "INSERT INTO t_news(title, editor_id, type_id, content_id, is_top, state) " \
                  "VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (title, editor_id, type_id, content_id, is_top, "待审批"))
            con.commit()
        except Exception as e:
            if "con" in dir():
                con.rollback()
            print(e)
        finally:
            if "con" in dir():
                con.close()

    def search_cache_target(self, _id):
        """
        查找需要缓存的新闻记录
        :param _id:
        :return: 对象新闻数据
        """
        con = None
        try:
            con = pool.get_connection()
            cursor = con.cursor()
            sql = "SELECT n.title, u.username, t.type, n.content_id, n.is_top, n.created_time " \
                  "FROM t_news n " \
                  "JOIN t_type t ON n.type_id=t.id " \
                  "JOIN t_user u ON n.editor_id=u.id WHERE n.id=%s"
            cursor.execute(sql, [_id])
            return cursor.fetchone()
        except Exception as e:
            print(e)
        finally:
            if "con" in dir():
                con.close()

    def search_by_id(self, _id):
        """
        根据ID查找新闻
        :param _id: 新闻ID
        :return: 新闻记录
        """
        con = None
        try:
            con = pool.get_connection()
            cursor = con.cursor()
            sql = "SELECT n.title, t.type, n.is_top " \
                  "FROM t_news n JOIN t_type t ON n.type_id=t.id WHERE n.id=%s"
            cursor.execute(sql, [_id])
            return cursor.fetchone()
        except Exception as e:
            print(e)
        finally:
            if "con" in dir():
                con.close()

    def update(self, _id, title, type_id, content_id, is_top):
        """
        更改新闻内容
        :param _id: 新闻ID
        :param title: 新闻标题
        :param type_id: 类型ID
        :param content_id: 新闻内容ID
        :param is_top: 是否置顶
        """
        con = None
        try:
            con = pool.get_connection()
            con.start_transaction()
            cursor = con.cursor()
            sql = "UPDATE t_news " \
                  "SET title=%s, type_id=%s, content_id=%s, is_top=%s, state=%s, update_time=NOW() " \
                  "WHERE id=%s"
            cursor.execute(sql, (title, type_id, content_id, is_top, "待审批", _id))
            con.commit()
        except Exception as e:
            if "con" in dir():
                con.rollback()
            print(e)
        finally:
            if "con" in dir():
                con.close()

    def search_content_id(self, _id):
        """
        查询内容ID
        :param _id: 新闻ID
        :return: 内容ID
        """
        con = None
        try:
            con = pool.get_connection()
            cursor = con.cursor()
            sql = "SELECT content_id FROM t_news WHERE id=%s"
            cursor.execute(sql, (_id, ))
            return cursor.fetchone()[0]
        except Exception as e:
            print(e)
        finally:
            if "con" in dir():
                con.close()
