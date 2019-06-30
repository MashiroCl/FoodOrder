from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse

# Create your views here.
def test(request):
    username=request.POST.get('username')
    print(username)
    dict=""
    return HttpResponse("牵牛花与加濑同学")

# 登录注册部分
def register(request):
    username=request.POST.get('username')
    password=request.POST.get('password')
    tele=request.POST.get('telephone_number')
    #查重
    #写入数据库
def sign(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    #查数据库
    #登录进入或者提示用户名密码不匹配

#点餐部分
def OrderFood(request):
    order=request.POST.get("")  #获取点的订单

#评价

#

def login(request):
    return render_to_response("login.html")