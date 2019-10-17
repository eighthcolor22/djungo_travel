# все скопировали с urls в корне проекта
# urlы приложения cities

from django.urls import path
from .views import (home, CityDetailView, CityCreatView,
                    CityUpdateView, CityDeleteView)  # поменяли на home
# t17 добавили импортирование класса CityDetailView

urlpatterns = [
    # убрали path admin
    path('', home, name='home'),
    path('detail/<int:pk>/', CityDetailView.as_view(), name='detail'),
    #  'detail/<int:pk>/'  - конструкция в урле, переход на сities/detail/ и дальеш
    #  primary key -  <int:pk>, определяет номер записи в базе данных по порядку
    path('add/', CityCreatView.as_view(), name='add'),  # t19
    path('update/<int:pk>', CityUpdateView.as_view(), name='update'),  # t20
    path('delete/<int:pk>', CityDeleteView.as_view(), name='delete'),  # t20
]