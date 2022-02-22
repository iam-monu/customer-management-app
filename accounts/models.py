from django.db import models

from django.contrib.auth.models import User

# Create your models here.



class Customer(models.Model):
    user =models.OneToOneField(User,null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=300, null=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.FloatField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=300, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    CATEGORY =(
                ('Indoor', 'Indoor'),
                ('Out Door', 'Outdoor'),
                )
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField(null=True)
    category = models.CharField(max_length=200, null=True,  choices=CATEGORY)
    description = models.CharField(max_length=200, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Out for Delivery', 'Out for Delivery'),
        ('Delivered', 'Delivered'),
        )
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=200, null=True , choices=STATUS)

    note = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.product.name