from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import ProductType, Product, Transaction
from .forms import TransactionForm, ProductForm, ProductUpdateForm
from user_management.models import Profile


def product_list(request):
    if request.user.is_authenticated:
        user_products = Product.objects.filter(owner__user=request.user)
        exclude_user_products = Product.objects.exclude(owner__user=request.user)

        ctx = {
            "user_products": user_products,
            "exclude_user_products": exclude_user_products
        }
    else: 
        all_products = Product.objects.all()
        ctx = {
            "all_products": all_products
        }
    return render(request, 'product_list.html', ctx)


def product_detail(request, pk):
    product = Product.objects.get(pk=pk)
    transactionForm = TransactionForm()
    if request.method == "POST":
        transactionForm = TransactionForm(request.POST, product=product)
        if transactionForm.is_valid():
            newTransaction = Transaction()
            newTransaction.product = product 
            newTransaction.status = 'On Cart'
            newTransaction.amount = transactionForm.cleaned_data.get('amount')
            if request.user.is_authenticated:
                newTransaction.buyer = request.user.profile 
                product.stock -= newTransaction.amount
                if product.stock == 0:
                    product.status = "Out of Stock"
                product.save()
                newTransaction.save()
                return redirect("merchstore:product_cart")
            else: 
                return redirect("user_management:login")
                
    ctx = {
        "product": product,
        "form": transactionForm
    }
    return render(request, 'product_detail.html', ctx)


@login_required
def product_create(request):
    productForm = ProductForm()
    if request.method == "POST":
        productForm = ProductForm(request.POST)
        if productForm.is_valid():
            product = productForm.save(commit=False)
            currentUser = Profile.objects.get(user=request.user)
            product.owner = currentUser
            product = productForm.save()
            return redirect("merchstore:product_list")
        
    ctx = {
        "form": productForm
    }
    return render(request, 'product_create.html', ctx)


@login_required
def product_update(request, pk):
    updateProduct = get_object_or_404(Product, pk=pk)
    updateForm = ProductUpdateForm(request.POST, instance=updateProduct)
    if request.method == "POST":
        if updateForm.is_valid():
            updateProduct = updateForm.save(commit=False)
            if updateProduct.stock == 0:
                updateProduct.status = "Out of Stock"
            else: 
                updateProduct.status = "Available"
            updateProduct = updateForm.save()
            return redirect("merchstore:product_detail", pk=pk)
    else:
        updateForm = ProductUpdateForm(instance=updateProduct)

    ctx = {
        "form":updateForm,
        "product":updateProduct
    }
    return render(request, 'product_update.html', ctx)


@login_required
def product_cart(request):
    user_transactions_buyer = Transaction.objects.filter(buyer__user=request.user)

    buyer_cart = {}
    for transaction in user_transactions_buyer:
        owner = transaction.product.owner
        if owner not in buyer_cart:
            buyer_cart[owner] = []
        buyer_cart[owner].append(transaction)
    
    ctx = {
        'buyer_cart': buyer_cart
    }
    return render(request, 'product_cart.html', ctx)


@login_required
def transaction_list(request):
    user_transactions_seller = Transaction.objects.filter(product__owner__user=request.user)
    
    transaction_list = {}
    for transaction in user_transactions_seller:
        buyer = transaction.buyer
        if buyer not in transaction_list:
            transaction_list[buyer] = []
        transaction_list[buyer].append(transaction)
    
    ctx = {
        'transaction_list': transaction_list
    }
    return render(request, 'transaction_list.html', ctx)