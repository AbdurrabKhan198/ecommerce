from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from PIL import Image
import os

User = get_user_model()


class Category(models.Model):
    """Main product categories: Leggings, Pants, Dupattas"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField()
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.TextField(max_length=300, blank=True)
    image = models.ImageField(upload_to='categories/', blank=True)
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['sort_order', 'name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:category', kwargs={'category_slug': self.slug})


class SubCategory(models.Model):
    """Sub-categories like Ankle Length, Palazzos, Cotton, etc."""
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    description = models.TextField()
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.TextField(max_length=300, blank=True)
    image = models.ImageField(upload_to='subcategories/', blank=True)
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Sub Categories"
        ordering = ['sort_order', 'name']
        unique_together = ['category', 'slug']

    def __str__(self):
        return f"{self.category.name} - {self.name}"

    def get_absolute_url(self):
        return reverse('shop:subcategory', kwargs={
            'category_slug': self.category.slug,
            'subcategory_slug': self.slug
        })


class Product(models.Model):
    """Main product model"""
    FABRIC_CHOICES = [
        ('cotton', 'Cotton'),
        ('silk', 'Silk'),
        ('polyester', 'Polyester'),
        ('viscose', 'Viscose'),
        ('net', 'Net'),
        ('cotton_blend', 'Cotton Blend'),
        ('other', 'Other'),
    ]

    OCCASION_CHOICES = [
        ('casual', 'Casual'),
        ('formal', 'Formal'),
        ('party', 'Party'),
        ('traditional', 'Traditional'),
        ('work', 'Work'),
        ('sports', 'Sports'),
    ]

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField()
    short_description = models.TextField(max_length=500)
    
    # Product details
    fabric = models.CharField(max_length=20, choices=FABRIC_CHOICES)
    occasion = models.CharField(max_length=20, choices=OCCASION_CHOICES)
    care_instructions = models.TextField()
    
    # Pricing
    mrp = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Inventory
    stock_quantity = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    is_bestseller = models.BooleanField(default=False, help_text="Show in Bestsellers This Week section")
    
    # SEO
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.TextField(max_length=300, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', kwargs={'product_slug': self.slug})

    @property
    def discount_percentage(self):
        if self.mrp > self.selling_price:
            return round(((self.mrp - self.selling_price) / self.mrp) * 100)
        return 0

    @property
    def is_in_stock(self):
        return self.stock_quantity > 0

    @property
    def average_rating(self):
        reviews = self.reviews.filter(is_approved=True)
        if reviews:
            return round(sum(review.rating for review in reviews) / len(reviews), 1)
        return 0

    @property
    def review_count(self):
        return self.reviews.filter(is_approved=True).count()


class ProductImage(models.Model):
    """Product images"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')
    alt_text = models.CharField(max_length=200)
    is_primary = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['sort_order']

    def __str__(self):
        return f"{self.product.name} - Image {self.sort_order}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        # Resize image if it's too large
        if self.image:
            img = Image.open(self.image.path)
            if img.height > 800 or img.width > 800:
                output_size = (800, 800)
                img.thumbnail(output_size)
                img.save(self.image.path)


class ProductVariant(models.Model):
    """Product variants for size and color"""
    SIZE_CHOICES = [
        ('XS', 'Extra Small'),
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
        ('XXL', '2XL'),
        ('3XL', '3XL'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    size = models.CharField(max_length=10, choices=SIZE_CHOICES)
    color = models.CharField(max_length=50)
    color_code = models.CharField(max_length=7, blank=True)  # Hex color code
    stock_quantity = models.PositiveIntegerField(default=0)
    additional_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ['product', 'size', 'color']

    def __str__(self):
        return f"{self.product.name} - {self.size} - {self.color}"

    @property
    def is_in_stock(self):
        return self.stock_quantity > 0


class Review(models.Model):
    """Product reviews"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    title = models.CharField(max_length=200)
    comment = models.TextField()
    is_approved = models.BooleanField(default=False)
    is_verified_purchase = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['product', 'user']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.product.name} - {self.rating} stars by {self.user.get_full_name()}"


class Wishlist(models.Model):
    """User wishlist"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlists')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='wishlisted_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'product']

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.product.name}"


class RecentlyViewed(models.Model):
    """Recently viewed products"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recently_viewed')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'product']
        ordering = ['-viewed_at']

    def __str__(self):
        return f"{self.user.get_full_name()} viewed {self.product.name}"


class WhatsAppSubscription(models.Model):
    """WhatsApp subscription model for Indian customers"""
    phone_number = models.CharField(max_length=15, unique=True, help_text="WhatsApp number (e.g., +91 9876543210)")
    name = models.CharField(max_length=100, blank=True, help_text="Customer name (optional)")
    is_active = models.BooleanField(default=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    unsubscribed_at = models.DateTimeField(null=True, blank=True)
    source = models.CharField(max_length=100, default='website', help_text="Where the subscription came from")
    
    class Meta:
        ordering = ['-subscribed_at']
        verbose_name = 'WhatsApp Subscription'
        verbose_name_plural = 'WhatsApp Subscriptions'

    def __str__(self):
        return f"{self.phone_number} - {'Active' if self.is_active else 'Inactive'}"
