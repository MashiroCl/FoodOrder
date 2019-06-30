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


###############################################################################
'''
插入与更新操作请根据以下
两个函数的方式进行操作
（就是换下名字和参数就完事儿了 :D ）
'''
def InsertAdmin(adminID,pwd,aname,adtel):
    conn=sqlite3.connect("user.db")
    c=conn.cursor()
    sql='''insert into ADMIN(adminID,pwd,aname,adtel)
            VALUES (?,?,?,?)'''
    para=(adminID,pwd,aname,adtel)
    c.execute(sql,para)
    conn.commit()
    conn.close()

def UpdateAdmin(adminID,pwd):
    conn = sqlite3.connect("user.db")
    c = conn.cursor()
    cursor=c.execute("update ADMIN set pwd='%s' where adminID='%s'"%(pwd,adminID))
    conn.commit()
    conn.close()

'''
每个表都要有插入操作
update要求:
comment表:根据mealID更新evaluate与grade
Menu表：根据mealID更改grade
OrderList:更具orderID更改state
Store:根据StoreId更改number
'''
#################################################################################
'''此处填写代码'''

################################################################################

if __name__=="__main__":
    # init_DB()
    ShowAdmin()
    # ShowComment()
