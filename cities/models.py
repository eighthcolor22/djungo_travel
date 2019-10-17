from django.db import models


# Create your models here.
class City(models.Model):  # таблица для хранения городов
    name = models.CharField(max_length=100, unique=True, verbose_name='Город')
    # max_length - обязательно, unique=True параметр, указывающий на уникальность названия
    # verbose_name= 'Город' - параметр для переименования конкретного поля(видно его при добавлении
    # нового объекта http://127.0.0.1:8000/admin/cities/city/add/

    def __str__(self):  # функция определения
        # присваевает конкретному City object конкретное название с таблицы
        return self.name

    class Meta:  # класс для названия таблицы при оторбражении на
        # http://127.0.0.1:8000/admin/
        # http://127.0.0.1:8000/admin/cities/city/
        verbose_name = 'Город'  # применяется для всей таблицы(в единственном числе)
        verbose_name_plural = 'Города'  # в множественном числе
        ordering = ['name']  # сортировка

