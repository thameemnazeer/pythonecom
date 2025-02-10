from itertools import product

from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from shop.models import Category

from shop.models import Product



# Create your views here.
class Home(ListView):
    model = Category
    template_name = 'category.html'
    context_object_name = 'category'

class Categorydetails(DetailView):
    model = Category
    template_name = 'categorydetails.html'
    context_object_name = 'detail'
class Productdetail(DetailView):
    model = Product
    template_name = 'productdetail.html'
    context_object_name = 'detail'






class Register(CreateView):
    template_name = 'register.html'
    model = User
    fields = ['username', 'password', 'last_name', 'first_name']
    success_url = reverse_lazy('shop:home')

    def form_valid(request, form):
        u = form.cleaned_data['username']
        p = form.cleaned_data['password']
        l = form.cleaned_data['last_name']
        f = form.cleaned_data['first_name']
        m = User.objects.create_user(username=u, password=p, last_name=l, first_name=f)
        m.save()
        return redirect('shop:home')


class Login(LoginView):
    template_name = 'login.html'



class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('shop:home')



class Addcat(CreateView):
    model = Category
    fields = ['name','desc','image']
    template_name = 'addcategories.html'
    success_url = reverse_lazy('shop:home')
class Addpro(CreateView):
    model = Product
    fields = ['name', 'desc', 'image','price','stock','category']
    template_name = 'addproducts.html'
    success_url = reverse_lazy('shop:home')


class Addstock(UpdateView):
    model = Product
    template_name = 'addstock.html'
    fields = ['stock']
    # success_url = reverse_lazy('shop:home')
    def get_success_url(self):
        return reverse_lazy('shop:productdetail',kwargs={'pk':self.object.id})