from django.shortcuts import render


def support_home(request):
    """Support home page"""
    context = {
        'page_title': 'Support - Help & Customer Service',
    }
    return render(request, 'support/support_home.html', context)


def faq(request):
    """FAQ page"""
    context = {
        'page_title': 'Frequently Asked Questions - FAQ',
    }
    return render(request, 'support/faq.html', context)


def size_guide(request):
    """Size guide page"""
    context = {
        'page_title': 'Size Guide - Find Your Perfect Fit',
    }
    return render(request, 'support/size_guide.html', context)


def shipping_info(request):
    """Shipping information page"""
    context = {
        'page_title': 'Shipping Information - Delivery Details',
    }
    return render(request, 'support/shipping_info.html', context)


def returns_policy(request):
    """Returns and exchange policy"""
    context = {
        'page_title': 'Returns & Exchange Policy',
    }
    return render(request, 'support/returns_policy.html', context)


def care_guide(request):
    """Clothing care guide"""
    context = {
        'page_title': 'Care Guide - How to Care for Your Garments',
    }
    return render(request, 'support/care_guide.html', context)


def privacy_policy(request):
    """Privacy policy page"""
    context = {
        'page_title': 'Privacy Policy - Your Data Protection',
    }
    return render(request, 'support/privacy_policy.html', context)


def terms_conditions(request):
    """Terms and conditions page"""
    context = {
        'page_title': 'Terms & Conditions - Legal Information',
    }
    return render(request, 'support/terms_conditions.html', context)


def refund_policy(request):
    """Refund policy page"""
    context = {
        'page_title': 'Refund Policy - Money Back Guarantee',
    }
    return render(request, 'support/refund_policy.html', context)


def contact_form(request):
    """Contact form page"""
    context = {
        'page_title': 'Contact Us - Get in Touch',
    }
    return render(request, 'support/contact_form.html', context)


def live_chat(request):
    """Live chat page"""
    context = {
        'page_title': 'Live Chat - Instant Support',
    }
    return render(request, 'support/live_chat.html', context)
