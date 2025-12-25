import mysql.connector
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 建立与数据库的连接
def connect_to_database():
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port=int(os.getenv("DB_PORT", "3306")),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", "root"),
            database=os.getenv("DB_NAME", "chefdishmanagement")
        )
        print("成功连接到数据库")
        return conn
    except mysql.connector.Error as error:
        print("连接数据库失败：{}".format(error))
        return None

# 厨师登录
def chef_login(conn):
    chef_id = input("请输入厨师ID: ")
    password = input("请输入密码: ")

    query = "SELECT * FROM Chef WHERE ChefID = %s AND Password = %s"
    values = (chef_id, password)

    cursor = conn.cursor()
    cursor.execute(query, values)
    result = cursor.fetchone()

    if result:
        print("登录成功！欢迎，{}".format(result[1]))
        return result[0]  # 返回厨师ID
    else:
        print("登录失败，请检查输入的厨师ID和密码。")
        return None

# 查看菜品
def view_dishes(conn, chef_id):
    query = "SELECT * FROM Dish WHERE ChefID = %s"
    values = (chef_id,)

    cursor = conn.cursor()
    cursor.execute(query, values)
    dishes = cursor.fetchall()

    if dishes:
        print("菜品列表：")
        for dish in dishes:
            print("ID: {}, 名称: {}, 描述: {}".format(dish[0], dish[1], dish[3]))
    else:
        print("没有找到相关菜品。")



def add_dish(conn, chef_id):
    # 自动获取下一个可用的菜品ID
    cursor = conn.cursor()
    cursor.execute("SELECT COALESCE(MAX(DishID), 0) + 1 FROM Dish")
    dish_id = cursor.fetchone()[0]
    
    dish_name = input("请输入菜品名称: ")
    dish_description = input("请输入菜品描述: ")

    query = "INSERT INTO Dish (DishID, Name, ChefID, Description) VALUES (%s, %s, %s, %s)"
    values = (dish_id, dish_name, chef_id, dish_description)

    try:
        cursor.execute(query, values)
        conn.commit()
        print("菜品添加成功！菜品ID: {}".format(dish_id))
    except mysql.connector.Error as err:
        print("菜品添加失败: {}".format(err))



# 修改菜品
def edit_dish(conn, chef_id):
    dish_id = input("请输入要修改的菜品ID: ")
    new_description = input("请输入新的菜品描述: ")

    query = "UPDATE Dish SET Description = %s WHERE DishID = %s AND ChefID = %s"
    values = (new_description, dish_id, chef_id)

    cursor = conn.cursor()
    cursor.execute(query, values)
    if cursor.rowcount > 0:
        conn.commit()
        print("菜品已成功修改！")
    else:
        print("修改菜品失败，请检查菜品ID和权限。")

# 添加厨师账号
def add_chef_account(conn):
    # 自动获取下一个可用的厨师ID
    cursor = conn.cursor()
    cursor.execute("SELECT COALESCE(MAX(ChefID), 0) + 1 FROM Chef")
    chef_id = cursor.fetchone()[0]
    
    name = input("请输入厨师姓名: ")
    specialty = input("请输入厨师特长: ")
    password = input("请输入密码: ")

    query = "INSERT INTO Chef (ChefID, Name, Specialty, Password) VALUES (%s, %s, %s, %s)"
    values = (chef_id, name, specialty, password)

    try:
        cursor.execute(query, values)
        conn.commit()
        print("厨师账号已成功添加！厨师ID: {}".format(chef_id))
    except mysql.connector.Error as err:
        print("厨师账号添加失败: {}".format(err))

# 删除厨师账号
def delete_chef_account(conn):
    chef_id = input("请输入要删除的厨师ID: ")

    query = "DELETE FROM Chef WHERE ChefID = %s"
    values = (chef_id,)

    cursor = conn.cursor()
    cursor.execute(query, values)
    if cursor.rowcount > 0:
        conn.commit()
        print("厨师账号已成功删除！")
    else:
        print("删除厨师账号失败，请检查厨师ID。")

# 添加菜品信息
def add_dish_info(conn):
    # 自动获取下一个可用的菜品ID
    cursor = conn.cursor()
    cursor.execute("SELECT COALESCE(MAX(DishID), 0) + 1 FROM Dish")
    dish_id = cursor.fetchone()[0]
    
    name = input("请输入菜品名称: ")
    chef_id = input("请输入所属厨师ID: ")
    description = input("请输入菜品描述: ")

    query = "INSERT INTO Dish (DishID, Name, ChefID, Description) VALUES (%s, %s, %s, %s)"
    values = (dish_id, name, chef_id, description)

    try:
        cursor.execute(query, values)
        conn.commit()
        print("菜品信息已成功添加！菜品ID: {}".format(dish_id))
    except mysql.connector.Error as err:
        print("菜品信息添加失败: {}".format(err))



# 删除菜品信息
def delete_dish_info(conn):
    dish_id = input("请输入要删除的菜品ID: ")

    query = "DELETE FROM Dish WHERE DishID = %s"
    values = (dish_id,)

    cursor = conn.cursor()
    cursor.execute(query, values)
    if cursor.rowcount > 0:
        conn.commit()
        print("菜品信息已成功删除！")
    else:
        print("删除菜品信息失败，请检查菜品ID。")

# 主函数
def main():
    conn = connect_to_database()
    if conn is None:
        return

    user_type = input("请选择用户类型（1.厨师 2.管理员）: ")

    if user_type == "1":  # 厨师
        chef_id = chef_login(conn)
        if chef_id is None:
            return

        while True:
            print("\n功能选项：")
            print("1.查看菜品")
            print("2.添加菜品")
            print("3.修改菜品")
            print("0.退出")
            choice = input("请选择要执行的操作：")

            if choice == "1":
                view_dishes(conn, chef_id)
            elif choice == "2":
                add_dish(conn, chef_id)
            elif choice == "3":
                edit_dish(conn, chef_id)
            elif choice == "0":
                break
            else:
                print("无效的选项，请重新输入。")

    elif user_type == "2":  # 管理员
        admin_id = input("请输入管理员ID: ")
        password = input("请输入密码: ")

        query = "SELECT * FROM Admin WHERE AdminID = %s AND Password = %s"
        values = (admin_id, password)

        cursor = conn.cursor()
        cursor.execute(query, values)
        result = cursor.fetchone()

        if result:
            print("登录成功！欢迎，{}".format(result[1]))
            while True:
                print("\n功能选项：")
                print("1.管理厨师账号")
                print("2.管理菜品信息")
                print("0.退出")
                choice = input("请选择要执行的操作：")

                if choice == "1":
                    print("\n厨师账号管理选项：")
                    print("1.添加厨师账号")
                    print("2.删除厨师账号")
                    account_choice = input("请选择要执行的操作：")

                    if account_choice == "1":
                        add_chef_account(conn)
                    elif account_choice == "2":
                        delete_chef_account(conn)
                    elif account_choice == "0":
                        break
                    else:
                        print("无效的选项，请重新输入。")

                elif choice == "2":
                    print("\n菜品信息管理选项：")
                    print("1.添加菜品信息")
                    print("2.删除菜品信息")
                    dish_choice = input("请选择要执行的操作：")

                    if dish_choice == "1":
                        add_dish_info(conn)
                    elif dish_choice == "2":
                        delete_dish_info(conn)
                    elif dish_choice == "0":
                        break
                    else:
                        print("无效的选项，请重新输入。")

                elif choice == "0":
                    break
                else:
                    print("无效的选项，请重新输入。")
        else:
            print("登录失败，请检查管理员ID和密码。")

    conn.close()

# 调用主函数
if __name__ == '__main__':
    main()
