from django.shortcuts import render,get_object_or_404,redirect
from blog.models import Post,Product_detail,checkout_detail
from django.utils import timezone
from blog.forms import PostForm,RegForm,LoginForm,CheckoutForm
from django.shortcuts import redirect
from django.views.generic import View
from django.contrib.auth import login as auth_login,logout
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect
from django.template.context_processors import csrf
from blog.utility import *
from django.urls import reverse 
from django.contrib.auth.models import User
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from blog.serializers import PostSerializer

# Create your views here.

cart_no=0
cart_details={}
cart_Ids=[]
getsum = 0
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts':posts,'cart_no':cart_no,'cart_details':cart_details})

def post_detail(request,pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post,'cart_no':cart_no,'cart_details':cart_details})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form,'cart_no':cart_no,'cart_details':cart_details})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form,'cart_no':cart_no,'cart_details':cart_details})

#class Post_API_list(APIView):
    #def get(self,request):
        #API_posts = Post.objects.all()
        #serializer = PostSerializer(API_posts , many=True)
        #return Response(serializer.data)

    #def post(self):
        #pass

class RegFormview(View):

    def post(self,request):
        form = RegForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            user.set_password(password)
            user.save()
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request=request, user=user)
                return HttpResponseRedirect(reverse('home'))
        msg_to_html = custom_message('Invalid Credentials', TagType.danger)
        dictionary = dict(request=request, messages = msg_to_html)
        dictionary.update(csrf(request))
        return render(request,'blog/post_list.html', dictionary,{'cart_no':cart_no,'cart_details':cart_details})

  
def LoginFormview(request):
     if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request=request, user=user)
            return HttpResponseRedirect(reverse('home'))
        else:
            msg_to_html = custom_message('Invalid Credentials', TagType.danger)
            dictionary = dict(request=request, messages = msg_to_html)
            dictionary.update(csrf(request))
        return render(request,'blog/base.html', dictionary,{'cart_no':cart_no,'cart_details':cart_details})
    
def Logout_view(request):
    logout(request)
    return redirect('home')

def main_base(request):
    dictionary = dict(request=request)
    dictionary.update(csrf(request))
    return render(request,'blog/base.html', dictionary)

def home(request):
    global cart_details
    global cart_no
    global cart_Ids
    cart_no=len(cart_details)
    products = Product_detail.objects.all()
    return render(request,'blog/home.html',{'products':products,'cart_no':cart_no,'cart_details':cart_details,'cart_Ids':cart_Ids})

def cart(request,pk):
    if request.method=='POST':
        global cart_details
        global cart_Ids
        detail =get_object_or_404(Product_detail, pk=pk)
        cart_Ids.append(pk)
        cart_details[detail.details]=request.POST.get("quantity")
        return redirect(reverse('home'))
    
def remove_cart(request,pk):
    if request.method=='POST':
        global cart_details
        global cart_Ids
        detail =get_object_or_404(Product_detail, pk=pk)
        del cart_details[detail.details]
        cart_Ids.remove(pk)
        return redirect(reverse('home'))

def remove_cart_dropdown(request,val):
    if request.method=='POST':
        global cart_details
        global cart_Ids
        detail = get_object_or_404(Product_detail,details=val)
        del cart_details[val]
        cart_Ids.remove(detail.pk)
        return redirect(reverse('home'))

def buy(request):
        global cart_details
        global cart_no
        global cart_Ids
        global getsum
        getsum = 0
        cart_no=len(cart_details)
        products = Product_detail.objects.all()
        for key,value in cart_details.items():
            getp=get_object_or_404(Product_detail, details=key)
            getsum+=int(getp.price)*int(value)
        return render(request,'blog/buy.html',{'products':products,'cart_no':cart_no,'cart_details':cart_details,'cart_Ids':cart_Ids,'getsum':getsum})

def remove_mycart(request,val):
        global cart_details
        global cart_Ids
        global cart_no
        detail = get_object_or_404(Product_detail,details=val)
        products = Product_detail.objects.all()
        del cart_details[val]
        cart_Ids.remove(detail.pk)
        cart_no=len(cart_details)
        return redirect('buy')

def checkout(request):
    global cart_details
    global cart_no
    string = ''
    if request.method == "POST":
        form = CheckoutForm(request.POST)
        for key,value in cart_details.items():
            string+= key + " x " + value + " || "
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.time = timezone.now()
            post.order = string
            post.total = getsum
            post.save()
            cart_no=0
            cart_copy = cart_details
            cart_Ids = []
            return render(request,'blog/done.html',{'name':post.name,'address':post.address,'pincode':post.pincode,'contact':post.contact,'time':post.time,'cart_details':cart_copy,'cart_no':cart_no,'getsum':getsum})
    else:
        form = CheckoutForm()
    return render(request, 'blog/checkout.html', {'form': form,'cart_no':cart_no,'cart_details':cart_details})

def profile(request):
    user = get_object_or_404(User,username=request.user.get_username())
    return render(request,'blog/profile.html',{'email':user.email,'cart_no':cart_no,'cart_details':cart_details})

def my_order(request):
    name = request.user.get_username()
    get = checkout_detail.objects.filter(user__username__exact= name).order_by('time')
    return render(request,'blog/my_order.html',{'prd':get,'cart_no':cart_no,'cart_details':cart_details})

def contact(request):
    return render(request,'blog/contact.html',{'cart_no':cart_no,'cart_details':cart_details})