from django.urls import path

from . import views

app_name = 'address'  # give it a namespace here

# create the url path here
urlpatterns = [
    # navigable pages
    path('/', views.index, name='login'),
    path('/home', views.home, name='home'),
    path('/add', views.add, name='add'),
    path('/<int:contact_id>', views.detail, name='detail'),

    # api endpoints for posts, etc.
    path('/do_add', views.do_add, name='do_add'),
    path('/<int:contact_id>/do_edit', views.do_edit, name='do_edit'),
    path('/<int:contact_id>/do_delete', views.do_delete, name='do_delete'),
    path('/<int:contact_id>/phone/do_add', views.phone_add, name='phone_add'),
    path('/<int:contact_id>/phone/<int:phonenumber_id>/do_delete', views.phone_delete, name='phone_delete'),
    path('/sign_out', views.sign_out, name='sign_out'),
]
