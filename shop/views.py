from django.http import  JsonResponse
from django.shortcuts import redirect, render
from shop.form import CustomUserForm
from . models import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .models import Catagory, Product
import json
 
 
def home(request):
  products=Product.objects.filter(trending=1)
  return render(request,"index.html",{"products":products})
 
def favviewpage(request):
  if request.user.is_authenticated:
    fav=Favourite.objects.filter(user=request.user)
    return render(request,"fav.html",{"fav":fav})
  else:
    return redirect("/")
 
def remove_fav(request,fid):
  item=Favourite.objects.get(id=fid)
  item.delete()
  return redirect("/favviewpage")
 
 
 
 
def cart_page(request):
  if request.user.is_authenticated:
    cart=Cart.objects.filter(user=request.user)
    return render(request,"cart.html",{"cart":cart})
  else:
    return redirect("/")
 
def remove_cart(request,cid):
  cartitem=Cart.objects.get(id=cid)
  cartitem.delete()
  return redirect("/cart")
 
 
 
def fav_page(request):
   if request.headers.get('x-requested-with')=='XMLHttpRequest':
    if request.user.is_authenticated:
      data=json.load(request)
      product_id=data['pid']
      product_status=Product.objects.get(id=product_id)
      if product_status:
         if Favourite.objects.filter(user=request.user.id,product_id=product_id):
          return JsonResponse({'status':'Product Already in Favourite'}, status=200)
         else:
          Favourite.objects.create(user=request.user,product_id=product_id)
          return JsonResponse({'status':'Product Added to Favourite'}, status=200)
    else:
      return JsonResponse({'status':'Login to Add Favourite'}, status=200)
   else:
    return JsonResponse({'status':'Invalid Access'}, status=200)
 
 
def add_to_cart(request):
   if request.headers.get('x-requested-with')=='XMLHttpRequest':
    if request.user.is_authenticated:
      data=json.load(request)
      product_qty=data['product_qty']
      product_id=data['pid']
      #print(request.user.id)
      product_status=Product.objects.get(id=product_id)
      if product_status:
        if Cart.objects.filter(user=request.user.id,product_id=product_id):
          return JsonResponse({'status':'Product Already in Cart'}, status=200)
        else:
          if product_status.quantity>=product_qty:
            Cart.objects.create(user=request.user,product_id=product_id,product_qty=product_qty)
            return JsonResponse({'status':'Product Added to Cart'}, status=200)
          else:
            return JsonResponse({'status':'Product Stock Not Available'}, status=200)
    else:
      return JsonResponse({'status':'Login to Add Cart'}, status=200)
   else:
    return JsonResponse({'status':'Invalid Access'}, status=200)
 
def logout_page(request):
  if request.user.is_authenticated:
    logout(request)
    messages.success(request,"Logged out Successfully")
  return render(request,'login.html')
 
 
def login_page(request):
  if request.user.is_authenticated:
    return render(request,"pindex.html")
  else:
    if request.method=='POST':
      name=request.POST.get('username')
      pwd=request.POST.get('password')
      user=authenticate(request,username=name,password=pwd)
      if user is not None:
        login(request,user)
        messages.success(request,"Logged in Successfully")
        return render(request,'pindex.html')
      else:
        messages.error(request,"Invalid User Name or Password")
        return redirect("/login")
    return render(request,"login.html")
 
def register(request):
  form=CustomUserForm()
  if request.method=='POST':
    form=CustomUserForm(request.POST)
    if form.is_valid():
      form.save()
      messages.success(request,"Registration Success You can Login Now..!")
      return redirect('/login')
  return render(request,"register.html",{'form':form})
 
 
from django.contrib import messages
from django.shortcuts import redirect

def collections(request):
  catagory=Catagory.objects.all()
  return render(request,"collections.html",{"catagory":catagory})
 
def collectionsview(request,name):
  if(Catagory.objects.filter(name=name,status=1)):
      product=Product.objects.filter(name=name)
      return render(request,"pindex.html",{"product":product,"name":name})
  else:
    messages.warning(request,"No Such Catagory Found")
    return redirect('collections')
 
 
# def product_details(request,cname,pname):
#     if(Catagory.objects.filter(name=cname,status=0)):
#       if(Product.objects.filter(name=pname,status=0)):
#         product=Product.objects.filter(name=pname,status=0).first()
#         return render(request,"product_details.html",{"product":product})
#       else:
#         messages.error(request,"No Such Produtct Found")
#         return redirect('collections')
#     else:
#       messages.error(request,"No Such Catagory Found")
#       return redirect('collections')

# def product_details(request, cname, pname):
#     try:
#         category = Category.objects.get(name=cname, status=0)
#         product = Product.objects.get(category=category, name=pname, status=0)
#         return render(request, "product_details.html", {"product": product})
#     except Category.DoesNotExist:
#         messages.error(request, "No such category found")
#         return redirect('collections')
#     except Product.DoesNotExist:
#         messages.error(request, "No such product found")
#         return redirect('collections')

'''def product_details(request,cname,pname):
    print(cname)
    if(Catagory.objects.filter(name=cname,status=1)):
      if(Product.objects.filter(name=pname,status=1)):
        products=Product.objects.filter(name=pname,status=1).first()
        return render(request,"product_details.html",{"products":products})
      else:
        messages.error(request,"No Such Produtct Found")
        return redirect('collections')
    else:
      messages.error(request,"No Such Catagory Found")
      return redirect('collections')'''

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Catagory, Product

def product_details(request, cname, pname):
    print(cname)  # Debugging statement to print the category name
    if Catagory.objects.filter(name=cname, status=0).exists():
        if Product.objects.filter(name=pname, status=0).exists():
            product = Product.objects.filter(name=pname, status=0).first()
            return render(request, "product_details.html", {"product": product})
        else:
            messages.error(request, "No such product found")
            return redirect('collections')
    else:
        messages.error(request, "No such category found")
        return redirect('collections')


