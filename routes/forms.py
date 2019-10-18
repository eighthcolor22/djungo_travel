from django import forms
from cities.models import City


class RouteForm(forms.Form):
    from_city = forms.ModelChoiceField(
        label='Откуда',
        queryset=City.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control js-example-basic-single'})
        )
    to_city = forms.ModelChoiceField(
        label='Куда',
        queryset=City.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control js-example-basic-single'})
        )
    across_cities = forms.ModelMultipleChoiceField(
        label='Через города',
        queryset=City.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-control js-example-basic-multiple'})
    )
    traveling_time = forms.IntegerField(label='Поезд',
                                        widget=forms.NumberInput(
                                            attrs={'class': 'Form-control',
                                                   'placeholder': 'Время в пути'})
                                        )


