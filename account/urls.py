from django.urls import path

from . import views
app_name = 'account'
urlpatterns = [
    path('', views.index, name='index'),
    path('Signup/', views.signup, name='create'),
    path('LogIn/', views.login_view, name='login'),
    path('home/', views.home_view, name='home'),
    path('LogOut/', views.logout_view, name='logout'),
]