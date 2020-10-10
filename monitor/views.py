from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from lxml import html
import urllib.request
from .models import Vacancy, Marker
from django.shortcuts import get_object_or_404


# Create your views here.

class HomeView(ListView):
    model = Marker
    template_name = 'monitor/home.html'
    markers_in_db = Marker.objects.all()
    for marker in markers_in_db:
        if not Vacancy.objects.filter(marker__slug=marker):
            Marker.objects.filter(slug=marker).delete()
    context_object_name = 'markers'


def vacansies_by_marker(request, slug):
    vacansies = Vacancy.objects.filter(marker__slug=slug)
    context = {'vacansies': vacansies}
    return render(request, 'monitor/vacansies-by-marker.html', context)


def search_and_parse(request):
    name_and_link = []
    q = request.GET.get('q')
    if not Marker.objects.filter(slug=q):
        Marker.objects.create(slug=q)
    marker = get_object_or_404(Marker, slug=q)
    saved_vac = Vacancy.objects.filter(marker__slug=marker)
    already_saved_vac = [str(i) for i in saved_vac]
    iterate_q = q.split()
    search_query_base = 'https://hh.ru/search/vacancy?L_is_autosearch=false' \
                        '&area=1&clusters=true&enable_snippets=true&text='
    for word in iterate_q:
        search_query_base += f'{word}+'
    for i in range(0, 3):
        url = search_query_base + '&page={0}'.format(i)
        print(url)
        request_html = urllib.request.urlopen(url)
        mybytes = request_html.read()
        tree = html.fromstring(mybytes)
        vacancy_link = tree.xpath(
            '/html/body/div[6]/div/div/div[2]/div/div['
            '3]/div/div[2]/div/div[3]/div/div/div/div['
            '2]/div[1]/span/span/span/a/@href')
        vacancy_name = tree.xpath(
            '/html/body/div[6]/div/div/div[2]/div/div['
            '3]/div/div[2]/div/div[3]/div/div/div/div['
            '2]/div[1]/span/span/span/a/text()')
        for link, name in zip(vacancy_link, vacancy_name):
            name_and_link.append([name, link[:str(link).find('?')]])
    parsed_links = [link for name, link in name_and_link]
    for name, link in name_and_link:
        if not Vacancy.objects.filter(vacancy_link=link):
            Vacancy.objects.create(vacancy_name=name, vacancy_link=link,
                                   marker=marker)
        else:
            if not Vacancy.objects.filter(vacancy_link=link, new_or_old=2):
                vacancy_obj = Vacancy.objects.filter(vacancy_link=link)
                number = ([str(i) for i in vacancy_obj.values('new_or_old')][0][-2])
                vacancy_obj.update(new_or_old=int(str(number))+1)
            else:
                continue
    saved_vacancies = Vacancy.objects.filter(marker__slug=marker)
    for item in already_saved_vac:
        if item not in parsed_links:
            Vacancy.objects.filter(vacancy_link=item).delete()
    context = {'object': saved_vacancies}
    return render(request, 'monitor/parsed-data.html', context)
