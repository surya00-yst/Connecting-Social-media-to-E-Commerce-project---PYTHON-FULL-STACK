from itertools import chain

from django.contrib import messages
from django.db.models import Q, Count
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .models import Admin, Customer, Vendor, Notification, Category, Product, Cart, Orders, Order_Products, \
    My_Preference, Contact, Likes
from .forms import ContactForm, CustomerForm, VendorForm, NotificationForm, CategoryForm, ProductForm, CartForm, \
    OrderForm, Order_ProductsForm, AdminForm, My_PreferenceForm, ReviewForm, Review, Friends_Requests, PostForm, Post, \
    Comment, CommentForm
from django.http import JsonResponse, HttpResponseForbidden


# Create your views here.

def index(request):
    return render(request, "index.html", {})


def doctor(request):
    return render(request, "doctor.html", {})


def departments(request):
    return render(request, "departments.html", {})


def department_single(request):
    return render(request, "department-single.html", {})


def blog_single(request):
    return render(request, "blog-single.html", {})


def blog(request):
    return render(request, "blog.html", {})


def about(request):
    return render(request, "about.html", {})




def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        print(form.errors)
        if form.is_valid():
            form.save()
            return render(request, "contact.html", {"msg": "Thanks For Contacting Us"})

        return render(request, "contact.html", {"msg": "While Contacting Us Your Getting Error"})
    return render(request, "contact.html", {})


def customer_register_form(request):
    if request.method == "POST":
        form = CustomerForm(request.POST, request.FILES)
        email = request.POST['email']
        if Customer.objects.filter(email=email).exists():
            return render(request, "customer_register_form.html",
                          {"msg": "This Email Already Exists Please Try With Another Email"})

        else:
            if form.is_valid():
                print(form.errors)
                form.save()
                return render(request, "customer_login.html", {"msg": "Registered Successfully Done"})
            return render(request, "customer_register_form.html", {"msg": "Not Registered Successfully Done"})
    return render(request, "customer_register_form.html", {})


def customer_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        log = Customer.objects.filter(email=email, password=password)
        if log.exists():
            if log[0].status == "Accepted":
                request.session['email'] = email
                return render(request, "customer_home.html", {"msg": "Accepted Successfully"})
            elif log[0].status == "Rejected":
                return render(request, "customer_login.html", {"msg": "Rejected login"})

            else:
                return render(request, "customer_login.html", {"msg": "Pending"})
        return render(request, "customer_login.html", {"msg": "Login Failed"})
    return render(request, "customer_login.html", {})


def customer_home(request):
    return render(request, "customer_home.html", {})


def customer_logout(request):
    return redirect('/customerlogin')


def customer_profile(request):
    email = request.session['email']
    profile = Customer.objects.get(email=email)
    return render(request, "customer_profile.html", {"x": profile})




def admin_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        log = Admin.objects.filter(email=email, password=password)
        if log.exists():
            request.session['email'] = email
            return render(request, "admin_home.html", {})
        return render(request, "admin_login.html", {"msg": "Login Failed"})
    return render(request, "admin_login.html", {})




def admin_Logout(request):
    request.session.flush()
    return redirect('/admin_login')


def admin_home(request):
    return render(request, "admin_home.html", {})


def admin_viewcontact(request):
    contact = Contact.objects.all()
    return render(request, "admin_viewcontact.html", {"contact": contact})


def admin_viewcustomer(request):
    customer = Customer.objects.all()
    return render(request, "admin_viewcustomer.html", {"customer": customer})


def accept_customer(request, id):
    cus = Customer.objects.get(id=id)
    cus.status = 'Accepted'
    cus.save()
    return redirect('/admin_viewcustomer')


def reject_customer(request, id):
    cus = Customer.objects.get(id=id)
    cus.status = 'Rejected'
    cus.save()
    return redirect('/admin_viewcustomer')


def customer_edit(request):
    email = request.session['email']
    cus = Customer.objects.get(email=email)
    return render(request, 'customer_edit.html', {'x': cus})


def update(request):
    if request.method == 'POST':
        id = request.POST['id']
        cus = Customer.objects.get(id=id)
        form = CustomerForm(request.POST, request.FILES, instance=cus)
        print(form.errors)
        if form.is_valid():
            form.save()
            return redirect('/customer_profile')
        return render(request, "customer_edit.html", {})
    return render(request, "customer_edit.html", {})


def is_login(request):
    if request.session.__contains__('email'):
        return True
    else:
        return False


def customer_change_password(request):
    email = request.session.get("email")
    if not email:
        return redirect('/customerlogin')

    if is_login(request):
        if request.method == 'POST':
            password = request.POST['password']
            new_password = request.POST['new_password']
            if password == new_password:
                return render(request, "customer_change_password.html",
                              {"msg": "Your Old Password And New Password Are Same.", "email": email})
            try:
                user = Customer.objects.get(email=email, password=password)
                user.password = new_password
                user.save()
                messages.success(request, 'Password Changed Successfully')
                return redirect('/customerlogin')
            except Exception as e:
                print(e)
                return render(request, "customer_change_password.html", {"msg": "Invalid Credentials", "email": email})
        return render(request, "customer_change_password.html", {"email": email})
    else:
        return redirect('/customerlogin')


def deactivate(request, id):
    cus = Customer.objects.get(id=id)
    cus.status = 'pending'
    cus.save()
    return redirect('/customerlogin')


def admin_change_password(request):
    email = request.session.get("email")
    if not email:
        return redirect('/admin_login')

    if is_login(request):
        if request.method == 'POST':
            password = request.POST['password']
            new_password = request.POST['new_password']
            if password == new_password:
                return render(request, "admin_change_password.html",
                              {"msg": "Your Old Password And New Password Are Same.", "email": email})
            try:
                user = Admin.objects.get(email=email, password=password)
                user.password = new_password
                user.save()
                messages.success(request, 'Password Changed Successfully')
                return redirect('/admin_login')
            except Exception as e:
                print(e)
                return render(request, "admin_change_password.html", {"msg": "Invalid Credentials", "email": email})
        return render(request, "admin_change_password.html", {"email": email})
    else:
        return redirect('/admin_login')


def vendor_register_form(request):
    if request.method == "POST":
        form = VendorForm(request.POST, request.FILES)
        email = request.POST['email']
        if Vendor.objects.filter(email=email).exists():
            return render(request, "vendor_register_form.html",
                          {"msg": "This Email Already Exists Please Try With Another Email"})

        else:
            if form.is_valid():
                print(form.errors)
                form.save()
                return render(request, "vendor_login.html", {"msg": "Registration Successfully Done"})
            return render(request, "vendor_register_form.html", {"msg": "Not Registration Successfully Done"})
    return render(request, "vendor_register_form.html", {})


def vendor_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        log = Vendor.objects.filter(email=email, password=password)
        if log.exists():
            request.session['email'] = email
            return render(request, "vendor_home.html", {"msg": "Accepted Successfully"})
        return render(request, "vendor_login.html", {"msg": "Login Failed"})
    return render(request, "vendor_login.html", {})


def vendor_home(request):
    return render(request, "vendor_home.html", {})


def vendor_logout(request):
    return redirect('/vendor_login')


def vendor_profile(request):
    email = request.session['email']
    profile = Vendor.objects.get(email=email)
    return render(request, "vendor_profile.html", {"x": profile})


def accept_vendor(request, id):
    vendor = Vendor.objects.get(id=id)
    vendor.status = 'accepted'
    vendor.save()
    return redirect('/view_vendor')


def reject_vendor(request, id):
    vendor = Vendor.objects.get(id=id)
    vendor.status = 'rejected'
    vendor.save()
    return redirect('/view_vendor')


def vendor_edit(request):
    email = request.session['email']
    vendor = Vendor.objects.get(email=email)
    return render(request, 'vendor_edit.html', {'x': vendor})


def vendor_update(request):
    if request.method == 'POST':
        id = request.POST['id']
        vendor = Vendor.objects.get(id=id)
        form = VendorForm(request.POST, request.FILES, instance=vendor)
        print(form.errors)
        if form.is_valid():
            form.save()
            return redirect('/vendor_profile')
        return render(request, "vendor_edit.html", {})
    return render(request, "vendor_edit.html", {})


def vendor_change_password(request):
    email = request.session.get("email")
    if not email:
        return redirect('/vendor_login')

    if is_login(request):
        if request.method == 'POST':
            password = request.POST['password']
            new_password = request.POST['new_password']
            if password == new_password:
                return render(request, "vendor_change_password.html",
                              {"msg": "Your Old Password And New Password Are Same.", "email": email})
            try:
                user = Vendor.objects.get(email=email, password=password)
                user.password = new_password
                user.save()
                messages.success(request, 'Password Changed Successfully')
                return redirect('/vendor_login')
            except Exception as e:
                print(e)
                return render(request, "vendor_change_password.html", {"msg": "Invalid Credentials", "email": email})
        return render(request, "vendor_change_password.html", {"email": email})
    else:
        return redirect('/vendor_login')


def deactivate_vendor(request, id):
    vendor = Vendor.objects.get(id=id)
    vendor.status = 'pending'
    vendor.save()
    return redirect('/vendor_login')


def vendor_view_customer(request):
    customer = Customer.objects.all()
    return render(request, "vendor_view_customer.html", {"customer": customer})


def add_notification(request):
    if request.method == 'POST':
        form = NotificationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_notification')
        return render(request, "add_notification.html", {})
    return render(request, "add_notification.html", {})


def view_notification(request):
    profile = Notification.objects.all()
    return render(request, "view_notification.html", {"profile": profile, })


def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_category')
        return render(request, "add_category.html", {})
    return render(request, "add_category.html", {})


def view_category(request):
    profile = Category.objects.all()
    return render(request, "view_category.html", {"profile": profile, })


def view_vendor(request):
    customer = Vendor.objects.all()
    return render(request, "view_vendor.html", {"customer": customer})


def delete_view_notification(request, id):
    notify = Notification.objects.get(id=id)
    notify.delete()
    return redirect('/add_notification')


def delete_view_category(request, id):
    cat = Category.objects.get(id=id)
    cat.delete()
    return redirect('/add_category')


def add_product(request):
    email = request.session['email']
    category = Category.objects.all()
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        print('********************************')
        print(form.errors)
        if form.is_valid():
            form.save()
            return redirect('view_product')
        return render(request, "add_product.html", {"email": email})
    return render(request, "add_product.html", {"email": email, "category": category})


def view_product(request):
    email = request.session['email']
    profile = Product.objects.filter(email=email)
    return render(request, "view_product.html", {"profile": profile})


def customer_view_product(request):
    profile = Product.objects.all()
    return render(request, "customer_view_product.html", {"profile": profile})


def delete_view_product(request, id):
    cat = Product.objects.get(id=id)
    cat.delete()
    return redirect('/add_product')


def product_edit(request, id):
    edit = Product.objects.get(id=id)
    return render(request, 'product_edit.html', {'x': edit})


def product_update(request):
    if request.method == 'POST':
        id = request.POST['id']
        product = Product.objects.get(id=id)
        form = ProductForm(request.POST, request.FILES, instance=product)
        print(form.errors)
        if form.is_valid():
            form.save()
            return redirect('/view_product')
        return render(request, "product_edit.html", {})
    return render(request, "product_edit.html", {})


def view_cart(request):
    email = request.session['email']
    cate = Cart.objects.filter(customer_email=email)
    tq = 0
    tc = 0
    td = 0
    fc = 0
    for x in cate:
        tq = tq + int(x.quantity)
        tc = tc + int(x.cost * x.quantity)
        td = td + int(x.discount * x.quantity)
        fc = tc - td
    return render(request, "view_cart.html", {"cate": cate, "td": td, "tc": tc, "tq": tq, "fc": fc})


def delete_view_cart(request, id):
    cart = Cart.objects.get(id=id)
    cart.delete()
    return redirect('/view_cart')


def customer_view_vendors(request):
    vendor = Vendor.objects.all()
    return render(request, "customer_view_vendors.html", {"vendor": vendor})


def customer_view_notification(request):
    profile = Notification.objects.all()
    return render(request, "customer_view_notification.html", {"profile": profile, })


def add_to_cart(request, id):
    email = request.session["email"]
    customer = Customer.objects.get(email=email)
    product = Product.objects.get(id=id)

    if request.method == "POST":
        # Check if the product is already in the cart
        existing_cart_item = Cart.objects.filter(product=product, customer_email=customer.email).first()

        if existing_cart_item:
            return render(request, "add_to_cart.html", {
                "msg": "This product is already in your cart.",
                'email': email,
                'x': product
            })

        # Check if there are items in the cart from a different vendor
        cart_items = Cart.objects.filter(customer_email=customer.email)

        if cart_items.exists():
            existing_vendor_email = cart_items.first().vendor_email

            if existing_vendor_email != product.email:
                return render(request, "add_to_cart.html", {
                    "msg": "You can only select products from one vendor at a time. Please complete your current order before adding products from another vendor.",
                    "customer": customer,
                    "product": product,
                    "email": email
                })

        # If all checks pass, add the product to the cart
        form = CartForm(request.POST, request.FILES)
        print(form.errors)
        if form.is_valid():
            form.save()
            return render(request, "add_to_cart.html", {
                'msg': 'Product successfully added to your cart',
                'email': email,
                'x': product
            })
        else:
            print("Form is not valid:", form.errors)

    return render(request, "add_to_cart.html", {
        'email': email,
        'x': product
    })


# def add_to_cart(request):
#     email = request.session['email']
#     customer = Customer.objects.get(email=email)
#     print(customer)
#     email1 = request.session['email']
#     product = Product.objects.filter(email=email1)
#     print("hii")
#     if request.method == "POST":
#         if Cart.objects.filter(product=product, customer_email=customer.email).exists():
#             return render(request, "add_to_cart.html",
#                           {"msg": "This Item Already In Cart", "customer": customer, "product": product,
#                            "email": email})
#         else:
#             book = CartForm(request.POST)
#             print("errors", book.errors)
#             print('hii')
#             if book.is_valid():
#                 print("error:", book.errors)
#                 book.save()
#                 return render(request, "add_to_cart.html",
#                               {"msg": "Added To Cart", "customer": customer, "product": product,
#                                "email": email})
#         return render(request, "add_to_cart.html",
#                       {"customer": customer.id, "product": product, "email": email})
#     return render(request, "add_to_cart.html",
#                   {"customer": customer.id, "product": product, "email": email})


# def customer_view_cart(request):
#     email = request.session["email"]
#     cart = Cart.objects.filter(customer_email=email)
#     tq = 0
#     tc = 0
#     td = 0
#     fc = 0
#     for x in cart:
#         tq = tq + int(x.quantity)
#         tc = tc + int(x.cost * x.quantity)
#         td = td + int(x.discount * x.quantity)
#     fc = fc + tc - td
#     return render(request, "view_cart.html", {"cart": cart, "td": td, "tc": tc, "tq": tq, "fc": fc})


# def checkout(request):
#     cart = Cart.objects.all()
#     tq = 0
#     tc = 0
#     td = 0
#     fc = 0
#     customer_mail = 0
#     vendor_mail = 0
#     for x in cart:
#         customer_mail = x.customer_email
#         vendor_mail = x.vendor_email
#         tq = tq + int(x.quantity)
#         tc = tc + int(x.cost * x.quantity)
#         td = td + int(x.discount * x.quantity)
#     fc = fc + tc - td
#     if request.method == "POST":
#         print("hello")
#         order_form = OrderForm(request.POST)
#         print("errors", order_form.errors)
#         print('hii')
#         if order_form.is_valid():
#             print("error:", order_form.errors)
#             x = order_form.save()
#             print("x = ", x.id)
#             cart_1 = Cart.objects.all()
#             for item in cart_1:
#                 Order_Products.objects.create(order=x, product=item.product, cost=item.cost, quantity=item.quantity,
#                                               discount=item.discount, total=item.total, title=item.title,
#                                               customer_mail=item.customer_mail,
#                                               vendor_mail=item.vendor_mail)
#
#             cart_1.delete()
#             return render(request, "checkout.html",
#                           {"msg": "Your Order Is Success", "customer_mail": customer_mail, "vmail": vendor_mail,
#                            "td": td, "tc": tc,
#                            "tq": tq, "fc": fc})
#     return render(request, "checkout.html",
#                   {"customer_mail": customer_mail, "vendor_mail": vendor_mail, "td": td, "tc": tc, "tq": tq, "fc": fc})
def checkout(request):
    print("Checkout called")
    cart_items = Cart.objects.filter(customer_email=request.session["email"])

    tq = sum(item.quantity for item in cart_items)
    tc = sum(item.cost * item.quantity for item in cart_items)
    td = sum(item.discount * item.quantity for item in cart_items)
    fc = tc - td

    if request.method == "POST":
        order_form = OrderForm(request.POST)
        print("POST data received:", request.POST)

        if order_form.is_valid():
            order = order_form.save()
            print("Order saved with ID:", order.id)

            for item in cart_items:
                Order_Products.objects.create(
                    order=order,
                    product=item.product,
                    title=item.product.title,
                    quantity=item.quantity,
                    cost=item.cost,
                    discount=item.discount,
                    total=item.total,
                    customer_email=item.customer_email,
                    vendor_email=item.vendor_email
                )

            cart_items.delete()
            return render(request, "checkout.html", {
                "msg": "Your Order Is Success",
                "customer_email": order.customer_email,
                "vendor_email": order.vendor_email,
                "td": td,
                "tc": tc,
                "tq": tq,
                "fc": fc
            })
        else:
            print("Form is not valid:", order_form.errors)
    else:
        print("Request method not POST")

    return render(request, "checkout.html", {
        "customer_email": cart_items[0].customer_email if cart_items else "",
        "vendor_email": cart_items[0].vendor_email if cart_items else "",
        "td": td,
        "tc": tc,
        "tq": tq,
        "fc": fc
    })


def my_orders(request):
    email = request.session['email']
    orders = Orders.objects.filter(customer_email=email)
    return render(request, "my_orders.html", {"orders": orders})


def my_orders_products(request, id):
    orders = Orders.objects.get(id=id)
    order_products = Order_Products.objects.filter(order_id=orders.id)
    return render(request, "my_orders_products.html", {"order_products": order_products})


def customer_view_products(request, id):
    order_products = Order_Products.objects.filter(order_id=id)
    return render(request, "customer_view_products.html", {"order_products": order_products})


def edit_item(request, id):
    cart = Cart.objects.get(id=id)
    return render(request, "edit_item.html", {"cart": cart})


def edit_item_update(request):
    if request.method == "POST":
        print("error:")
        id = request.POST["id"]
        print("hello")
        user = Cart.objects.get(id=id)
        users = CartForm(request.POST, instance=user)
        print("error:", users.errors)
        if users.is_valid():
            print("error:", users.errors)
            users.save()
        return redirect("/customer_view_cart")
    return redirect("/customer_view_cart")


def remove_item(request, id):
    cart = Cart.objects.get(id=id)
    cart.delete()
    return redirect("/customer_view_cart")


def customer_checkout(request):
    order = Orders.objects.all()
    return render(request, "customer_checkout.html", {"order": order})

def cancel_order(request, id):
    email = request.session["email"]
    orders = Orders.objects.get(id=id)
    if request.method == "POST":
        print("hii")
        form = OrderForm(request.POST, instance=orders)
        print("hii22")
        print(form.errors)
        print("hii3")
        if form.is_valid():
            print(form.errors)
            orders.status = 'Cancelled'
            form.save()
            return redirect("/my_orders")
        return render(request, "cancel_order.html", {"orders": orders, "email":email})
    return render(request, "cancel_order.html", {"orders": orders, "email":email})


def customer_cart_products(request, id):
    order_products = Order_Products.objects.filter(order_id=id)
    return render(request, "customer_cart_products.html", {"order_products": order_products})


def accept_checkout(request, id):
    accept = Orders.objects.get(id=id)
    accept.status = 'Accepted'
    accept.save()
    return redirect('/vendor_checkout')


def reject_checkout(request, id):
    reject = Orders.objects.get(id=id)
    reject.status = 'Rejected'
    reject.save()
    return redirect('/vendor_checkout')


def delivery_checkout(request, id):
    delivery = Orders.objects.get(id=id)
    delivery.status = 'Delivered'
    delivery.save()
    return redirect('/vendor_checkout')


def vendor_cart_products(request, id):
    order_products = Order_Products.objects.filter(order_id=id)
    return render(request, "vendor_cart_products.html", {"order_products": order_products})


def vendor_checkout(request):
    order = Orders.objects.all()
    return render(request, "vendor_checkout.html", {"order": order})


def customer_orders(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customer_view_cart')
        return render(request, "customer_orders.html", {})
    return render(request, "customer_orders.html", {})


def order_products(request):
    if request.method == 'POST':
        form = Order_ProductsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customer_orders')
        return render(request, "order_products.html", {})
    return render(request, "order_products.html", {})


def admin(request):
    if request.method == 'POST':
        form = AdminForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_login')
        return render(request, "admin.html", {})
    return render(request, "admin.html", {})


def add_preference(request):
    email = request.session["email"]
    category = Category.objects.all()

    if request.method == "POST":
        form = My_PreferenceForm(request.POST)
        print(form.errors)
        if form.is_valid():
            form.save()
            return render(request, "add_preference.html", {"msg": "Submitted Preference Form"})

        return render(request, "add_preference.html", {"msg": "Not Submitted Preference Form"})
    return render(request, "add_preference.html", {"email": email, "category": category})


def my_preference(request):
    email = request.session['email']
    preferences = My_Preference.objects.filter(email=email)
    profile = []
    for preference in preferences:
        products = Product.objects.filter(category=preference.category)
        profile.extend(products)

    return render(request, "my_preference.html", {"profile": profile})


def customer_view_cart_edit(request, id):
    cate = Cart.objects.get(id=id)
    return render(request, "customer_view_cart_edit.html", {"cate": cate})


def customer_view_cart_update(request):
    if request.method == "POST":
        print("error:")
        id = request.POST["id"]
        print("hello")
        user = Cart.objects.get(id=id)
        users = CartForm(request.POST, instance=user)
        print("error:", users.errors)
        if users.is_valid():
            print("error:", users.errors)
            users.save()
            return redirect('/view_cart')
        return render(request, "customer_view_cart.html", {"msg": "not update"})
    return redirect("/customer_view_cart")


def vendor_view_orders(request):
    email = request.session['email']
    orders = Orders.objects.filter(vendor_email=email)
    return render(request, "vendor_view_orders.html", {"orders": orders})


def vendor_view_orders_products(request, id):
    orders = Orders.objects.get(id=id)
    order_products = Order_Products.objects.filter(order_id=orders.id)
    return render(request, "vendor_view_orders_products.html", {"order_products": order_products})


def accept_order(request, id):
    orders = Orders.objects.get(id=id)
    orders.status = 'Accepted'
    orders.save()
    return redirect('/vendor_view_orders')


def reject_order(request, id):
    orders = Orders.objects.get(id=id)
    orders.status = 'Rejected'
    orders.save()
    return redirect('/vendor_view_orders')


def cancel_order(request, id):
    orders = Orders.objects.get(id=id)
    orders.status = 'Cancelled'
    orders.save()
    return redirect('//my_orders')


def search(request):
    queryval = request.POST["profile"]
    profile = Product.objects.filter(category__contains=queryval)
    return render(request, "customer_view_product.html", {"profile": profile})


def all_users(request):
    email = request.session['email']
    customers = Customer.objects.exclude(email=email)

    # Sent and received requests
    sent_requests = Friends_Requests.objects.filter(from_email=email)
    received_requests = Friends_Requests.objects.filter(to_email=email)

    # Requested and accepted requests
    requested_ids = list(sent_requests.values_list('to_email', flat=True)) + list(
        received_requests.values_list('from_email', flat=True))

    # Friends list (accepted requests)
    accepted_requests = Friends_Requests.objects.filter(
        (Q(from_email=email) | Q(to_email=email)), status='Accepted'
    ).values_list('from_email', 'to_email')

    friends_ids = [req[0] if req[1] == email else req[1] for req in accepted_requests]

    return render(request, 'all_users.html', {
        "customers": customers,
        "requested_ids": requested_ids,
        "friends_ids": friends_ids
    })


def customer_add_review(request, id):
    email = request.session["email"]
    profile = Product.objects.get(id=id)
    if request.method == "POST":
        form = ReviewForm(request.POST)
        print(form.errors)
        if form.is_valid():
            form.save()
            return render(request, "customer_add_review.html", {'msg': 'Review Added Successfully '})
        return render(request, "customer_add_review.html", {})
    return render(request, 'customer_add_review.html', {"email": email, "profile": profile})


def customer_view_review(request, id):
    profile = Product.objects.get(id=id)
    reviews = Review.objects.filter(orders_id=profile.id)
    return render(request, 'customer_view_review.html', {"reviews": reviews})



def add_friends_requests(request, id):
    if request.method == "POST":
        email = request.session['email']
        customer = get_object_or_404(Customer, id=id)

        # Check if request already exists
        if Friends_Requests.objects.filter(from_email=email, to_email=customer.email).exists():
            return JsonResponse({"msg": "Request Already Sent"}, status=400)

        # Create friend request
        Friends_Requests.objects.create(
            customers=customer,
            from_email=email,
            to_email=customer.email
        )
        return JsonResponse({"msg": "Friend Request Sent"}, status=200)

    return JsonResponse({"msg": "Invalid Request"}, status=400)


def view_friends_requests(request):
    email = request.session['email']
    requests = Friends_Requests.objects.filter(to_email=email)
    return render(request,'view_friends_requests.html',{"requests":requests})



def accept_request(request,id):
    requests = Friends_Requests.objects.get(id=id)
    requests.status='Accepted'
    requests.save()
    return redirect("/view_friends_requests")

def reject_request(request, id):
    requests = Friends_Requests.objects.get(id=id)
    requests.status='Rejected'
    requests.save()
    return redirect("/view_friends_requests")

def my_friends(request):
    email = request.session['email']
    sent_friends = Friends_Requests.objects.filter(from_email=email, status='Accepted')
    received_friends = Friends_Requests.objects.filter(to_email=email,status='Accepted')

    return render(request, "my_friends.html",{
        "sent_friends": sent_friends,
        "received_friends": received_friends
    })



def post(request):
    email = request.session['email']
    if request.method == "POST":
        form = PostForm(request.POST,request.FILES)
        print(form.errors)
        if form.is_valid():
            form.save()
            return render(request, "post.html", {"msg": "Thanks For Posting Us"})
        return render(request, "post.html", {"msg": "While Posting Us Your Getting Error"})
    return render(request, "post.html", {"email":email})





def view_post(request):
    email = request.session['email']
    friends_pairs = Friends_Requests.objects.filter(
        (Q(from_email=email) | Q(to_email=email)),
        status='Accepted'
    ).values_list('from_email','to_email')

    friends = set(chain(*friends_pairs)) - {email}

    post = Post.objects.filter(
        Q(posts_for='all') |
        (Q(posts_for = 'friends') & Q(email__in=friends)),
        status='Accepted'
    ).exclude(email=email).annotate(like_count=Count('likes'))

    liked_posts = Likes.objects.filter(customer_email=email).values_list('post_id',flat=True)
    return render(request, "view_post.html", {"post":post,"liked_posts":liked_posts})


def view_all_posts(request):
    email = request.session['email']
    post = Post.objects.filter(email=email)
    return render(request, "view_all_posts.html", {"post":post})

def admin_view_all_posts(request):
    post = Post.objects.all()
    return render(request, "admin_view_all_posts.html", {"post":post})


def accept_all_posts(request,id):
    requests = Post.objects.get(id=id)
    requests.status='Accepted'
    requests.save()
    return redirect("/admin_view_all_posts")



def reject_all_posts(request, id):
    requests = Post.objects.get(id=id)
    requests.status='Rejected'
    requests.save()
    return redirect("/admin_view_all_posts")

def like_post(request, post_id):
    email = request.session['email']
    post = get_object_or_404(Post, id=post_id)

    if not Likes.objects.filter(post=post, customer_email=email).exists():
        Likes.objects.create(post=post, customer_email=email, date_time=timezone.now())
        msg = "Liked Successfully"
    else:
        msg = "You've Already Likes This Post"
    return redirect('/view_post')



def comment(request, id):
    email = request.session["email"]
    profile = Post.objects.get(id=id)
    comments = Comment.objects.filter(post_id_id=profile.id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        print(form.errors)
        if form.is_valid():
            form.save()
            return render(request, "comment.html", {'msg': 'Comment Added Successfully ',"comments":comments})
        return render(request, "comment.html", {"comments":comments})
    return render(request, 'comment.html', {"email": email, "profile": profile,"comments":comments})


