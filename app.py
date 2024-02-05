import os
import sys
import time
from colorama import Fore, Style
from getpass import getpass
from service.user_service import UserService
from service.news_service import NewsService
from service.role_service import RoleService
from service.type_service import TypeService


# 初始化服务（用户、角色、新闻和类型）
user_s = UserService()
news_s = NewsService()
role_s = RoleService()
type_s = TypeService()


def __init_welcome_page():
    """
    初始化欢迎界面
    """
    # 清空页面
    os.system("cls")
    print(Fore.LIGHTBLUE_EX, "\n\t====================")
    print(Fore.LIGHTBLUE_EX, "\n\t欢迎使用新闻管理系统")
    print(Fore.LIGHTBLUE_EX, "\n\t====================")
    print(Fore.LIGHTGREEN_EX, "\n\t1.登录系统")
    print(Fore.LIGHTGREEN_EX, "\n\t2.退出系统")
    # 重置字体
    print(Style.RESET_ALL)


def __init_manager_page():
    """
    初始化管理员管理界面
    """
    print(Fore.LIGHTGREEN_EX, "\n\t1.新闻管理")
    print(Fore.LIGHTGREEN_EX, "\n\t2.用户管理")
    print(Fore.LIGHTRED_EX, "\n\tback.退出登录")
    print(Fore.LIGHTRED_EX, "\n\texit.退出系统")
    print(Style.RESET_ALL)


def __init_news_manage_page():
    """
    初始化新闻管理界面
    """
    # 清空页面（为即将进入新页面作准备
    os.system("cls")
    print(Fore.LIGHTGREEN_EX, "\n\t1.审批新闻")
    print(Fore.LIGHTGREEN_EX, "\n\t2.删除新闻")
    print(Fore.LIGHTRED_EX, "\n\tback.返回上一层")
    print(Style.RESET_ALL)


def __init_review_news_page(page, lists, total_page):
    """
    初始化审批新闻一览界面
    :param page:
    :param lists:
    :param total_page:
    """
    os.system("cls")
    # 展示所有带审批新闻
    for index in range(len(lists)):
        news = lists[index]
        # 索引编号  标题  类型  作者
        print(Fore.LIGHTBLUE_EX, "\n\t%d\t%s\t%s\t%s" % (index + 1, news[1], news[2], news[3]))
    # 紧接着显示 当前页/总页数 信息
    print(Fore.LIGHTBLUE_EX, "\n\t------------------------------")
    print(Fore.LIGHTBLUE_EX, "\n\t%d/%d" % (page, total_page))
    print(Fore.LIGHTBLUE_EX, "\n\t------------------------------")
    # 显示命令区域
    print(Fore.LIGHTRED_EX, "\n\tback.返回上一层")
    print(Fore.LIGHTRED_EX, "\n\tprev.上一页")
    print(Fore.LIGHTRED_EX, "\n\tnext.下一页")
    print(Style.RESET_ALL)


def __init_common_news_job_page(opt3):
    """
    初始化新闻管理共通界面
    :param opt3: 审批 OR 删除
    """
    page = 1  # 初始页面设为第1页
    while True:
        # 获取待审批新闻的总页数
        total_page = news_s.search_unrevised_list_total_count() if opt3 == "1" else news_s.search_all_list_total_count()
        # 获取所有待审批新闻
        lists = news_s.search_unrevised_list(page) if opt3 == "1" else news_s.search_all_list(page)
        # 创建审批新闻一览界面
        __init_review_news_page(page, lists, total_page)
        opt4 = input("\n\t请输入操作编号: ")
        if opt4 == "back":
            # 直接结束当前循环，返回上层
            break
        elif opt4 == "prev":
            if page > 1:  # 上一页的前提得至少是第2页以后
                page -= 1
        elif opt4 == "next":
            if page < total_page:  # 下一页的前提得至少小于最后一页
                page += 1
        else:
            try:
                if 1 <= int(opt4) <= 10:
                    news_id = lists[int(opt4) - 1][0]
                    if opt3 == "1":
                        news_s.update_target_news(news_id, "待审批")
                        # 将审批成功的新闻缓存到Redis服务中
                        target = news_s.search_cache_target(news_id)
                        title = target[0]
                        username = target[1]
                        _type = target[2]
                        content_id = target[3]
                        # 从MongoDB查找新闻正文
                        content = news_s.search_content_by_id(content_id)
                        is_top = target[4]
                        created_time = str(target[5])
                        news_s.cache_target_news(news_id, title, username, _type, content, is_top, created_time)
                        print("\n\t审批成功（3秒后自动返回）")
                    else:
                        news_s.delete_by_id(news_id)
                        # 将Redis服务中的缓存数据删除
                        news_s.delete_cache(news_id)
                        print("\n\t删除成功（3秒后自动返回）")
                    time.sleep(3)
            except Exception as e:
                print("\n\t非法输入（3秒后自动返回）", e)
                time.sleep(3)

def __init_user_manage_page():
    """
    初始化用户管理界面
    """
    os.system("cls")
    print(Fore.LIGHTGREEN_EX, "\n\t1.添加用户")
    print(Fore.LIGHTGREEN_EX, "\n\t2.修改用户")
    print(Fore.LIGHTGREEN_EX, "\n\t3.删除用户")
    print(Fore.LIGHTRED_EX, "\n\tback.返回上一层")
    print(Style.RESET_ALL)


def __edit_user_info(opt3):
    """
    编辑用户信息
    :param opt3: 新规 OR 更新
    """
    os.system("cls")
    username = input("\n\t用户名: ") if opt3=="1" else input("\n\t新用户名: ")
    password = getpass("\n\t密码: ") if opt3=="1" else getpass("\n\t新密码: ")
    password_2 = getpass("\n\t重复密码: ") if opt3=="1" else getpass("\n\t再次输入密码: ")
    isError = False
    if password != password_2:
        isError = True
        return (isError, None, None, None, None)
    email = input("\n\t邮箱: ") if opt3=="1" else input("\n\t新邮箱: ")
    # 获取角色
    ret = role_s.search_all_list()
    for index in range(len(ret)):
        record = ret[index]
        # 索引编号.角色名称
        print(Fore.LIGHTBLUE_EX, "\n\t%d.%s" % (index + 1, record[1]))
    print(Style.RESET_ALL)
    opt = input("\n\t角色编号: ")
    role_id = ret[int(opt) - 1][0]

    return (isError, username, password, email, role_id)


def __init_common_user_job_page(opt3):
    """
    初始化用户管理共通界面
    :param opt3: 更新 OR 删除
    """
    page = 1  # 初始页面设为第1页
    while True:
        # 清空页面（为即将进入新页面作准备
        os.system("cls")
        # 获取用户的总页数
        total_page = user_s.search_total_count()
        # 获取所有用户信息
        lists = user_s.search_page_list(page)
        # 展示当页所有用户信息
        for index in range(len(lists)):
            user = lists[index]
            # 索引编号  标题  类型  作者
            print(Fore.LIGHTBLUE_EX, "\n\t%d\t%s\t%s" % (index + 1, user[1], user[2]))
            # 紧接着显示 当前页/总页数 信息
        print(Fore.LIGHTBLUE_EX, "\n\t------------------------------")
        print(Fore.LIGHTBLUE_EX, "\n\t%d/%d" % (page, total_page))
        print(Fore.LIGHTBLUE_EX, "\n\t------------------------------")

        # 显示命令区域
        print(Fore.LIGHTRED_EX, "\n\tback.返回上一层")
        print(Fore.LIGHTRED_EX, "\n\tprev.上一页")
        print(Fore.LIGHTRED_EX, "\n\tnext.下一页")

        print(Style.RESET_ALL)
        opt4 = input("\n\t请输入操作编号: ")
        if opt4 == "back":
            # 直接结束当前循环，返回上层
            break
        elif opt4 == "prev" and page > 1:  # 上一页的前提得至少是第2页以后
            page -= 1
        elif opt4 == "next" and page < total_page:  # 下一页的前提得至少小于最后一页
            page += 1
        else:
            try:
                if 1 <= int(opt4) <= 10:
                    user_id = lists[int(opt4) - 1][0]
                    if opt3 == "2":
                        # 编辑用户情报
                        isError, username, password, email, role_id = __edit_user_info(opt3)
                        if isError:
                            print("\n\t两次密码不一致（3秒后自动返回）")
                            time.sleep(3)
                            break
                        opt5 = input("\n\t是否保存（Y/N）")
                        if opt5 == "Y" or opt5 == "y":
                            user_s.update(user_id, username, password, email, role_id)
                            print("\n\t保存成功（3秒后自动返回）")
                            time.sleep(3)
                    else:
                        user_s.delete_by_id(user_id)
                        print("\n\t删除成功（3秒后自动返回）")
                        time.sleep(3)
            except Exception as e:
                print("\n\t非法输入（3秒后自动返回）", e)
                time.sleep(3)


if __name__ == "__main__":
    while True:
        # 创建欢迎界面
        __init_welcome_page()
        opt1 = input("\n\t请输入操作编号: ")
        if opt1 == "1":  # 选择【登录系统】的场合
            username = input("\n\t用户名: ")
            password = getpass("\n\t密码: ")
            has_permission = user_s.login(username, password)
            if has_permission: # 登录成功的场合，需要判断用户的角色来进行后续相应的处理
                # 查询角色
                u_role = user_s.search_user_role(username)
                while True:
                    # 清空页面（为即将进入新页面作准备
                    os.system("cls")
                    if u_role == "新闻编辑":
                        print(Fore.LIGHTGREEN_EX, "\n\t1.发表新闻")
                        print(Fore.LIGHTGREEN_EX, "\n\t2.编辑新闻")
                        print(Fore.LIGHTRED_EX, "\n\tback.退出登录")
                        print(Fore.LIGHTRED_EX, "\n\texit.退出系统")
                        print(Style.RESET_ALL)
                        opt2 = input("\n\t请输入操作编号: ")
                        if opt2 == "1":
                            os.system("cls")
                            title = input("\n\t新闻标题: ")
                            user_id = user_s.search_user_id(username)
                            types = type_s.search_all_list()
                            for index in range(len(types)):
                                record = types[index]
                                print(Fore.LIGHTBLUE_EX, "\n\t%d.%s" % (index+1, record[1]))
                            print(Style.RESET_ALL)
                            opt = input("\n\t请输入操作编号: ")
                            type_id = types[int(opt)-1][0]
                            # 新闻正文内容
                            news_path = input("\n\t输入文件路径: ")
                            news_file = open(news_path, "rb")
                            content = news_file.read()
                            news_file.close()
                            is_top = input("\n\t置顶级别（0-5）: ")
                            is_commit = input("\n\t是否提交（Y/N）: ")
                            if is_commit == "Y" or is_commit == "y":
                                news_s.insert(title, user_id, type_id, content, is_top)
                                print("\n\t提交成功（3秒后自动返回）")
                                time.sleep(3)
                        elif opt2 == "2":
                            page = 1  # 初始页面设为第1页
                            while True:
                                os.system("cls")
                                # 获取新闻的总页数
                                total_page = news_s.search_all_list_total_count()
                                # 获取当前页面的所有新闻数据
                                news = news_s.search_all_list(page)
                                # 展示当页所有新闻信息
                                for index in range(len(news)):
                                    record = news[index]
                                    # 索引编号  标题  类型  作者
                                    print(Fore.LIGHTBLUE_EX, "\n\t%d\t%s\t%s" % (index + 1, record[1], record[2]))
                                    # 紧接着显示 当前页/总页数 信息
                                print(Fore.LIGHTBLUE_EX, "\n\t------------------------------")
                                print(Fore.LIGHTBLUE_EX, "\n\t%d/%d" % (page, total_page))
                                print(Fore.LIGHTBLUE_EX, "\n\t------------------------------")

                                # 显示命令区域
                                print(Fore.LIGHTRED_EX, "\n\tback.返回上一层")
                                print(Fore.LIGHTRED_EX, "\n\tprev.上一页")
                                print(Fore.LIGHTRED_EX, "\n\tnext.下一页")

                                print(Style.RESET_ALL)
                                opt3 = input("\n\t请输入操作编号: ")
                                if opt3 == "back":
                                    break
                                elif opt3 == "prev":
                                    if page > 1:    # 上一页的前提得至少是第2页以后
                                        page -= 1
                                elif opt3 == "next":
                                    if page < total_page:   # 下一页的前提得至少小于最后一页
                                        page += 1
                                else:
                                    try:
                                        if 1 <= int(opt3) <= 10:
                                            os.system("cls")
                                            news_id = news[int(opt3)-1][0]
                                            news_info = news_s.search_by_id(news_id)
                                            title = news_info[0]
                                            _type = news_info[1]
                                            is_top = news_info[2]
                                            print("\n\t新闻原标题: %s" % title)
                                            new_title = input("\n\t新标题: ")

                                            print("\n\t原类型: %s" % _type)
                                            types = type_s.search_all_list()
                                            for index in range(len(types)):
                                                record = types[index]
                                                print(Fore.LIGHTBLUE_EX, "\n\t%d.%s" % (index + 1, record[1]))
                                            print(Style.RESET_ALL)
                                            opt4 = input("\n\t类型编号: ")
                                            type_id = types[int(opt4)-1][0]
                                            # 输入新闻内容
                                            news_path = input("\n\t输入文件路径: ")
                                            news_file = open(news_path, "rb")
                                            content = news_file.read()
                                            news_file.close()
                                            print("\n\t原置顶级别: %s" % is_top)
                                            new_is_top = input("\n\t置顶级别（0-5）: ")
                                            is_commit = input("\n\t是否提交（Y/N）: ")
                                            if is_commit == "Y" or is_commit == "y":
                                                news_s.update(news_id, new_title, type_id, content, is_top)
                                                print("\n\t更新成功（3秒后自动返回）")
                                                time.sleep(3)
                                    except Exception as e:
                                        print("\n\t非法输入（3秒后自动返回）", e)
                                        time.sleep(3)
                        elif opt2 == "back":
                            break
                        elif opt2 == "exit":
                            sys.exit(0)
                    elif u_role == "管理员":
                        # 创建管理员页面
                        __init_manager_page()
                        opt2 = input("\n\t请输入操作编号: ")
                        if opt2 == "1":  # 选择【新闻管理】的场合
                            while True:
                                # 创建新闻管理界面
                                __init_news_manage_page()
                                opt3 = input("\n\t请输入操作编号: ")
                                if opt3 in ["1", "2"]:  # 选择【审批或者删除新闻】的场合
                                    __init_common_news_job_page(opt3)
                                elif opt3 == "back":    # 选择【返回上一层】的场合
                                    break   # 直接结束当前循环，返回上层
                        elif opt2 == "2":   # 选择【用户管理】的场合
                            while True:
                                # 创建用户管理界面
                                __init_user_manage_page()
                                opt3 = input("\n\t请输入操作编号: ")
                                if opt3 == "1":   # 选择【添加用户】的场合
                                    # 编辑用户情报
                                    isError, username, password, email, role_id = __edit_user_info(opt3)
                                    if isError:
                                        print("\n\t两次密码不一致（3秒后自动返回）")
                                        time.sleep(3)
                                        continue
                                    user_s.insert(username, password, email, role_id)
                                    print("\n\t保存成功（3秒后自动返回）")
                                    time.sleep(3)
                                elif opt3 in ["2", "3"]:    # 选择【修改或者删除用户】的场合
                                    __init_common_user_job_page(opt3)
                                elif opt3 == "back":
                                    break
                        elif opt2 == "back":
                            # 直接结束当前循环，返回上层
                            break
                        elif opt2 == "exit":
                            sys.exit(0)
            else:
                print("\n\t登录失败（3秒后自动返回）")
                time.sleep(3)
        elif opt1 == "2":
            sys.exit(0)
        else:
            print("\n\t非法输入！请重新选择！！")
            time.sleep(1)
