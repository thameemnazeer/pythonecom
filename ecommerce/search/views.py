from django.db.models import Q
from django.shortcuts import render

from shop.models import Product


# Create your views here.
def search(request):
    p=None
    query=''
    if(request.method=='POST'):
        s=request.POST.get('q')
        if s:
            p=Product.objects.filter(Q(name__icontains=s)|Q(desc__icontains=s))
            print(p)
    return render(request,'search.html',{'p':p,'query':query})


