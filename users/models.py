from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Review(models.Model):
    """"""

    item = models.ForeignKey(
        'items.ItemDetailPage',
        blank=False,
        null=True,
        on_delete=models.SET_NULL
    )
    user = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.SET_NULL       # When deleting user, set this value to null
    )
    name = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )
    rating = models.IntegerField(
        default=0,
        blank=False,
        null=True,
    )
    comment = models.TextField(
        max_length=2000,
        blank=True,
        null=True
    )

    def __str__(self):
        # @todo make it so incoming objects will always be unique?
        return str( str(self.id) + ' ' + str(self.name) + ' ' + str(self.rating) )



class Cart(models.Model):
    """User cart model."""

    user = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.SET_NULL       # When deleting user, set this value to null
    )
    payment_method = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    shipping_price = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        blank=True,
        null=True
    )
    tax_price = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        blank=True,
        null=True
    )
    total_price = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        blank=True,
        null=True
    )
    is_paid = models.BooleanField(
        default=False,
        blank=True,
        null=True
    )
    paid_at = models.DateTimeField(
        auto_now_add=False,
        blank=True,
        null=True
    )
    is_delivered = models.BooleanField(
        default=False,
        blank=True,
        null=True
    )
    delivered_at = models.DateTimeField(
        auto_now_add=False,
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(
        default=timezone.now,
    )

    def __str__(self):
        return str( str(self.id) + ' ' + str(self.user) + ' ' + str(self.created_at) )


class Order(models.Model):
    """Order model. Multiple can be connected to a single cart object."""

    item = models.ForeignKey(
        'items.ItemDetailPage',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    image = models.CharField(
        max_length=2000,
        blank=True,
        null=True
    )
    cart = models.ForeignKey(
        'users.Cart',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    name = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )
    quantity = models.IntegerField(
        default=0,
        blank=False,
        null=True,
    )
    price = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        blank=True,
        null=True
    )

    def __str__(self):
        return str( str(self.id) + ' ' + str(self.name) )



class ShippingAddress(models.Model):
    """"""

    cart = models.OneToOneField(
        'users.Cart',
        blank=True,
        null=True,
        on_delete=models.CASCADE  # When a cart is deleted, the shipping address object connected to it will also be removed
    )
    address = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )
    city = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    postal_code = models.CharField(
        max_length=10,
        blank=True,
        null=True
    )
    country = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    shipping_price = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        blank=True,
        null=True
    )

    def __str__(self):
        return str( str(self.id) + ' ' + str(self.address) )