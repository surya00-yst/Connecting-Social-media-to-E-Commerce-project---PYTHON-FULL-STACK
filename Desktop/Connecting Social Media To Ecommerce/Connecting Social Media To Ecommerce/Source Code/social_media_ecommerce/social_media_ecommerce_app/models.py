from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    subject = models.CharField(max_length=40)
    message = models.TextField()

    class Meta:
        db_table = "Contact"


class Admin(models.Model):
    email = models.EmailField()
    password = models.CharField(max_length=100)


class Customer(models.Model):
    name = models.CharField(max_length=60)
    email = models.EmailField()
    mandal = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    state = models.CharField(max_length=40)
    age = models.IntegerField()
    gender = models.CharField(max_length=40)
    image = models.FileField()
    password = models.CharField(max_length=20)
    status = models.CharField(max_length=100, default='pending')


class Vendor(models.Model):
    name = models.CharField(max_length=60)
    email = models.EmailField()
    mandal = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    state = models.CharField(max_length=40)
    age = models.IntegerField()
    gender = models.CharField(max_length=40)
    image = models.FileField()
    password = models.CharField(max_length=20)
    status = models.CharField(max_length=100, default='pending')

    def __str__(self):
        return self.name


class Notification(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    date_time = models.DateTimeField(auto_now=True)


class Category(models.Model):
    title = models.CharField(max_length=100)


class Product(models.Model):
    email = models.EmailField()
    category = models.CharField(max_length=100)
    title = models.CharField(max_length=40)
    orign = models.CharField(max_length=80)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.FileField()
    description = models.TextField()
    brand = models.CharField(max_length=30)
    model = models.CharField(max_length=30)
    discount = models.IntegerField()
    specification = models.CharField(max_length=40)
    warranty = models.CharField(max_length=40)

    def __str__(self):
        return self.name


class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    quantity = models.BigIntegerField()
    cost = models.BigIntegerField()
    discount = models.BigIntegerField()
    total = models.BigIntegerField()
    customer_email = models.EmailField()
    vendor_email = models.EmailField()

    class Meta:
        db_table = 'Cart'


class Orders(models.Model):
    customer_email = models.EmailField()
    vendor_email = models.EmailField()
    quantity = models.BigIntegerField()
    cost = models.BigIntegerField()
    discount = models.BigIntegerField()
    total = models.BigIntegerField()
    address = models.TextField()
    delivery_date = models.DateField()
    order_datetime = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=100, default="Pending")


class Order_Products(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    quantity = models.BigIntegerField()
    cost = models.BigIntegerField()
    discount = models.BigIntegerField()
    total = models.BigIntegerField()
    customer_email = models.EmailField()
    vendor_email = models.EmailField()


class My_Preference(models.Model):
    email = models.EmailField()
    category = models.CharField(max_length=100)


class Review(models.Model):
    customer_email = models.EmailField()
    orders = models.ForeignKey(Product, on_delete=models.CASCADE)
    reviews = models.CharField(max_length=100)
    date_time = models.DateTimeField(auto_now=True)
    ratings = models.BigIntegerField()

    class Meta:
        db_table = "Review"


class Friends_Requests(models.Model):
    customers = models.ForeignKey(Customer, on_delete=models.CASCADE)
    from_email = models.EmailField()
    to_email = models.EmailField()
    status = models.CharField(max_length=100, default="Pending")

    class Meta:
        db_table = "Friends_Requests"
        unique_together = ('from_email', 'to_email')


class Post(models.Model):
    posts_for = models.CharField(max_length=100)
    email = models.EmailField()
    title = models.CharField(max_length=100)
    description = models.TextField()
    date_time = models.DateTimeField(auto_now=True)
    file = models.FileField()
    status = models.CharField(max_length=100, default="Pending")

    class Meta:
        db_table = "Post"


class Likes(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    customer_email = models.EmailField()
    date_time = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('post', 'customer_email')


class Review(models.Model):
    customer_email = models.EmailField()
    orders = models.ForeignKey(Product, on_delete=models.CASCADE)
    reviews = models.CharField(max_length=100)
    date_time = models.DateTimeField(auto_now=True)
    ratings = models.BigIntegerField()

    class Meta:
        db_table = "Review"


class Comment(models.Model):
    customer_email = models.EmailField()
    post_id = models.ForeignKey(Post,on_delete=models.CASCADE)
    comment = models.CharField(max_length=100)
    date_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "Comment"

