from django.contrib import admin
from django.urls import path, include

from . import views
import accounts


urlpatterns = [
    path('', accounts.views.home, name="home"),
    path('products/', accounts.views.products, name="products"),
    path('customer/<str:pk_test>/', views.customers, name="customer"),

    path('create_order/<str:user_id>/', views.createOrder, name="create_order"),
    path('update_order/<str:user_id>/', views.updateOrder, name="update_order"),
    path('delete_order/<str:user_id>/', views.deleteOrder, name="delete_order"),


]
