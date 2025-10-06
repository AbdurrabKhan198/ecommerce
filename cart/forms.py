from django import forms


class AddToCartForm(forms.Form):
    """Add to cart form"""
    
    product_id = forms.IntegerField(widget=forms.HiddenInput())
    variant_id = forms.IntegerField(required=False, widget=forms.HiddenInput())
    quantity = forms.IntegerField(
        min_value=1,
        initial=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control quantity-input',
            'min': '1',
            'max': '10',
            'style': 'width: 80px;'
        })
    )


class UpdateCartForm(forms.Form):
    """Update cart item form"""
    
    item_id = forms.IntegerField(widget=forms.HiddenInput())
    quantity = forms.IntegerField(
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control quantity-input',
            'min': '0',
            'max': '10',
            'style': 'width: 80px;'
        })
    )
