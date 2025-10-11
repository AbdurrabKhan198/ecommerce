"""
URL configuration for womens_wear_ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shop.urls')),
    path('account/', include('accounts.urls')),
    path('cart/', include('cart.urls')),
    path('checkout/', include('checkout.urls')),
    path('support/', include('support.urls')),
    path('bill/', include('billing.advanced_urls')),
]

# Serve media and static files
if settings.DEBUG:
    # Development: Serve media files
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Development: Serve static files
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
else:
    # Production: Serve static files from collected directory
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    # Production: Media files should be served by web server (nginx/apache)
    # For development/testing, you can still serve media files in production
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
