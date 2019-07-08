from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
import DataBase
from django.http import JsonResponse
import json

def test(request):
    username=request.POST.get('username')
    print(username)
    dict=""
    return HttpResponse("牵牛花与加濑同学")

'''
登陆注册部分
'''
# 注册
def registerCheck(request):
    username=request.POST.get('username')
    password=request.POST.get('password')
    phone=request.POST.get('phone')

    print(username)
    print(password)
    print(phone)

    #查重
    #合格 未出现重复
    if(len(DataBase.SelectUser(username))==0):
        #注册成功
        # 写入数据库
        DataBase.InsertUser(userID=DataBase.GetUserNum(),uname=username,tel=phone,password=password)
    else:
        #用户名重复
        pass
    dict=""

    return JsonResponse({'res': 1})

#登录
def signCheck(request):
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


