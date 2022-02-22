from tokenize import group
from django import forms

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory

from accounts.decorators import unauthenticated_user

from .models import *
from .forms import OrderForm, CreateUserForm
from .filters import OrderFilter

from django.contrib.auth.forms import UserCreationForm

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout 

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group    

from .decorators import unauthenticated_user,allowed_users,admin_only

@unauthenticated_user
def registerPage(request):


    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user=form.save()
            username = form.cleaned_data.get('username')

            group =Group.objects.get(name='customer')
            user.groups.add(group)

            Customer.objects.create(
                user=user,
            )

            messages.success(request,'Account created for ' + username )

            return redirect('login')

    context = {'form' : form}
    return render(request, 'accounts/register.html', context)

@unauthenticated_user
def loginPage(request):

    if request.method =='POST':
        username= request.POST.get('username')
        password= request.POST.get('password')

        user= authenticate(request,username=username, password=password )

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.info(request,'Username or password incorrect')

    context = {}
    return render(request, 'accounts/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@admin_only
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    # total_customers = customers.count()
    total_orders = orders.count()

    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {'orders': orders, 'customers': customers,
               'total_orders': total_orders, 'delivered': delivered,
               'pending': pending}
    return render(request, 'accounts/dashboard.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    orders = request.user.customer.order_set.all()
    print('ORDERS:', orders)
    
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

	
    context = {'orders' : orders,'total_orders': total_orders, 'delivered': delivered,
               'pending': pending}
    return render(request, 'accounts/user.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
    products = Product.objects.all()

    return render(request, 'accounts/products.html', {'products': products})


#
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customers(request, pk_test):
    customer = Customer.objects.get(id=pk_test)

    orders = customer.order_set.all()
    orders_count = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)

    orders = myFilter.qs

    context = {'customer': customer, 'orders': orders,
               'orders_count': orders_count, 'myFilter': myFilter}
    return render(request, 'accounts/customers.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request, user_id):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'))
    customer = Customer.objects.get(id=user_id)
    # formset = OrderFormSet(instance=customer)
    form = OrderForm(initial={'customer': customer})
    if request.method == 'POST':
        print('Printing post', request.POST)
        form = OrderForm(request.POST)
        # formset = OrderForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form}
    # context= {'formset': formset }
    return render(request, 'accounts/order_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request, user_id):
    order = Order.objects.get(id=user_id)
    form = OrderForm(instance=order)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form}
    return render(request, 'accounts/order_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, user_id):
    order = Order.objects.get(id=user_id)
    if request.method == 'POST':
        order.delete()
        return redirect('/')

    context = {'order': order}
    return render(request, 'accounts/delete.html', context)
