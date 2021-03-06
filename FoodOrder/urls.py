"""FoodOrder URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import SelfOrderSystem.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', SelfOrderSystem.views.login),
    path('test/', SelfOrderSystem.views.test),
    path('register/',SelfOrderSystem.views.register),
    path('menu/',SelfOrderSystem.views.menu),
    path('sign/',SelfOrderSystem.views.sign),
    path('home/',SelfOrderSystem.views.home),
    path('registerCheck/',SelfOrderSystem.views.registerCheck),
    path('news/', SelfOrderSystem.views.news),
    path('getComment/', SelfOrderSystem.views.getComment),
    path('Settlement/', SelfOrderSystem.views.Settlement),
    path('PayEnd/', SelfOrderSystem.views.Settlement),
    path('KitchenGetOrder/',SelfOrderSystem.views.KitchenGetOrder),
    path('Kitchen/', SelfOrderSystem.views.Kitchen),
    path('signCheck/', SelfOrderSystem.views.signCheck),
    path('PayEndProcess/', SelfOrderSystem.views.PayEndProcess),
    path('waiting/', SelfOrderSystem.views.PayEnd),
    path('comment/', SelfOrderSystem.views.comment),
    path('checkStore/', SelfOrderSystem.views.checkStore),
    path('KitchenFinished/', SelfOrderSystem.views.KitchenFinished),
    path('getCommentFromCus/', SelfOrderSystem.views.getCommentFromCus),
    path('FoodDelivered/', SelfOrderSystem.views.FoodDelivered),

]
