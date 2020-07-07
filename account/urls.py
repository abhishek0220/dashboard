from django.urls import path, include
from . import views
from django.urls import reverse_lazy
app_name = 'account'
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', views.index, name='index'),
    path('Signup/', views.signup, name='create'),
    path('LogIn/', views.login_view, name='login'),
    path('home/', views.home_view, name='home'),
    path('LogOut/', views.logout_view, name='logout'),
    path('forget/', views.forget_view, name = 'forget'),
    path('forget/done/', views.email_sent, name='email_sent'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name = 'account/reset_link.html',
        success_url =reverse_lazy('account:reset_done')
        ), name='password_change'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(
        template_name = 'account/reset_done.html'
        ) , name = "reset_done"),
]