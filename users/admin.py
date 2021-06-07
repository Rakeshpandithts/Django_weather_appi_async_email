from django.contrib import admin
from .models import User, weatherData

# Register your models here.
admin.site.register(weatherData)
admin.site.register(User)

