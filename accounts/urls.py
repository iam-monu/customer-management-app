from django.contrib import admin
from django.urls import path, include

from . import views
import accounts


urlpatterns = [
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),

    path('', accounts.views.home, name="home"),
    path('user/', accounts.views.userPage, name="user-page"),
    path('products/', accounts.views.products, name="products"),
    path('customer/<str:pk_test>/', views.customers, name="customer"),

    path('create_order/<str:user_id>/', views.createOrder, name="create_order"),
    path('update_order/<str:user_id>/', views.updateOrder, name="update_order"),
    path('delete_order/<str:user_id>/', views.deleteOrder, name="delete_order"),


]
