from django.urls import path
from . import views

urlpatterns = [
path('post_list',views.post_list,name="post_list"),
path('post/<int:pk>/',views.post_detail,name='post_detail'),
path('post/new/', views.post_new, name='post_new'),
path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
path('reg/',views.RegFormview.as_view(),name='Reg'),
path('login/',views.LoginFormview,name='Login'),
path('logout/',views.Logout_view,name='logout'),
path('main_base/',views.main_base,name='main_base'),
path('',views.home,name='home'),
path('cart/<int:pk>/',views.cart,name='cart'),
path('remove_cart/<int:pk>/',views.remove_cart,name='remove_cart'),
path('remove_cart_dropdown/<str:val>/',views.remove_cart_dropdown,name='remove_cart_dropdown'),
path('buy/',views.buy,name='buy'),
path('remove_mycart/<str:val>/',views.remove_mycart,name='remove_mycart'),
path('checkout/',views.checkout,name='checkout'),
path('profile/',views.profile,name='profile'),
path('my_order/',views.my_order,name='my_order'),
path('contact/',views.contact,name='contact')
]