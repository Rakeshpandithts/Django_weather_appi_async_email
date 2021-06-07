from .models import User, weatherData
import requests
import csv
from io import StringIO
from django.core.mail import EmailMessage
from django.conf import settings
def get_weather_data():
    url = "https://api.openweathermap.org/data/2.5/group?id=524901,703448,2643743,5128581,4068590,4068590,5308655,4119403,5389519,2643741,4174757,4553440,4281730,5412347,5325738,5150529,5323810,5392900,5387890,5505411&appid=57590eef9c2c1ae7905ec6d3f02a39b1"
    api_request = requests.get(url)
    try:
            api_request.raise_for_status()
            weather_datas =  api_request.json()
    except:
            return None
    if weather_datas is not None:
        try:
            for weather_data in weather_datas["list"]:
                if weatherData.objects.filter(city=weather_data["name"]).exists():
                    weather_object = weatherData.objects.filter(city=weather_data["name"])
                    weather_object.temperature = weather_data["main"]["temp"]
                    weather_object.description = weather_data["weather"][0]["description"]
                    weather_object.city = weather_data["name"]
                    weather_object.update()
                else:
                    weather_object = weatherData.objects.create(temperature=weather_data["main"]["temp"], description=weather_data["weather"][0]["description"], city=weather_data["name"])
                    weather_object.save()
            csvfile = StringIO()
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(["City", "Description", "Temperature"])

            for weather_data in weather_datas["list"]:
                csvwriter.writerow([weather_data["name"], weather_data["main"]["temp"], weather_data["weather"][0]["description"]])
            
            message = EmailMessage("Hello","Weather data",settings.EMAIL_HOST_USER, settings.RECIPIENT_LIST)

            message.attach('WeatherData.csv', csvfile.getvalue(), 'text/csv')
            message.send()
            

        except:
            print('Exception')