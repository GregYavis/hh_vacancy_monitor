from django.urls import path
from .views import HomeView, search_and_parse, vacansies_by_marker

app_name = 'monitor'
urlpatterns = [
    path('', HomeView.as_view(), name='main-page'),
    # path('parse_hh/', parse, name='parse-hh-data'),
    path('search/', search_and_parse, name='search'),
    path('vacansy-marker/<slug>', vacansies_by_marker, name='vacancy-marker')

]
