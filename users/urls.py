from django.urls import path
from . import views
app_name = 'users'
urlpatterns = [
    path('register', views.register, name='register'),
    path('register-select', views.register_select, name='register-select'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('profile/<str:username>/edit', views.edit_profile, name='edit'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('<int:user_id>/update-role/', views.update_role, name='update-role'),
]