# все скопировали с urls в корне проекта
# urlы приложения cities

from django.urls import path
from .views import (home, TrainCreateView, TrainDetailView, TrainUpdateView, TrainDeleteView)

urlpatterns = [
    # убрали path admin
    path('', home, name='home'),
    path('detail/<int:pk>/', TrainDetailView.as_view(), name='detail'),
    # #  'detail/<int:pk>/'  - конструкция в урле, переход на сities/detail/ и дальеш
    # #  primary key -  <int:pk>, определяет номер записи в базе данных по порядку
    path('add/', TrainCreateView.as_view(), name='add'),  # t19
    path('update/<int:pk>', TrainUpdateView.as_view(), name='update'),  # t20
    path('delete/<int:pk>', TrainDeleteView.as_view(), name='delete'),  # t20
]