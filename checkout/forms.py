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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'remove-form-style'
