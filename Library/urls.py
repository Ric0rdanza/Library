"""Library URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, re_path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.index),
    path('login/', views.login_page),
    path('register/', views.register_page),
    re_path(r'^detail/(\d*)', views.detail),
    re_path(r'^myaccount/(.*)', views.myaccount),
    path('modify_account/', views.modify_account),
    path('changepassword/', views.changepassword),
    path('newpassword/', views.new_password),
    path('login_action/', views.login),
    path('register_action/', views.register),
    path('logout_now/', views.logout),
    path('newbook/', views.manager_newbook),
    path('newbook_action/', views.newbook_action),
    re_path(r'^search/(\d*)', views.searchbook),
    re_path(r'^addwishlist/(\d*)', views.addwishlist),
    path('wishlist/', views.viewwishlist),
    re_path(r'^removewishlist/(\d*)', views.removewishlist),
    path('orderlist/', views.vieworderlist),
    re_path(r'^addorderlist/(\d*)', views.addorderlist),
    re_path(r'^removeorderlist/(\d*)', views.removeorderlist),
    path('borrowlist/', views.viewborrowlist),
    re_path(r'^addborrowlist/(\d*)', views.addborrowlist),
    path('record/', views.borrowrecord),
    re_path(r'^readerreturn/(\d*)', views.readerreturn),
    path('checkreturn/', views.manager_check),
    re_path(r'^checkreturn_action/(\d*)/(.*)', views.check_action)
]
