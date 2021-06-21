# Features:
1. Django rest login and logout
2. Fetch external weather api data every 30 mins.
3. store weather data in DB.
4. Get paginated api data
5. Sending email using api call without async task

Requirements:
All the required packages are mentioned in requirements.txt file in Django Project folder.

asgiref==3.3.4
certifi==2021.5.30
chardet==4.0.0
Django==3.2.4
django-cors-headers==3.7.0
django-crontab==0.7.1
djangorestframework==3.12.4
idna==2.10
PyJWT==1.7.1
pytz==2021.1
requests==2.25.1
six==1.16.0
sqlparse==0.4.1
typing-extensions==3.10.0.0
tzlocal==2.1
urllib3==1.26.5

Install and Run

Create a virtual environment where all the required python packages will be installed

Activate the virtual environment

Install all the project Requirements:  pip install -r requirements.txt

In Django projects settings.py set your email host details:

EMAIL_BACKEND ='django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'smtp.gmail.com'

EMAIL_USE_TLS = True

EMAIL_PORT = 587

EMAIL_HOST_USER = 'your@gmail.com'

EMAIL_HOST_PASSWORD = ''

In Django projects settings.py add recipient list:
RECIPIENT_LIST = []

Run the following commands to start scheduling task (Now set to 30 mins)

Start

python manage.py crontab add .

Show current active jobs

python manage.py crontab show

Stop current active jobs

python manage.py crontab remove

Run the development server

python manage.py runserver

Testing:

For api testing I used Postman and I am adding those test screenshots here.

1. Login API
Post http://127.0.0.1:8000/api/login
Input credentials= {"email": "rakesh@gmail.com","password": "asdf"} 
Use this user credentials: "email": "rakesh@gmail.com","password": "asdf"
Output 
Success = {    "jwt": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwiZXhwIjoxNjIzMDUxOTY5LCJpYXQiOjE2MjMwNDgzNjl9.ew_vUXYe4EkfIMqDgBakOlEp_oPMrfEyTuFyT8k8ZjU"}
Password error = {   "detail": "Incorrect password!"}
User not found = { "detail": "User not found!"}

2. Logout API
POST http://127.0.0.1:8000/api/logout
Cookie is deleted from browser
Output Success = {"message": "success"}

3. Email Weather API 
I have created the cron.py in the django project folder here I have added the api call and emailing a csv to the recipient list.
Flow is as follows:
Call the  https://openweathermap.org/api using requests
Stores weather data in weatherData model
Creates a csv files from the data
Send the email with csv attachment to RECIPIENT_LIST
Output:


4. Get Weather Information API Pagination
POST http://127.0.0.1:8000/api/weather
Input {   "jwt": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwiZXhwIjoxNjIzMDU0MDU3LCJpYXQiOjE2MjMwNTA0NTd9.uFY2I5PDw9thdVGENFvtOILs3Ts7BgVxYDeZIIayEHA"}
Post the JWT token when calling this api, It will first authenticate the user and then give the data.
Pagination
POST http://127.0.0.1:8000/api/weather?page=2
This is also handels pagination
Now the page size is given as 5





5. Sending email using api call without async task (I have added this process just for testing purpose)
POST http://127.0.0.1:8000/api/email 
Call the  https://openweathermap.org/api using requests
Stores weather data in weatherData model
Creates a csv files from the data
Send the email with csv attachment to RECIPIENT_LIST
Output 
Receive weather data csv file in mail
 { 'message': 'Email sent'   }



