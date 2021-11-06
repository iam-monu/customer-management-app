from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import *
from .forms import OrderForm

def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    # total_customers = customers.count()
    total_orders = orders.count()

    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {'orders': orders,'customers': customers,
               'total_orders': total_orders, 'delivered': delivered,
               'pending': pending}
    return render(request, 'accounts/dashboard.html', context)


def products(request):
    products = Product.objects.all()

    return render(request, 'accounts/products.html', {'products': products})


#
def customers(request, pk_test):
    customers = Customer.objects.get(id=pk_test)

    orders = customers.order_set.all()
    orders_count = orders.count()

    context = {'customers': customers , 'orders':orders,
               'orders_count': orders_count}
    return render(request, 'accounts/customers.html', context)


def createOrder(request):

    form = OrderForm()
    if request.method == 'POST':
        print('Printing post',request.POST)
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    context= {'form': form}
    return render(request, 'accounts/order_form.html',context)


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



def deleteOrder(request,user_id):
    order = Order.objects.get(id=user_id)
    if request.method == 'POST':
            order.delete()
            return redirect('/')

    context= {'order': order}
    return render(request, 'accounts/delete.html',context)


