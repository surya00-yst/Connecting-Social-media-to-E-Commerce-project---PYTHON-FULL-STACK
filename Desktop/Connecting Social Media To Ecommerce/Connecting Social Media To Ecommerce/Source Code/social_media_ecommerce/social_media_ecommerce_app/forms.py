from django import forms
from .models import Contact,Customer,Vendor,Notification,Category,Product,Cart,Orders,Order_Products,Admin, My_Preference,Review,Friends_Requests,Post,Likes,Comment
class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = "__all__"
class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = "__all__"
        exclude=['status']
class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = "__all__"
        exclude=['status']
class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = "__all__"
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields= "__all__"
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"
class CartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = "__all__"
class OrderForm(forms.ModelForm):
    class Meta:
        model = Orders
        exclude = ["status"]
class Order_ProductsForm(forms.ModelForm):
    class Meta:
        model = Order_Products
        fields = "__all__"
class AdminForm(forms.ModelForm):
    class Meta:
        model = Admin
        fields = "__all__"


class My_PreferenceForm(forms.ModelForm):
    class Meta:
        model = My_Preference
        fields = "__all__"


class ReviewForm(forms.ModelForm):
    class Meta:
        model =Review
        fields = "__all__"


class Friends_RequestsForm(forms.ModelForm):
    class Meta:
        model =Friends_Requests
        exclude = ["status"]



class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ["status"]


class LikesForm(forms.ModelForm):
    class Meta:
        model = Likes
        fields = "__all__"

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = "__all__"
