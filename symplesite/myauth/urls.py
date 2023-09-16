from django.urls import path
from .views import AboutMeView, RegisterView, login_view, logout_view, PasswordChangeView
from . import views

urlpatterns = [
    path('about-me/', AboutMeView.as_view(), name='about-me'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', login_view,  name='login'),
    path('logout/', logout_view, name='logout'),
    path('passwordchange/', PasswordChangeView.as_view(), name='passwordchange')
]