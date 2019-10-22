from django.shortcuts import render
from django.views.generic.detail import DetailView  # t17.
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.paginator import Paginator  # t22
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin  # t23
from django.contrib import messages  # t23
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import City  # импортируем нашу модель с .models
# from .forms import HtmlForm  # t18
from .forms import CityForm  # t19


def home(request):
    # следующие строки заполненные в t18
    # if request.method == 'POST':
    #     form = CityForm(request.POST or None)
    #     if form.is_valid():
    #         print(form.cleaned_data)
    # form = CityForm()
    # # -----------------------------------t18
    # city = request.POST.get('name')  # t18
    # print(city)

    # https://docs.djangoproject.com/en/2.2/topics/pagination/
    cities = City.objects.all()  # сделали запросна получение всех записей из бызы данных
    paginator = Paginator(cities, 10)  # t22
    page = request.GET.get('page')
    cities = paginator.get_page(page)
    return render(request, 'cities/home.html', {'object_list': cities})


class CityDetailView(DetailView):
    queryset = City.objects.all()  # t17 обязательный параметр, это
    # все записи в моделе
    context_object_name = 'object'  # t17 параметр, определяющий с каким
    # именем мы будем отправлять наши данные как контекст для рендер
    template_name = 'cities/details.html'  # адрес нашего шаблона

    # def get_queryset(self):
    #     return City.objects.all()

    # def get_object(self, queryset=None):
    #     res = self.get_queryset().filter(id=self.kwargs.get("pk"))
    #     return res


class CityCreateView(SuccessMessageMixin,LoginRequiredMixin, CreateView):  # t19 класс создания новой записи в б/д
    login_url = '/login/'
    model = City
    form_class = CityForm
    template_name = 'cities/create.html'
    success_url = reverse_lazy('city:home')  # атрибут, указывающий на страницу,
    success_message = "Город успешно создан"
    # в случае успешного выполнения


class CityUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):  # t20 класс создания новой записи в б/д
    login_url = '/login/'
    model = City
    form_class = CityForm
    template_name = 'cities/update.html'
    success_url = reverse_lazy('city:home')
    success_message = "Город успешно отредактирован"


class CityDeleteView(LoginRequiredMixin, DeleteView):  # t20 класс создания новой записи в б/д
    login_url = '/login/'
    model = City
    # template_name = 'cities/delete.html'  # Запускаем страницу удаления c подтверждением
    success_url = reverse_lazy('city:home')

    def get(self, request, *args, **kwargs):  # удаляем без страницы подтверждения
        messages.success(request, 'Город успешно удален')
        return self.post(request, *args, **kwargs)