from django.shortcuts import render
from .models import Train
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin  # t23
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import TrainForm

def home(request):
    trains = Train.objects.all()  # сделали запросна получение всех записей из бызы данных
    paginator = Paginator(trains, 10)  # t22
    page = request.GET.get('page')
    trains = paginator.get_page(page)
    return render(request, 'trains/home.html', {'object_list': trains})


class TrainDetailView(DetailView):
    queryset = Train.objects.all()  # t17 обязательный параметр, это
    # все записи в моделе
    context_object_name = 'object'  # t17 параметр, определяющий с каким
    # именем мы будем отправлять наши данные как контекст для рендер
    template_name = 'trains/details.html'  # адрес нашего шаблона


class TrainCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):  # t19 класс создания новой записи в б/д
    login_url = '/login/'
    model = Train
    form_class = TrainForm
    template_name = 'trains/create.html'
    success_url = reverse_lazy('train:home')  # атрибут, указывающий на страницу,
    success_message = "поезд успешно создан!"


class TrainUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):  # t20 класс создания новой записи в б/д
    login_url = '/login/'
    model = Train
    form_class = TrainForm
    template_name = 'trains/update.html'
    success_url = reverse_lazy('train:home')
    success_message = "Поезд успешно отредактирован"


class TrainDeleteView(LoginRequiredMixin, DeleteView):  # t20 класс создания новой записи в б/д
    login_url = '/login/'
    model = Train
    success_url = reverse_lazy('train:home')

    def get(self, request, *args, **kwargs):  # удаляем без страницы подтверждения
        messages.success(request, 'Поезд успешно удален')
        return self.post(request, *args, **kwargs)