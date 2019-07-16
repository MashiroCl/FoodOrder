from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
import DataBase
from django.http import JsonResponse
import json
from spa.classifiers import SVMClassifier,classifyComment,DictClassifier
from sklearn.externals import joblib
def test(request):
#     # username=request.POST.get('username')
#     # print(username)
#     # dict=""
#     # return HttpResponse("牵牛花与加濑同学")
#     # data={}
#     # data= DataBase.GetOrderList("waiting")
#     # data={}
#     # data['data']='frick'
#     classifiers.start()
#     return render_to_response('login.html',{'data':data})
    return render_to_response('login.html')

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

def comment(request):
    return render_to_response("comment.html")

def getComment(request):
    mealid=request.POST.get("id")
    url=request.POST.get("url")
    print(mealid)
    print(url)
    comment =DataBase.GetComment(mealID=mealid);
    print(comment)
    comment=json.dumps(comment)

    score=DataBase.calScore(mealID=mealid)
    comment=JsonResponse({"comment":comment,"score":score})
    return comment

def getOrder(request):
    order=DataBase.GetOrderList('waiting')

def PayEnd(request):
    return render_to_response("waiting.html")

def PayEndProcess(request):
    print("PayEndProcess here!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    userID=request.POST.get("id")
    meal=request.POST.get("dish")
    # temp_meal=meal.splite(",")

    # for each in


    orderNum=DataBase.GetOrderListNum()+1
    sequenceNum=DataBase.GetSequenceNum()

    DataBase.InsertOrderList(orderNum,sequenceNum,meal,userID,"waiting")
    return JsonResponse({'orderNum': orderNum,'waitingNum':sequenceNum})                  #返回的orderNum放到url,付完款跳转到取餐完成评价界面

def home(request):
    return render_to_response("home.html")


def Kitchen(request):
    return render_to_response("Kitchen.html")


def KitchenGetOrder(request):
    order=DataBase.GetOrderList1("waiting")
    order=json.dumps(order)
    order=JsonResponse({"order":order})

    return order

def checkStore(request):
    dish=request.POST.getlist("dish")
    dishNum=request.POST.getlist("dishNum")
    print(dish)
    print(dishNum)
    number=[]
    storeId=[]
    for i in range(len(dish)):
        temp1,temp2=DataBase.UpdateStore(dish[i],-int(dishNum[i]))
        number.append(temp1)
        storeId.append(temp2)
    print(number)
    print(storeId)
    numberMinus=[]
    lalala=""
    for i in range(len(number)):
        if number[i]<0:
            numberMinus.append(storeId[i])
            lalala = lalala + "编号" + storeId[i]

    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print(numberMinus)

    numberMinus = json.dumps(numberMinus)
    numberMinus = JsonResponse({"numberMinus": lalala})
    return numberMinus

def KitchenFinished(request):
    orderNum=request.POST.get("orderNum")
    print(orderNum)
    DataBase.UpdateOrderList(orderNum,"finished")
    return HttpResponse("finished")

def FoodDelivered(request):
    orderNum=request.POST.get("state")  #订单号
    temp=DataBase.GetOrderList2(orderNum)
    state=temp[0][4]
    if(state=="waiting"):
        state=0
    elif(state=="finished"):
        state=1
    return JsonResponse({"isFinished":state})

    DataBase.UpdateOrderList(orderNum,"finished")

def getCommentFromCus(request):
    print("getCommentFromCus")
    temp=request.POST.getlist("comdata")
    print("?????????????????")
    print(temp[2])
    userID=temp[0]
    dish=[]
    dishComment=[]
    i=0
    while i < len(temp):
        if(i==0):
            i=i+1
        else:
            dish.append(temp[i])
            print(dish)
            i=i+1
            print(i)
            dishComment.append(temp[i])
            print(dishComment)
            i=i+1

    for i in range(len(dish)):
        print(i)
        DataBase.Insertcomment(userID,dish[i],dishComment[i],-1)
        classifyComment("2",dish[i])
    return JsonResponse({'res': 1})