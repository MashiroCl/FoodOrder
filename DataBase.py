import sqlite3
def init_DB():
    conn=sqlite3.connect("DataBase.db")
    c=conn.cursor()
    c.execute('''
    CREATE TABLE ADMIN
    (adminID number unique,
    pwd varchar(20) not null,
    aname varchar(20) not null,
    adtel varchar(20) not null)
    ''')
    conn.commit()
    conn.close()

    conn=sqlite3.connect("DataBase.db")
    c=conn.cursor()
    c.execute('''
    CREATE TABLE comment
    (orderID number unique,
    mealID number not null,
    evaluate varchar,
    grade number)
    ''')
    conn.commit()
    conn.close()

    conn = sqlite3.connect("DataBase.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE Emp
        (empID number unique,
        ename varchar,
        etel varchar,
        password varchar not null)
        ''')
    conn.commit()
    conn.close()

    conn = sqlite3.connect("DataBase.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE Menu
        (mealID number unique,
        mname varchar not null,
        empID number,
        price number,
        pircture varchar,
        grade number,
        element number not null)
        ''')
    conn.commit()
    conn.close()

    conn = sqlite3.connect("DataBase.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE OrderList
        (orderID number unique,
        takeID varchar,
        mealID varchar,
        userID number not null,
        state varchar)
        ''')
    conn.commit()
    conn.close()

    conn = sqlite3.connect("DataBase.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE Store
        (StoreID number unique,
        sname varchar,
        number number)
        ''')
    conn.commit()
    conn.close()

    conn = sqlite3.connect("DataBase.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE User
        (userID number unique,
        uname varchar,
        tel varchar,
        password varchar not null)
        ''')
    conn.commit()
    conn.close()
def ShowAdmin():
    conn = sqlite3.connect('DataBase.db')
    c = conn.cursor()
    sql="select name from sqlite_master where type='table' order by name"
    cursor=c.execute(sql)
    for row in c:
        print(row)
    conn.close()

def ShowComment():
    conn = sqlite3.connect('DataBase.db')
    c = conn.cursor()
    cursor=c.execute(''' select * from comment''')
    for row in c:
        print(row)
    conn.close()


#
# 初始化表
#插入新的数据
#更新表

if __name__=="__main__":
    # init_DB()
    ShowAdmin()
    # ShowComment()

# '''
# import sqlite3
# from FastFoodShop import customer
# def init_DB_user():
#     conn = sqlite3.connect('user.db')
#     c = conn.cursor()
#     c.execute('''CREATE TABLE USER
#            (username nchar NOT NULL,
#            password  varchar NOT NULL,
#            phone   number not null);''')
#     conn.commit()
#     conn.close()
# def init_DB_OrderList():
#     '''存储数据为json'''
#     conn = sqlite3.connect('orderList.db')
#     c = conn.cursor()
#
#     c.execute('''CREATE TABLE orderList
#            (orderList varchar NOT NULL,
#            phone varchar NOT NULL);''')
#
#     conn.commit()
#     conn.close()
#
# def insert_user(username1,password1,phone1):
#     conn = sqlite3.connect('user.db')
#     c = conn.cursor()
#     sql='''insert into USER(username,password,phone)
#                 VALUES (?,?,?)'''
#     para=(username1,password1,phone1)
#     c.execute(sql,para)
#     conn.commit()
#     conn.close()
#
# def insert_orderList(data,phone):
#     conn = sqlite3.connect('orderList.db')
#     c = conn.cursor()
#     sql='''insert into orderList(orderList,phone)
#                 VALUES (?,?)'''
#     para=(data,phone)
#     c.execute(sql,para)
#     conn.commit()
#     conn.close()
#
#
# def show_user():
#     conn = sqlite3.connect('user.db')
#     c = conn.cursor()
#     cursor=c.execute(''' select * from USER''')
#     for row in c:
#         print(row)
#     conn.close()
#
# def show_orderList():
#     conn = sqlite3.connect('orderList.db')
#     c = conn.cursor()
#     cursor=c.execute(''' select * from orderList''')
#     temp=[]
#     for row in c:
#         temp.append(row)
#         # print(row)
#     conn.close()
#     return temp
#
#
# if  __name__=="__main__":
#     # init_DB_user()
#     # insert_user('ADMIN','ADMIN','11111111111')
#     # show_user()
#
#     init_DB_OrderList()
#     # insert_orderList("MashiroCl","1111111111")
#
#     temp=show_orderList()
#     print(temp)
#     print(len(temp))
#
# '''