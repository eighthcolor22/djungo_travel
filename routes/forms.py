from django import forms
from cities.models import City
from .models import Route


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


class RouteModelForm(forms.ModelForm):
    name = forms.CharField(label='Название маршрута', widget=
                           forms.TextInput(attrs={'class': 'Form-control'}))  # открытое поле,
    # название вводит пользователь

    # скрытые поля
    from_city = forms.CharField(widget=forms.HiddenInput())
    to_city = forms.CharField(widget=forms.HiddenInput())
    across_cities = forms.CharField(widget=forms.HiddenInput())
    travel_times = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model = Route
        fields = ('name', 'from_city', 'to_city',
                  'across_cities', 'travel_times'
                  )
