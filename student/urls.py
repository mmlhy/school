from django.urls import path
from django.conf.urls import url,include
from . import views

urlpatterns = [
    path('index/',views.index),
    path('login/<int:type>/',views.login),
    path('get_valiCode_img/',views.get_valiCode_img),
    path('',views.index),
    path('schengji/',views.schengji),
    path('kebiao/',views.skebiao),
    path('test/',views.test),
    path('qingjia/',views.qingjia),
    path('jilu/',views.jilu),
    path('kezhuang/',views.kezhuang),
    path('dchengji/',views.dchengji),
    path('ddchengji/',views.ddchengji),
]
