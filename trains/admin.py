from django.contrib import admin
from .models import Train
# Register your models here.


class TrainAdmin(admin.ModelAdmin):
    class Meta:
        model = Train
    list_display = ('name', 'from_city', 'travel_time')
    list_editable = ['travel_time']


admin.site.register(Train, TrainAdmin)

