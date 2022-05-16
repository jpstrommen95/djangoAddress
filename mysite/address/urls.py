from django.urls import path

from . import views

app_name = 'address'  # give it a namespace here

# create the url path here
urlpatterns = [
    path('', views.index, name='login'),
    path('home/', views.home, name='home'),
    path('add/', views.add, name='add'),
    path('<int:contact_id>/', views.detail, name='detail'),

    path('<int:contact_id>/edit/', views.do_edit, name='do_edit'),
    path('do_add/', views.do_add, name='do_add'),
]
