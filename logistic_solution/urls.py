from django.conf.urls import url
from logistic_solution import views

urlpatterns = [
    url(r'place/$', views.startPlace_list),
    url(r'place/(?P<pk>[0-9]+)/$', views.place_detail),
    url(r'solution_selectedPlace/$', views.solution_list_selectedPlace),
    url(r'solution_inputPlace/$', views.solution_list_inputPlace),
]
