from django import forms
from . import models


class CheckoutForm(forms.ModelForm):

    class Meta:
        model = models.NewOrder
        fields = [
            'first_name', 'last_name', 'email',
            'street_address1', 'street_address2',
            'postcode', 'town_or_city', 'country'
            ]
