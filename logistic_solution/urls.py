from django.conf.urls import url
from logistic_solution import views

urlpatterns = [
    url(r'place/$', views.startPlace_list),
    url(r'place/(?P<pk>[0-9]+)/$', views.place_detail),
]
