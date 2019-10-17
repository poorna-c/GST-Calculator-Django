from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('register/',views.register,name='register_page'),
    path('login/',auth_views.LoginView.as_view(template_name = 'accounts/login.html'),name = 'login_page'),
    path('logout/',auth_views.LogoutView.as_view(template_name = 'accounts/logout.html'),name = 'logout_page'),
    path('profile/',views.profile,name = 'profile_page'),
]
