from django.contrib import admin
from .models import City
# импортировали класс City,

admin.site.register(City)  # регистрируем модель City
