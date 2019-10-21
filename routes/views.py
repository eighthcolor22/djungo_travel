from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from .forms import *
from trains.models import Train



def home(request):
    form = RouteForm()
    return render(request, 'routes/home.html', {'form': form})


def dfs_paths(graph, start, goal):
    """Функция поиска всех возможных маршрутов
       из одного города в другой. Вариант посещения
       одного и того же города более одного раза,
        не рассматривается.
    """
    stack = [(start, [start])]
    while stack:
        (vertex, path) = stack.pop()
        if vertex in graph.keys():
            for next_ in graph[vertex] - set(path):
                if next_ == goal:
                    yield path + [next_]
                else:
                    stack.append((next_, path + [next_]))


def get_graph():  # функция составляет граф со всех наших маршрутов
    qs = Train.objects.values('from_city')
    # print(qs)
    from_city_set = set(i['from_city'] for i in qs)
    # print(from_city_set)
    graph = {}
    for city in from_city_set:
        trains = Train.objects.filter(from_city=city).values('to_city')
        tmp = set(i['to_city'] for i in trains)
        graph[city] = tmp
    return graph


def find_routes(request):
    if request.method == 'POST':
        form = RouteForm(request.POST or None)
        if form.is_valid():
            data = form.cleaned_data  # проверить, объект типа словарь
            # assert False
            from_city = data['from_city']

            # print('\n','from_city', type(from_city))  # print('\n','from_city', from_city)
            # print('\n', type(from_city.name))  # class 'str'

            to_city = data['to_city']
            across_cities_form = data['across_cities']  # получаем что-то в виде списка
            traveling_time = data['traveling_time']
            # на данном этапе мы получили все данные с формы

            graph = get_graph()

            # print()
            # print('our_graph', graph)
            # print()

            all_ways = list(dfs_paths(graph, from_city.id, to_city.id))  # список
            # всех маршрутов между выбранными в форме городами
            # print()
            # print('all_ways', all_ways)
            # print()

            # проверка на наличие маршрутов между указанными городами в форме
            if len(all_ways) == 0:
                messages.error(request, 'Маршрута, '
                                        'удовлетворяющего условиям, '
                                        'не существует')
                return render(request, 'routes/home.html', {'form': form})

            # если есть города, через которые надо проехать
            if across_cities_form:  # Если в форму ввели города,
                # то мы ищем те маршруты, которые соединяют эти города
                across_cities = [city.id for city in across_cities_form]  # достаем в список
                # города после возвращения формы
                right_ways = []
                for way in all_ways:
                    if all(point in way for point in across_cities):  # возвращает True,
                        # когда все города(point) через которые проходит маршрут(way)
                        # присутсвуют в списке городов, которые нужно посетить(across_cities)
                        right_ways.append(way)

                #  если такого маршрута не нашлось
                if not right_ways:
                    messages.error(request, 'Маршрут через эти города, не возможен ')
                    return render(request, 'routes/home.html', {'form': form})

            #  если в форму не ввели города, которые нам необходимо
            #  посетить попути, значит все маршруты соединяющие
            #  конечные города нам подходят
            else:
                right_ways = all_ways
        # на данный момент мы получаем список, содержащий ID городов входящих в удовлетворяющие маршруты.

        # на основе списка right_ways выбираем поезда, которые включены в наш маршрут, чтоб их отобразить
        trains = []
        for route in right_ways:
            tmp = {}
            tmp['trains'] = []
            total_time = 0
            for index in range(len(route) - 1):
                qs = Train.objects.filter(from_city=route[index], to_city=route[index + 1])  # запрос, возвращающий
                # поезда(с модели Train), выбранные по значениям из маршрутов
                qs = qs.order_by('travel_time').first()  # конструкция фильтрует все значения поездов и
                # возвращает с намиеньшим значение поля'travel_time'
                total_time += qs.travel_time
                tmp['trains'].append(qs)
            tmp['total_time'] = total_time  # полное время пути

            # проверка соответствия времени
            if total_time <= traveling_time:
                trains.append(tmp)
        if not trains:
            messages.error(request, 'время в пути больше заданного')
            return render(request, 'routes/home.html', {'form': form})

        # print('\n', trains, '\n')

        routes = []
        cities = {'from_city': from_city.name, 'to_city': to_city.name}  # параметры для отображения на странице

        # print('\n', cities, '\n')
        # преобразовываем полученный список trains  в более удобный вид
        for tr in trains:
            routes.append({'route': tr['trains'],
                           'total_time': tr['total_time'],
                           'from_city': from_city.name,
                           'to_city': to_city.name
                           })
            # print('\n', routes, '\n')

        # сортируем маршруты под продолжительности поездки
        sorted_routes = []
        if len(routes) == 1:
            sorted_routes = routes
        else:
            times = list(set(x['total_time'] for x in routes))  # вытаскиваем временя маршрутов
            # print('\n', times, '\n')
            times = sorted(times)
            for time in times:
                for route in routes:
                    if time == route['total_time']:
                        sorted_routes.append(route)

        # отображаем эту дичь
        context = {}
        form = RouteForm()
        context['form'] = form
        context['routes'] = sorted_routes
        context['cities'] = cities
        return render(request, 'routes/home.html', context)

    else:
        messages.error(request, 'Создайте маршрут')
        form = RouteForm()
        return render(request, 'routes/home.html', {'form': form})


def add_route(request):  # функция отображения сохранения маршрута
    if request.method == "POST":  # отрабатывает при нажатии на кнопку "сохранить"
        form = RouteModelForm(request.POST or None)
        if form.is_valid():
            data = form.cleaned_data
            name = data['name']
            travel_times = data['travel_times']
            from_city = data['from_city']
            to_city = data['to_city']
            across_cities = data['across_cities'].split(' ')
            trains = [int(x) for x in across_cities if x.isalnum()]
            qs = Train.objects.filter(id__in=trains)

            route = Route(name=name, from_city=from_city,
                          to_city=to_city, travel_times=travel_times)
            route.save()
            for tr in qs:
                route.across_cities.add(tr.id)
            messages.success(request, 'Маршрут был успешно сохранен.')
            return redirect('/')
    else:
        data = request.GET
        if data:
            travel_times = data['travel_times']
            from_city = data['from_city']
            to_city = data['to_city']
            across_cities = data['across_cities'].split(' ')
            trains = [int(x) for x in across_cities if x.isalnum()]
            qs = Train.objects.filter(id__in=trains)
            train_list = ' '.join(str(i) for i in trains)
            form = RouteModelForm(initial={'from_city': from_city,
                                           'to_city': to_city,
                                           'travel_times': travel_times,
                                           'across_cities': train_list})
            route_desc = []
            # передаем описательную часть
            for tr in qs:
                dsc = 'Поезд №{} следующий из г. {} в г. {}. Время в пути {} часа'.format(tr.name,
                                                                                  tr.from_city,
                                                                                  tr.to_city,
                                                                                  tr.travel_time)
                route_desc.append(dsc)
            print('\n', route_desc, '\n')
            context = {'form': form, 'descr': route_desc,
                       'from_city': from_city, 'to_city': to_city,
                       'travel_times': travel_times}
            return render(request, 'routes/create.html', context)
        else:
            messages.error(request, 'Невозможно сохранить несуществующий маршрут')
            return redirect('/')


class RouteDetailView(DetailView):
    queryset = Route.objects.all()
    context_object_name = 'object'
    template_name = 'routes/detail.html'


class RouteListView(ListView):
    queryset = Route.objects.all()
    context_object_name = 'object_list'
    template_name = 'routes/list.html'


class RouteDeleteView(DeleteView):  # t20 класс создания новой записи в б/д
    model = Route
    # template_name = 'cities/delete.html'  # Запускаем страницу удаления c подтверждением
    success_url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):  # удаляем без страницы подтверждения
        messages.success(request, 'Маршрут успешно удален')
        return self.post(request, *args, **kwargs)