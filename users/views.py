from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer, weatherDataSerializer
from .models import User, weatherData
import jwt, datetime
import requests
import csv
from io import StringIO
from django.core.mail import EmailMessage, send_mail
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view
from django.conf import settings

# Create your views here.

#register User
class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

#User Login view
class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found!')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256').decode('utf-8')

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }
        return response

#User list View
class UserView(APIView):

    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)

# Logout view
class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response

#get weather data in email
@api_view(['POST'])
def weather_email(request):
    token = request.COOKIES.get('jwt')

    if not token:
        raise AuthenticationFailed('Unauthenticated!')
    response = Response()

    url = "https://api.openweathermap.org/data/2.5/group?id=524901,703448,2643743,5128581,4068590,4068590,5308655,4119403,5389519,2643741,4174757,4553440,4281730,5412347,5325738,5150529,5323810,5392900,5387890,5505411&appid=57590eef9c2c1ae7905ec6d3f02a39b1"
    # url = "https://api.openweathermap.org/data/2.5/group?id=524901,703448,2643743,5128581,4068590,4068590,5308655,4119403,5389519,149653,149658,149703,149768,149775,149792,149812,149854,149876,149879,149929,150004,150006,150037,150099,150173,150276,150436,150442,150453,150580,150602,150634,150689,150732,150733,150793,150885,150930,151062,151108&appid=57590eef9c2c1ae7905ec6d3f02a39b1" 

    # 4164138,4167147,4180439,5856195,3582383,4269802,5024719,4418478,4860019,4929283,4931108,4975802,5016884,5476526,4744247,4798258,5263045,5263058,5263113,5263023
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
            
            message = EmailMessage("Hello","Weather data", settings.EMAIL_HOST_USER, settings.RECIPIENT_LIST)

            message.attach('WeatherData.csv', csvfile.getvalue(), 'text/csv')
            message.send()
            response.data = {
                'message': 'Email sent'
            }
            return response
            

        except:
            response.data = {
                'message': 'Exception'
            }
            return response

#get weather data in JSON (pagination)
@api_view(['POST',])
def get_weather_data_Json(request):
    token = request.COOKIES.get('jwt')

    if not token:
        raise AuthenticationFailed('Unauthenticated!')

    paginator = PageNumberPagination()
    paginator.page_size = 5
    weather_object = weatherData.objects.all()
    print(weather_object)
    result_page = paginator.paginate_queryset(weather_object, request)
    serializer = weatherDataSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)

