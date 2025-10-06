from django.urls import path
from . import views

app_name = 'support'

urlpatterns = [
    # Support pages
    path('', views.support_home, name='support_home'),
    path('faq/', views.faq, name='faq'),
    path('size-guide/', views.size_guide, name='size_guide'),
    path('shipping/', views.shipping_info, name='shipping_info'),
    path('returns/', views.returns_policy, name='returns_policy'),
    path('care-guide/', views.care_guide, name='care_guide'),
    
    # Legal pages
    path('privacy/', views.privacy_policy, name='privacy_policy'),
    path('terms/', views.terms_conditions, name='terms_conditions'),
    path('refund/', views.refund_policy, name='refund_policy'),
    
    # Contact and support
    path('contact/', views.contact_form, name='contact_form'),
    path('live-chat/', views.live_chat, name='live_chat'),
]
