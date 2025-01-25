from django import forms 

from .models import Product, Transaction


class TransactionForm(forms.ModelForm):
    def __init__(self, *args, product=None, **kwargs):
        self.product = product
        super().__init__(*args, **kwargs)

    class Meta: 
        model = Transaction
        fields = ["amount"]

    def validateAmount(self, *args, **kwargs):
        print(args)
        amount = self.cleaned_data.get("amount")
        if amount <= 0:   
            raise forms.ValidationError("You have inputted a negative amount. Please try again.")
        if amount > self.product.stock:
            raise forms.ValidationError("There is not enough stocks of your product. Please try again.")
        return amount


class ProductForm(forms.ModelForm):
    class Meta: 
        model = Product
        exclude = ['owner']


class ProductUpdateForm(forms.ModelForm):
    class Meta: 
        model = Product
        exclude = ['owner']


    