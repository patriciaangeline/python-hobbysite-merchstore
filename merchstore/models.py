from django.db import models
from django.urls import reverse
from user_management.models import Profile

class ProductType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Product Type'
        verbose_name_plural = 'Product Types'


class Product(models.Model):
    name = models.CharField(max_length=255)
    productType = models.ForeignKey(
        ProductType, 
        null=True,
        on_delete=models.SET_NULL, 
        related_name='products'
    )
    owner = models.ForeignKey(
        Profile,
        null=True,
        on_delete=models.CASCADE,
        related_name='users'
    )
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(null=True)

    class ProductStatus(models.TextChoices):
        AVAILABLE = 'Available'
        ON_SALE = 'On Sale'
        OUT_OF_STOCK = 'Out of Stock'

    status = models.CharField(
        max_length=100,
        choices=ProductStatus.choices,
        default=ProductStatus.AVAILABLE
    )

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('merchstore:product_detail', args=[self.pk])
    
    class Meta: 
        ordering = ['name']


class Transaction(models.Model): 
    buyer = models.ForeignKey(
        Profile, 
        null=True,
        on_delete=models.SET_NULL
    )
    product = models.ForeignKey(
        Product, 
        null=True,
        on_delete=models.SET_NULL
    )
    amount = models.IntegerField(null=True)

    class TransactionStatus(models.TextChoices):
        ON_CART = 'On Cart'
        TO_PAY = 'To Pay'
        TO_SHIP = 'To Ship'
        TO_RECEIVE = 'To Receive'
        DELIVERED = 'Delivered'

    status = models.CharField(
        max_length=100,
        choices=TransactionStatus.choices
    )
    createdOn = models.DateTimeField(auto_now_add=True, null=True)