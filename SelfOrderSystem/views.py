from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
import DataBase


def test(request):
    username=request.POST.get('username')
    print(username)
    dict=""
    return HttpResponse("牵牛花与加濑同学")

'''
登陆注册部分
'''
# 注册
def register(request):
    username=request.POST.get('username')
    password=request.POST.get('password')
    tele=request.POST.get('telephone_number')

    #查重
    #合格 未出现重复
    if(len(DataBase.SelectUser(username))==0):
        #注册成功
        # 写入数据库
        DataBase.InsertUser(userID=DataBase.GetUserNum(),username=username,tel=tele,password=password)
    else:
        #用户名重复
        pass


#登录
def sign(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    #查数据库
    if(DataBase.SelectUser(username)[3]!=password):
        #提示用户名密码不匹配
        pass
    else:
        #登陆成功
        pass

'''
点餐部分
'''
def OrderFood(request):
    order=request.POST.get("")  #获取点的订单

'''
做菜查库存
'''

'''
评价部分
'''

def login(request):
    return render_to_response("login.html")

def register(request):
    return render_to_response("register.html")

def sign(request):
    return render_to_response("sign.html")

def menu(request):
    return render_to_response("menu.html")


