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
        picture varchar,
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
        (storeID number unique,
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
每个表都要有插入操作
update要求:
comment表:根据mealID更新evaluate与grade
Menu表：根据mealID更改grade
OrderList:更具orderID更改state
Store:根据storeID更改number
'''
##############################################################################
def InsertAdmin(adminID,pwd,aname,adtel):
    conn=sqlite3.connect("DataBase.db")
    c=conn.cursor()
    sql='''insert into ADMIN(adminID,pwd,aname,adtel)
            VALUES (?,?,?,?)'''
    para=(adminID,pwd,aname,adtel)
    c.execute(sql,para)
    conn.commit()
    conn.close()

def Insertcomment(orderID,mealID,evaluate,grade):
    conn=sqlite3.connect("DataBase.db")
    c=conn.cursor()
    sql='''insert into comment(orderID,mealID,evaluate,grade)
            VALUES (?,?,?,?)'''
    para=(orderID,mealID,evaluate,grade)
    c.execute(sql,para)
    conn.commit()
    conn.close()

def InsertEmp(empID,ename,etel,password):
    conn=sqlite3.connect("DataBase.db")
    c=conn.cursor()
    sql='''insert into Emp(empID,ename,etel,password)
            VALUES (?,?,?,?)'''
    para=(empID,ename,etel,password)
    c.execute(sql,para)
    conn.commit()
    conn.close()

def InsertMenu(mealID,manme,empID,price,picture,grade,element):
    conn=sqlite3.connect("DataBase.db")
    c=conn.cursor()
    sql='''insert into Menu(mealID,manme,empID,price,picture,grade,element)
            VALUES (?,?,?,?,?,?,?)'''
    para=mealID,manme,empID,price,picture,grade,element
    c.execute(sql,para)
    conn.commit()
    conn.close()

def InsertOrderList(orderID,takeID,mealID,userID,state):
    conn=sqlite3.connect("DataBase.db")
    c=conn.cursor()
    sql='''insert into OrderList(orderID,takeID,mealID,userID,state)
            VALUES (?,?,?,?,?)'''
    para=orderID,takeID,mealID,userID,state
    c.execute(sql,para)
    conn.commit()
    conn.close()

def InsertUser(userID,uname,tel,password):
    conn=sqlite3.connect("DataBase.db")
    c=conn.cursor()
    sql='''insert into User(userID,uname,tel,password)
            VALUES (?,?,?,?)'''
    para=userID,uname,tel,password
    c.execute(sql,para)
    conn.commit()
    conn.close()

def UpdateAdmin(adminID,pwd):
    conn = sqlite3.connect("DataBase.db")
    c = conn.cursor()
    cursor=c.execute("update ADMIN set pwd='%s' where adminID='%s'"%(pwd,adminID))
    conn.commit()
    conn.close()

def Updatecomment(mealID,evaluate,grade):
    conn = sqlite3.connect("DataBase.db")
    c = conn.cursor()
    cursor=c.execute("update comment set evaluate='%s',grade='%s' where mealID='%s'"%(evaluate,grade,mealID))
    conn.commit()
    conn.close()

def UpdateMenu(mealID,grade):
    conn = sqlite3.connect("DataBase.db")
    c = conn.cursor()
    cursor=c.execute("update Menu set grade='%s' where mealID='%s'"%(grade,mealID))
    conn.commit()
    conn.close()

def UpdateOrderList(orderId,state):
    conn = sqlite3.connect("DataBase.db")
    c = conn.cursor()
    cursor=c.execute("update OrderList set state='%s' where orderID='%s'"%(state,orderId))
    conn.commit()
    conn.close()

def UpdateStore(storeID,number):
    conn = sqlite3.connect("DataBase.db")
    c = conn.cursor()
    cursor=c.execute("update Store set number='%s' where storeID='%s'"%(number,storeID))
    conn.commit()
    conn.close()

def SelectUser(uname):
    conn = sqlite3.connect('DataBase.db')
    c = conn.cursor()
    cursor = c.execute("select * from User where uname='%s'" % (uname))
    temp = ""
    for row in c:
        temp = row
    conn.close()
    return temp
def GetUserNum():
    conn = sqlite3.connect('DataBase.db')
    c = conn.cursor()
    cursor = c.execute("select count(uname) from User")

    result=cursor.fetchone()
    print(result[0])


def GetOrderListNum():
    conn = sqlite3.connect('DataBase.db')
    c = conn.cursor()
    cursor = c.execute("select count(orderID) from OrderList")
    result=cursor.fetchone()
    print(result[0])

def GetOrderList(state):
    conn = sqlite3.connect('DataBase.db')
    c = conn.cursor()
    cursor = c.execute("select * from OrderList where state='%s'" % (state))
    temp = []
    for row in c:
        temp.append(row)
    conn.close()
    return temp

def GetComment(mealID):
    conn = sqlite3.connect('DataBase.db')
    c = conn.cursor()
    cursor = c.execute("select * from comment where mealID='%s'" % (mealID))
    temp1=[]
    for row in c:
        lalala=[row[2]]
        temp1.append(lalala)
    conn.close()
    print(temp1)

    return temp1


if __name__=="__main__":
    # init_DB()
    # InsertUser(2,"Mashiro","123456789","123456789")
    # InsertAdmin(1,"12345","MashiroCl","1234556")
    # InsertEmp()
    # temp=SelectUser("MashiroCl")
    # InsertOrderList("4","2","lalqweala","asd","waiting")
    # GetUserNum()
    # GetOrderListNum()
    # Insertcomment("2","2","不好吃啊","59")
    GetComment(2)
    # temp=GetOrderList("waiting")
    # print(temp)
    # print(len(temp))
    # ShowAdmin()
    # ShowComment()
