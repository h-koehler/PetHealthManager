from django.urls import path
from . import views
app_name = 'pets'
urlpatterns = [
    # pets views
    # path('', views.index, name='index'),
    path('', views.home_view, name='home'),
    path('list/', views.pets_view, name='pets-list'),
    path('<int:pet_id>/', views.pet_details, name='pet-details'),
    path('create/', views.pet_create, name='pet-create'),
    path('<int:pet_id>/edit', views.pet_edit, name='pet-edit'),
    path('<int:pet_id>/delete', views.pet_delete, name='pet-delete'),
    path('search/', views.pet_search, name='pet-search'),
    path('edit-condition/', views.pet_edit_condition, name='pet-edit_condition'),
    path('popup/', views.pet_popup, name='pet-popup'),
]