"""
URL configuration for social_media_ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from social_media_ecommerce_app import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name="index"),
    path('doctor',views.doctor,name="doctor"),
    path('contact', views.contact, name="contact"),
    path('departments', views.departments, name="departments"),
    path('department', views.department_single, name="department"),
    path('blog', views.blog, name="blog"),
    path('blogs', views.blog_single, name="blogs"),
    path('about', views.about, name="about"),
    path('customerlogin',views.customer_login, name="customerlogin"),
    path('customer_register_form',views.customer_register_form,name="customer_register_form"),
    path('customer_home',views.customer_home,name="customer_home"),
    path('customer_profile',views.customer_profile,name="customer_profile"),
    path('customer_logout',views.customer_logout,name="customer_logout"),
    path('admin_login',views.admin_login,name="admin_login"),
    path('admin_home',views.admin_home,name="admin_home"),
    path('admin_Logout',views.admin_Logout,name="admin_Logout"),
    path('admin_viewcontact',views.admin_viewcontact,name="admin_viewcontact"),
    path('admin_viewcustomer',views.admin_viewcustomer,name="admin_viewcustomer"),
    path('accept_customer/<int:id>',views.accept_customer,name="accept_customer"),
    path('reject_customer/<int:id>', views.reject_customer, name="reject_customer"),
    path('customer_edit',views.customer_edit,name="customer_edit"),
    path('update',views.update,name="update"),
    path('customer_change_password',views.customer_change_password,name="customer_change_password"),
    path('deactivate/<int:id>', views.deactivate, name="deactivate"),
    path('admin_change_password', views.admin_change_password, name="admin_change_password"),
    path('vendor_login', views.vendor_login, name="vendor_login"),
    path('vendor_register_form', views.vendor_register_form, name="vendor_register_form"),
    path('vendor_home', views.vendor_home, name="vendor_home"),
    path('vendor_profile', views.vendor_profile, name="vendor_profile"),
    path('vendor_logout', views.vendor_logout, name="vendor_logout"),
    path('vendor_view_customer',views.vendor_view_customer,name="vendor_view_customer"),
    path('accept_vendor/<int:id>',views.accept_vendor,name="accept_vendor"),
    path('reject_vendor/<int:id>', views.reject_vendor, name="reject_vendor"),
    path('vendor_edit',views.vendor_edit,name="vendor_edit"),
    path('vendor_update',views.vendor_update,name="vendor_update"),
    path('vendor_change_password',views.vendor_change_password,name="vendor_change_password"),
    path('deactivate_vendor/<int:id>', views.deactivate_vendor, name="deactivate_vendor"),
    path('add_notification',views.add_notification,name="add_notification"),
    path('view_notification', views.view_notification, name="view_notification"),
    path('add_category/', views.add_category, name="add_category"),
    path('view_category', views.view_category, name="view_category"),
    path('view_vendor', views.view_vendor, name="view_vendor"),
    path('delete_view_notification/<int:id>',views.delete_view_notification, name="delete_view_notification"),
    path('delete_view_category/<int:id>', views.delete_view_category, name="delete_view_category"),
    path('add_product', views.add_product, name="add_product"),
    path('view_product', views.view_product, name="view_product"),
    path('customer_view_product', views.customer_view_product, name="customer_view_product"),
    path('delete_view_product/<int:id>', views.delete_view_product, name="delete_view_product"),
    path('product_edit/<int:id>', views.product_edit, name="product_edit"),
    path('product_update', views.product_update, name="product_update"),
    path('add_to_cart/<int:id>', views.add_to_cart, name="add_to_cart"),
    path('view_cart', views.view_cart, name="view_cart"),
    path('delete_view_cart/<int:id>', views.delete_view_cart, name="delete_view_cart"),
    path('customer_view_vendors', views.customer_view_vendors, name="customer_view_vendors"),
    path('customer_view_notification', views.customer_view_notification, name="customer_view_notification"),
    # path('customer_view_cart', views.customer_view_cart, name="customer_view_cart"),
    path('checkout', views.checkout, name="checkout"),
    path('edit_item', views.edit_item, name="edit_item"),
    path('edit_item_update', views.edit_item_update, name="edit_item_update"),
    path('remove_item', views.remove_item, name="remove_item"),
    path('cancel_order', views.cancel_order, name="cancel_order"),
    path('customer_checkout', views.customer_checkout, name="customer_checkout"),
    path('customer_cart_products', views.customer_cart_products, name="customer_cart_products"),
    path('accept_checkout', views.accept_checkout, name="accept_checkout"),
    path('reject_checkout', views.reject_checkout, name="reject_checkout"),
    path('delivery_checkout', views.delivery_checkout, name="delivery_checkout"),
    path('vendor_cart_products', views.vendor_cart_products, name="vendor_cart_products"),
    path('vendor_checkout', views.vendor_checkout, name="vendor_checkout"),
    path('customer_orders', views.customer_orders, name="customer_orders"),
    path('order_products', views.order_products, name="order_products"),
    path('admin', views.admin, name="admin"),
    path('add_preference', views.add_preference, name="add_preference"),
    path('my_preference', views.my_preference, name="my_preference"),
    path('customer_view_cart_edit/<int:id>', views.customer_view_cart_edit, name="customer_view_cart_edit"),
    path('customer_view_cart_update', views.customer_view_cart_update, name="customer_view_cart_update"),
    path('my_orders', views.my_orders, name="my_orders"),
    path('my_orders_products/<int:id>', views.my_orders_products, name="my_orders_products"),
    path('vendor_view_orders', views.vendor_view_orders, name="vendor_view_orders"),
    path('vendor_view_orders_products/<int:id>', views.vendor_view_orders_products, name="vendor_view_orders_products"),
    path('accept_order/<int:id>', views.accept_order, name="accept_order"),
    path('reject_order/<int:id>', views.reject_order, name="reject_order"),
    path('cancel_order/<int:id>', views.cancel_order, name="cancel_order"),
    path('search', views.search, name="search"),
    path('all_users', views.all_users, name="all_users"),
    path('customer_add_review/<int:id>', views.customer_add_review, name="customer_add_review"),
    path('customer_view_review/<int:id>', views.customer_view_review, name="customer_view_review"),
    path('add_friends_requests/<int:id>', views.add_friends_requests, name='add_friends_requests'),
    path('view_friends_requests', views.view_friends_requests, name="view_friends_requests"),
    path('accept_request/<int:id>', views.accept_request, name="accept_request"),
    path('reject_request/<int:id>', views. reject_request, name="reject_request"),
    path('my_friends', views.my_friends, name="my_friends"),
    path('post', views.post, name="post"),
    path('view_post', views.view_post, name="view_post"),
    path('view_all_posts', views.view_all_posts, name="view_all_posts"),
    path('admin_view_all_posts', views.admin_view_all_posts, name="admin_view_all_posts"),
    path('accept_all_posts/<int:id>', views.accept_all_posts, name="accept_all_posts"),
    path('reject_all_posts/<int:id>', views.reject_all_posts, name="reject_all_posts"),

    path('like_post/<int:post_id>', views.like_post, name='like_post'),
    path('comment/<int:id>', views.comment, name="comment")

]


if settings.DEBUG:  # new
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

