"""
URL configuration for ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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

from cart import views
from django.urls import path

app_name = "cart"
urlpatterns = [
    path('addtocart/<int:i>/', views.addtocart, name='addtocart'),
    path('cartview', views.cartview, name='cartview'),
    path('cartdecrement/<int:i>/', views.cart_decrement, name="cartdecrement"),
    path('cartdelete/<int:i>/', views.cart_delete, name="cartdelete"),
    path('orderform', views.order_form, name='orderform'),
    path('payment', views.order_form, name='payment'),
    path('status/<str:i>/', views.status, name='status'),
    path('orders', views.orders, name='orders'),

]
