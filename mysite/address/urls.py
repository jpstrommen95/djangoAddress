from django.urls import path

from . import views

# create the url path here
urlpatterns = [
    path('', views.index, name='login'),
    path('home/', views.home, name='home'),
    # ex: /polls/5/
    path('<int:contact_id>/', views.detail, name='detail'),
    # ex: /polls/5/results/
    path('<int:contact_id>/results/', views.results, name='results'),
    # ex: /polls/5/vote/
    path('<int:contact_id>/vote/', views.vote, name='vote'),
]
