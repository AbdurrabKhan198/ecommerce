from django import forms
from django.core.validators import EmailValidator
from .models import Review


class ContactForm(forms.Form):
    """Contact form"""
    SUBJECT_CHOICES = [
        ('general', 'General Inquiry'),
        ('order', 'Order Support'),
        ('product', 'Product Question'),
        ('returns', 'Returns & Exchange'),
        ('size', 'Size Guide Help'),
        ('complaint', 'Complaint'),
        ('suggestion', 'Suggestion'),
        ('partnership', 'Partnership'),
        ('other', 'Other'),
    ]
    
    PRIORITY_CHOICES = [
        ('normal', 'Normal'),
        ('urgent', 'Urgent'),
    ]
    
    CONTACT_METHOD_CHOICES = [
        ('email', 'Email'),
        ('phone', 'Phone'),
        ('whatsapp', 'WhatsApp'),
    ]
    
    full_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your full name'
        })
    )
    
    email = forms.EmailField(
        validators=[EmailValidator()],
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email address'
        })
    )
    
    phone_number = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your phone number'
        })
    )
    
    subject = forms.ChoiceField(
        choices=SUBJECT_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    order_number = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Order number (if applicable)'
        })
    )
    
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'Please provide details about your inquiry'
        })
    )
    
    priority = forms.ChoiceField(
        choices=PRIORITY_CHOICES,
        initial='normal',
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    preferred_contact_method = forms.ChoiceField(
        choices=CONTACT_METHOD_CHOICES,
        initial='email',
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )


class ReviewForm(forms.ModelForm):
    """Product review form"""
    class Meta:
        model = Review
        fields = ['rating', 'title', 'comment']
        widgets = {
            'rating': forms.Select(
                choices=[(i, f'{i} Star{"s" if i != 1 else ""}') for i in range(1, 6)],
                attrs={'class': 'form-control'}
            ),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Review title'
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Share your experience with this product'
            })
        }


class ProductFilterForm(forms.Form):
    """Product filter form"""
    SORT_CHOICES = [
        ('featured', 'Featured'),
        ('newest', 'Newest'),
        ('price_low', 'Price: Low to High'),
        ('price_high', 'Price: High to Low'),
        ('rating', 'Customer Rating'),
    ]
    
    FABRIC_CHOICES = [
        ('', 'All Fabrics'),
        ('cotton', 'Cotton'),
        ('silk', 'Silk'),
        ('polyester', 'Polyester'),
        ('viscose', 'Viscose'),
        ('net', 'Net'),
        ('cotton_blend', 'Cotton Blend'),
        ('other', 'Other'),
    ]
    
    OCCASION_CHOICES = [
        ('', 'All Occasions'),
        ('casual', 'Casual'),
        ('formal', 'Formal'),
        ('party', 'Party'),
        ('traditional', 'Traditional'),
        ('work', 'Work'),
        ('sports', 'Sports'),
    ]
    
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search products...'
        })
    )
    
    category = forms.CharField(required=False)
    subcategory = forms.CharField(required=False)
    
    min_price = forms.DecimalField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Min price'
        })
    )
    
    max_price = forms.DecimalField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Max price'
        })
    )
    
    fabric = forms.ChoiceField(
        required=False,
        choices=FABRIC_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    occasion = forms.ChoiceField(
        required=False,
        choices=OCCASION_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    sort = forms.ChoiceField(
        choices=SORT_CHOICES,
        initial='featured',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
