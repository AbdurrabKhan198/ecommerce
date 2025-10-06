from django.db import models
from django.contrib.auth import get_user_model
from shop.models import Product, ProductVariant

User = get_user_model()


class Cart(models.Model):
    """Shopping cart model"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart for {self.user.get_full_name()}"

    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())

    @property
    def total_amount(self):
        return sum(item.get_total_price() for item in self.items.all())

    @property
    def is_eligible_for_free_shipping(self):
        from django.conf import settings
        return self.total_amount >= settings.FREE_SHIPPING_THRESHOLD


class CartItem(models.Model):
    """Cart item model"""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['cart', 'product', 'variant']

    def __str__(self):
        variant_info = f" - {self.variant}" if self.variant else ""
        return f"{self.product.name}{variant_info} x {self.quantity}"

    def get_total_price(self):
        price = self.product.selling_price
        if self.variant and self.variant.additional_price:
            price += self.variant.additional_price
        return price * self.quantity

    @property
    def is_in_stock(self):
        if self.variant:
            return self.variant.stock_quantity >= self.quantity
        return self.product.stock_quantity >= self.quantity
