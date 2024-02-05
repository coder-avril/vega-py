from db.mysql_db import pool

class UserDao:
    def login(self, username, password):
        """
        用户的认证登录
        :param username: 用户名
        :param password: 密码
        :return: 登录成功与否的结果
        """
        con = None
        try:
            con = pool.get_connection()
            cursor = con.cursor()
            sql = "SELECT COUNT(*) FROM t_user WHERE username=%s AND " \
                  "AES_DECRYPT(UNHEX(password), 'HelloWorld')=%s"
            cursor.execute(sql, (username, password))
            count = cursor.fetchone()[0]
            # 如果能够匹配到1条则表面存在，认证OK
            return True if count == 1 else False
        except Exception as e:
            print(e)
        finally:
            if "con" in dir():
                con.close()

    def search_user_role(self, username):
        """
        查询用户的角色
        :param username: 用户名
        :return: 角色
        """
        con = None
        try:
            con = pool.get_connection()
            cursor = con.cursor()
            sql = "SELECT r.role FROM t_user u INNER JOIN t_role r ON u.role_id=r.id WHERE " \
                  "u.username=%s"
            cursor.execute(sql, (username, ))
            ret = cursor.fetchone()
            return ret[0] if ret is not None else None
        except Exception as e:
            print(e)
        finally:
            if "con" in dir():
                con.close()

    def insert(self, username, password, email, role_id):
        """
        添加用户记录
        :param username: 用户名
        :param password: 密码
        :param email: 邮件
        :param role_id: 角色ID
        """
        con = None
        try:
            con = pool.get_connection()
            con.start_transaction()
            cursor = con.cursor()
            sql = "INSERT INTO t_user(username, password, email, role_id) " \
                  "VALUES (%s, HEX(AES_ENCRYPT(%s, 'HelloWorld')), %s, %s)"
            cursor.execute(sql, (username, password, email, role_id))
            con.commit()
        except Exception as e:
            if "con" in dir():
                con.rollback()
            print(e)
        finally:
            if "con" in dir():
                con.close()

    def search_page_list(self, page):
        """
        查询用户分页记录
        :param page: 第几页
        :return: 指定页面的所有数据
        """
        con = None
        try:
            con = pool.get_connection()
            cursor = con.cursor()
            sql = "SELECT u.id, u.username, r.role FROM t_user u " \
                  "INNER JOIN t_role r ON u.role_id=r.id " \
                  "ORDER BY u.id LIMIT %s,%s"
            cursor.execute(sql, ((page - 1) * 10, 10))
            return cursor.fetchall()
        except Exception as e:
            print(e)
        finally:
            if "con" in dir():
                con.close()

    def search_total_count(self):
        """
        查询用户数据的总页数
        :return: 总页数
        """
        con = None
        try:
            con = pool.get_connection()
            cursor = con.cursor()
            sql = "SELECT CEIL(COUNT(*)/10) FROM t_user"
            cursor.execute(sql)
            return cursor.fetchone()[0]
        except Exception as e:
            print(e)
        finally:
            if "con" in dir():
                con.close()

    def update(self, _id, username, password, email, role_id):
        """
        修改用户信息
        :param _id: 用户ID
        :param username: 用户名
        :param password: 密码
        :param email: 邮件
        :param role_id: 角色ID
        """
        con = None
        try:
            con = pool.get_connection()
            con.start_transaction()
            cursor = con.cursor()
            sql = "UPDATE t_user " \
                  "SET username=%s, password=HEX(AES_ENCRYPT(%s, 'HelloWord')), email=%s, role_id=%s " \
                  "WHERE id=%s"
            cursor.execute(sql, (username, password, email, role_id, _id))
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
        删除指定ID的用户
        :param _id: 用户ID
        """
        con = None
        try:
            con = pool.get_connection()
            # 手动开启事务
            con.start_transaction()
            cursor = con.cursor()
            sql = "DELETE FROM t_user WHERE id=%s"
            cursor.execute(sql, [_id])
            con.commit()
        except Exception as e:
            if "con" in dir():
                con.rollback()
            print(e)
        finally:
            if "con" in dir():
                con.close()

    def search_user_id(self, username):
        """
        查找用户名对应的用户ID
        :param username: 用户名
        :return: 用户ID
        """
        con = None
        try:
            con = pool.get_connection()
            cursor = con.cursor()
            sql = "SELECT id FROM t_user WHERE username=%s"
            cursor.execute(sql, [username])
            return cursor.fetchone()[0]
        except Exception as e:
            print(e)
        finally:
            if "con" in dir():
                con.close()
