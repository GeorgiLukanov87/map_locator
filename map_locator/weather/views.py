# from django.shortcuts import render
# import requests
#
#
# def weather(request):
#     appid = 'e9a97357148479e6439c5ba4333e96ee'
#     URL = 'https://api.openweathermap.org/data/2.5/weather'
#     PARAMS = {'q': 'amsterdam', 'appid': appid, 'unots': 'metric'}
#     r = requests.get(url=URL, params=PARAMS)
#     res = r.json()
#     description = res['weather'][0]['description']
#     icon = res['weather'][0]['icon']
#     temp = res['main']['temp']
#
#     context = {
#         'description': description,
#         'icon': icon,
#         'temp': temp,
#     }
#
#     return render(request, 'weather.html', context)


from django.shortcuts import render
import requests
import datetime


def weather(request):
    api_key = 'e9a97357148479e6439c5ba4333e96ee'
    current_weather_url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}'
    forecast_url = 'https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude=current,minutely,hourly,' \
                   'alerts&appid={} '

    if request.method == 'POST':
        city1 = request.POST['city1']
        city2 = request.POST.get('city2', None)

        weather_data1, daily_forecasts1 = fetch_weather_and_forecast(city1, api_key, current_weather_url, forecast_url)

        if city2:
            weather_data2, daily_forecasts2 = fetch_weather_and_forecast(city2, api_key, current_weather_url,
                                                                         forecast_url)
        else:
            weather_data2, daily_forecasts2 = None, None

        context = {
            'weather_data1': weather_data1,
            'daily_forecasts1': daily_forecasts1,
            'weather_data2': weather_data2,
            'daily_forecasts2': daily_forecasts2,
        }

        return render(request, 'weather.html', context)
    else:
        return render(request, 'weather.html')


def fetch_weather_and_forecast(city, api_key, current_weather_url, forecast_url):
    response = requests.get(current_weather_url.format(city, api_key)).json()
    lat, lon = response['coord']['lat'], response['coord']['lon']
    forecast_response = requests.get(forecast_url.format(lat, lon, api_key)).json()

    weather_data = {
        'city': city,
        'temperature': round(response['main']['temp'] - 273.15, 2),
        'description': response['weather'][0]['description'],
        'icon': response['weather'][0]['icon'],
    }

    daily_forecasts = []
    for daily_data in forecast_response['daily'][:5]:
        daily_forecasts.append({
            'day': datetime.datetime.fromtimestamp(daily_data['dt']).strftime('%A'),
            'min_temp': round(daily_data['temp']['min'] - 273.15, 2),
            'max_temp': round(daily_data['temp']['max'] - 273.15, 2),
            'description': daily_data['weather'][0]['description'],
            'icon': daily_data['weather'][0]['icon'],
        })

    return weather_data, daily_forecasts
