from django.urls import path
from .views import RegisterView, LoginView, UserView, LogoutView, get_weather_data_Json, weather_email

urlpatterns = [
    path('register', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('user', UserView.as_view()),
    path('logout', LogoutView.as_view()),
    path('weather',get_weather_data_Json),
    path('email',weather_email),
]
