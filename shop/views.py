from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q, Avg, Count
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json

from .models import (
    Category, SubCategory, Product, ProductVariant, 
    Review, Wishlist, RecentlyViewed
)
from .forms import ContactForm, ReviewForm


def homepage(request):
    """Homepage view"""
    print("Homepage view called!")  # Debug output
    
    # Get sample data for demonstration
    context = {
        'categories': [],
        'featured_products': [],
        'recent_products': [],
        'page_title': 'Premium Women\'s Wear - Leggings, Pants & Dupattas',
        'meta_description': 'Shop premium women\'s leggings, pants & dupattas online. High-quality fabrics, perfect fit guarantee, free shipping above ₹999.',
        'currency_symbol': '₹',
        'free_shipping_threshold': '999',
        'site_name': 'Women\'s Wear Store',
        'support_phone': '+91 9876543210',
        'support_email': 'hello@womenswear.com',
    }
    
    return render(request, 'shop/homepage.html', context)
    # return HttpResponse("""
    # <!DOCTYPE html>
    # <html>
    # <head>
    #     <title>Women's Wear Store</title>
    #     <style>
    #         body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
    #         h1 { color: #e91e63; }
    #         .success { color: #4caf50; font-size: 1.2em; margin: 20px 0; }
    #     </style>
    # </head>
    # <body>
    #     <h1>🛍️ Women's Wear Store</h1>
    #     <div class="success">✅ SUCCESS! Our Django app is working!</div>
    #     <p>The homepage view is now being called correctly.</p>
    #     <p>Our beautiful template will be restored in the next step.</p>
    # </body>
    # </html>
    # """)


def shop(request):
    """All products view with filters"""
    products = Product.objects.filter(is_active=True).select_related(
        'category', 'subcategory'
    ).prefetch_related('images')
    
    # Filter by category
    category_slug = request.GET.get('category')
    if category_slug:
        products = products.filter(category__slug=category_slug)
    
    # Filter by subcategory
    subcategory_slug = request.GET.get('subcategory')
    if subcategory_slug:
        products = products.filter(subcategory__slug=subcategory_slug)
    
    # Filter by price range
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        products = products.filter(selling_price__gte=min_price)
    if max_price:
        products = products.filter(selling_price__lte=max_price)
    
    # Filter by fabric
    fabric = request.GET.get('fabric')
    if fabric:
        products = products.filter(fabric=fabric)
    
    # Filter by occasion
    occasion = request.GET.get('occasion')
    if occasion:
        products = products.filter(occasion=occasion)
    
    # Search
    search_query = request.GET.get('search')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(short_description__icontains=search_query)
        )
    
    # Sorting
    sort_by = request.GET.get('sort', 'featured')
    if sort_by == 'price_low':
        products = products.order_by('selling_price')
    elif sort_by == 'price_high':
        products = products.order_by('-selling_price')
    elif sort_by == 'newest':
        products = products.order_by('-created_at')
    elif sort_by == 'rating':
        products = products.annotate(
            avg_rating=Avg('reviews__rating')
        ).order_by('-avg_rating')
    else:  # featured
        products = products.order_by('-is_featured', '-created_at')
    
    # Pagination
    paginator = Paginator(products, settings.PRODUCTS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get filter options
    categories = Category.objects.filter(is_active=True)
    fabric_choices = Product.FABRIC_CHOICES
    occasion_choices = Product.OCCASION_CHOICES
    
    context = {
        'page_obj': page_obj,
        'products': page_obj.object_list,
        'categories': categories,
        'fabric_choices': fabric_choices,
        'occasion_choices': occasion_choices,
        'current_filters': request.GET,
        'page_title': 'Shop Women\'s Wear - All Products',
    }
    return render(request, 'shop/shop.html', context)


def category_view(request, category_slug):
    """Category view"""
    category = get_object_or_404(Category, slug=category_slug, is_active=True)
    subcategories = category.subcategories.filter(is_active=True)
    
    products = Product.objects.filter(
        category=category, 
        is_active=True
    ).select_related('subcategory').prefetch_related('images')
    
    # Apply filters (similar to shop view)
    # ... (filter logic same as shop view)
    
    # Pagination
    paginator = Paginator(products, settings.PRODUCTS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'subcategories': subcategories,
        'page_obj': page_obj,
        'products': page_obj.object_list,
        'page_title': f'{category.meta_title or category.name}',
        'meta_description': category.meta_description or category.description[:150],
    }
    return render(request, 'shop/category.html', context)


def subcategory_view(request, category_slug, subcategory_slug):
    """Subcategory view"""
    category = get_object_or_404(Category, slug=category_slug, is_active=True)
    subcategory = get_object_or_404(
        SubCategory, 
        category=category, 
        slug=subcategory_slug, 
        is_active=True
    )
    
    products = Product.objects.filter(
        subcategory=subcategory, 
        is_active=True
    ).prefetch_related('images')
    
    # Apply filters and pagination (similar to category view)
    paginator = Paginator(products, settings.PRODUCTS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'subcategory': subcategory,
        'page_obj': page_obj,
        'products': page_obj.object_list,
        'page_title': f'{subcategory.meta_title or subcategory.name}',
        'meta_description': subcategory.meta_description or subcategory.description[:150],
    }
    return render(request, 'shop/subcategory.html', context)


def product_detail(request, product_slug):
    """Product detail view"""
    product = get_object_or_404(
        Product.objects.select_related('category', 'subcategory').prefetch_related(
            'images', 'variants', 'reviews__user'
        ),
        slug=product_slug,
        is_active=True
    )
    
    # Add to recently viewed
    if request.user.is_authenticated:
        RecentlyViewed.objects.update_or_create(
            user=request.user,
            product=product
        )
    
    # Get reviews
    reviews = product.reviews.filter(is_approved=True).order_by('-created_at')
    reviews_paginator = Paginator(reviews, settings.REVIEWS_PER_PAGE)
    reviews_page = request.GET.get('reviews_page')
    reviews_page_obj = reviews_paginator.get_page(reviews_page)
    
    # Get related products
    related_products = Product.objects.filter(
        subcategory=product.subcategory,
        is_active=True
    ).exclude(id=product.id).prefetch_related('images')[:4]
    
    # Check if in wishlist
    in_wishlist = False
    if request.user.is_authenticated:
        in_wishlist = Wishlist.objects.filter(
            user=request.user, 
            product=product
        ).exists()
    
    context = {
        'product': product,
        'reviews_page_obj': reviews_page_obj,
        'related_products': related_products,
        'in_wishlist': in_wishlist,
        'review_form': ReviewForm(),
        'page_title': f'{product.meta_title or product.name}',
        'meta_description': product.meta_description or product.short_description,
    }
    return render(request, 'shop/product_detail.html', context)


def search(request):
    """Search view"""
    query = request.GET.get('q', '')
    products = Product.objects.none()
    
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(short_description__icontains=query) |
            Q(category__name__icontains=query) |
            Q(subcategory__name__icontains=query),
            is_active=True
        ).select_related('category', 'subcategory').prefetch_related('images')
    
    paginator = Paginator(products, settings.PRODUCTS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'query': query,
        'page_obj': page_obj,
        'products': page_obj.object_list,
        'page_title': f'Search Results for "{query}"' if query else 'Search',
    }
    return render(request, 'shop/search.html', context)


def about(request):
    """About us view"""
    context = {
        'page_title': 'About Us - Our Story of Fashion & Quality',
        'meta_description': 'Learn about our journey to create premium women\'s fashion. Quality leggings, pants & dupattas. Customer-focused brand.',
    }
    return render(request, 'shop/about.html', context)


def contact(request):
    """Contact us view"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Save contact form data or send email
            messages.success(request, 'Thank you for your message. We\'ll get back to you soon!')
            return redirect('shop:contact')
    else:
        form = ContactForm()
    
    context = {
        'form': form,
        'page_title': 'Contact Us - We\'re Here to Help!',
        'meta_description': 'Get help with orders, returns, size guide & more. 24/7 support available.',
    }
    return render(request, 'shop/contact.html', context)


@login_required
@require_POST
def add_to_wishlist(request):
    """Add product to wishlist via AJAX"""
    try:
        data = json.loads(request.body)
        product_id = data.get('product_id')
        product = get_object_or_404(Product, id=product_id, is_active=True)
        
        wishlist_item, created = Wishlist.objects.get_or_create(
            user=request.user,
            product=product
        )
        
        return JsonResponse({
            'success': True,
            'added': created,
            'message': 'Added to wishlist' if created else 'Already in wishlist'
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
@require_POST
def remove_from_wishlist(request):
    """Remove product from wishlist via AJAX"""
    try:
        data = json.loads(request.body)
        product_id = data.get('product_id')
        
        Wishlist.objects.filter(
            user=request.user,
            product_id=product_id
        ).delete()
        
        return JsonResponse({
            'success': True,
            'message': 'Removed from wishlist'
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


def product_quick_view(request):
    """Product quick view via AJAX"""
    product_id = request.GET.get('product_id')
    if not product_id:
        return JsonResponse({'success': False, 'error': 'Product ID required'})
    
    try:
        product = get_object_or_404(
            Product.objects.prefetch_related('images', 'variants'),
            id=product_id,
            is_active=True
        )
        
        # Render partial template
        html = render(request, 'shop/partials/product_quick_view.html', {
            'product': product
        }).content.decode('utf-8')
        
        return JsonResponse({
            'success': True,
            'html': html
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
