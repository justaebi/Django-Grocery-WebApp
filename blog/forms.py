from django import forms
from django.contrib.auth.models import User
from .models import Post,checkout_detail

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text',)

class RegForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.CharField(widget=forms.EmailInput)
    class Meta:
        model = User
        fields = ['first_name','last_name','email','username','password']

class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username','password']

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = checkout_detail
        fields=('name','address','pincode','contact')
