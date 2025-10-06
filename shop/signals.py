from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import ProductImage, Product


@receiver(post_save, sender=ProductImage)
def update_product_updated_at(sender, instance, **kwargs):
    """Update product's updated_at when image is added/modified"""
    instance.product.save(update_fields=['updated_at'])


@receiver(post_delete, sender=ProductImage)
def update_product_on_image_delete(sender, instance, **kwargs):
    """Update product's updated_at when image is deleted"""
    if instance.product:
        instance.product.save(update_fields=['updated_at'])
