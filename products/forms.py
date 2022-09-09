from django import forms
from .models import Product, Category, Review


class ProductForm(forms.ModelForm):
    """ Form to add or edit products in the store """

    class Meta:
        model = Product
        fields = '__all__'

    image = forms.ImageField(label='Image', required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        friendly_names = [(c.id, c.get_friendly_name()) for c in categories]

        self.fields['category'].choices = friendly_names


class ReviewForm(forms.ModelForm):
    """ Form to review products """

    class Meta:
        model = Review
        fields = ('comment', 'rating')
