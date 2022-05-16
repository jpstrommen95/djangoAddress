from django.urls import path

from . import views

app_name = 'address'  # give it a namespace here

# create the url path here
urlpatterns = [
    path('', views.index, name='login'),
    path('home/', views.home, name='home'),
    path('<int:contact_id>/', views.detail, name='detail'),
    path('<int:contact_id>/edit/', views.edit, name='edit'),
]
