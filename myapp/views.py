from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm,ProductForm
from .models import Products,ProductOut
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib import messages
from django.http import JsonResponse


# Create your views here.

# user logic
# 
# 
@login_required
def dashboard(request):
    if request.method == "POST":
        logout(request)
        return redirect("login")
    return render(request,"user/dashboard.html")

@never_cache
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            return redirect("dashboard")
        else:
            print(form.errors)
    else:
        form = AuthenticationForm()
    return render(request,"user/login.html",{"form":form})

@never_cache
def register(request):
    if request.method =="POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("dashboard")
    else:
        form = RegisterForm()
    return render(request,"user/register.html",{"form":form})

@login_required
def logout_view(request):
    logout(request)
    return redirect("login")


# products logic
# 
# 
@login_required
@never_cache
def register_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            product = Products.objects.filter(name=name).exists()
            if product:
                print("product exists")
                messages.error(request,"product already registered")
            else:
                form.save() 
                messages.success(request,"data saved successfully")
                return redirect("viewProduct")
        else:
            messages.error(request, "There was an error with your form submission.")
    else:
        form = ProductForm()
    return render(request,"product/registerProduct.html",{"form":form})

@never_cache
@login_required
def view_product(request):
    products = Products.objects.all()
    count = products.count()
    totalAmount = sum(product.amount for product in products)
    if request.method == "POST":
        order = request.POST['order']
        products = Products.objects.all().order_by(order)
    else:
        products = Products.objects.all().order_by()
    return render(request,"product/viewProduct.html",{"product":products,"count":count,"totalAmount":totalAmount})

@login_required
@never_cache
def update_product(request,id):
    product = get_object_or_404(Products,id=id)
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect("viewProduct")
    else:
        form = ProductForm(instance=product)
    return render(request,"product/updateProduct.html",{"form":form})

@login_required
@never_cache
def delete_product(request,id):
    product = get_object_or_404(Products, id=id)
    if request.method == "POST":
        product.delete()
        return redirect("viewProduct")
    return redirect("viewProduct")

@login_required
@never_cache
def search(request):
    if request.method == "POST":
        query = request.POST.get('query', '')
        suggestions = list(Products.objects.filter(name__icontains=query).values_list('name',"quantity"))
    return JsonResponse(suggestions, safe=False)

@login_required
@never_cache
def productOut(request):
    context = {}
    if request.method == "POST":
        name_of_product = request.POST.get("soldName")
        quantity_of_product = int(request.POST.get("soldQuantity"))
        try:
            getProduct = Products.objects.get(name=name_of_product)
            if quantity_of_product > getProduct.quantity:
                messages.error(request,"no enough stock")
            else:
                # update quantity
                getProduct.quantity -= quantity_of_product
                getProduct.save()

                ProductOut.objects.create(
                    product_out = getProduct,
                    name = name_of_product,
                    quantityOut = quantity_of_product
                )
                context = {"productData":getProduct}
        except Products.DoesNotExist:
            messages.error(request,"product does not exist")
    return render(request,"sales/productOut.html",context)