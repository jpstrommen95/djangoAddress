from django.urls import path

from . import views

# create the url path here
urlpatterns = [
    path('', views.index, name='index'),
]
