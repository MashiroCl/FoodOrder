from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
import DataBase
from django.http import JsonResponse
import json

def test(request):
    # username=request.POST.get('username')
    # print(username)
    # dict=""
    # return HttpResponse("牵牛花与加濑同学")
    # data={}
    data= DataBase.GetOrderList("waiting")
    # data={}
    # data['data']='frick'
    return render_to_response('login.html',{'data':data})
    # return render_to_response('login.html')

def test1(request):
    data = DataBase.GetOrderList("waiting")
    # data={}
    # data['data']='frick'
    return render_to_response('login.html', {'data': data})

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
        DataBase.InsertUser(userID=DataBase.GetUserNum()+1,uname=username,tel=phone,password=password)
        return JsonResponse({'res': 1})
    else:
        return JsonResponse({'res': 0})


#登录
def signCheck(request):
    print("sign checking")
    username = request.POST.get('username')
    password = request.POST.get('password')
    print(username)
    print(password)
    #查数据库
    if(DataBase.SelectUser(username)[3]!=password):
        #提示用户名密码不匹配
        return JsonResponse({'res': 0})
    else:
        #登陆成功
        return JsonResponse({'res': 1})

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
    waitingOrder=DataBase.GetOrderList("waiting")

    # return render_to_response("login.html")
    data=[1,2,3,4]
    #传给html用
    return render_to_response(request,'login.html',{'data':data})
    #传递给js用

def register(request):
    return render_to_response("register.html")

def sign(request):
    return render_to_response("sign.html")

def menu(request):
    return render_to_response("menu.html")

def news(request):
    return render_to_response("news.html")

def Settlement(request):
    return render_to_response("Settlement.html")


def getComment(request):
    id=request.POST.get("id")
    url=request.POST.get("url")
    print(id)
    print(url)
    comment =DataBase.GetComment(mealID=2);
    print(comment)
    comment=json.dumps(comment)
    comment=JsonResponse({"comment":comment})
    return comment

def getOrder(request):
    order=DataBase.GetOrderList('waiting')

def PayEnd(request):
    order=request.POST.get("order")
    price=request.POST.get("price")
    DataBase.InsertOrderList(DataBase.GetOrderListNum()+1,DataBase.GetSequenceNum(),order," ","waiting")     #UserID没有

def Kitchen(request):
    return render_to_response("Kitchen.html")

def KitchenGetOrder(request):
    order=DataBase.GetOrderList("waiting")
    order=json.dumps(order)
    order=JsonResponse({"order":order})

    return order