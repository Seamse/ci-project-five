from django import forms
from . import models


class CheckoutForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = models.GenerateOrder
        fields = [
            'first_name', 'last_name', 'email',
            'street_address1', 'street_address2',
            'postcode', 'town_or_city', 'country'
            ]
