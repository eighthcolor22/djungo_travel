from django.shortcuts import render
from django.contrib import messages
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
            to_city = data['to_city']
            across_cities_form = data['across_cities']  # получаем что-то в виде списка
            traveling_time = data['traveling_time']
            # на данном этапе мы получили все данные с формы

            graph = get_graph()
            all_ways = list(dfs_paths(graph, from_city.id, to_city.id))  # список
            # всех маршрутов между выбранными в форме городами

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

        # отображаем эту дичь
        trains = []
        for route in right_ways:
            tmp = {}
            tmp

        context = {}
        form = RouteForm()
        context['form'] = form
        context['ways'] = right_ways
        return render(request, 'routes/home.html', context)

        return render(request, 'routes/home.html', {'form': form})
    else:
        messages.error(request, 'Создайте маршрут')
        form = RouteForm()
        return render(request, 'routes/home.html', {'form': form})
