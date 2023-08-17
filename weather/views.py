from django.shortcuts import render
from .models import Weather
from decouple import config

city_pl = config('CITY_PL')
city_en = config('CITY_EN')


def ow_view(request):
    # raw_data = fetch_openweather_data(city_pl)
    # processed_data_list = process_openweather_data(city_pl, raw_data)
    #
    # if not processed_data_list:
    #     return HttpResponse("No data to process from openweather.")
    #
    #
    # for data in processed_data_list:
    #     Weather.objects.create(
    #         city=data['city'],
    #         country=data['country'],
    #         temperature=data['temperature'],
    #         sky_condition=data['sky_condition'],
    #         wind_speed=data['wind_speed'],
    #         pressure=data['pressure'],
    #         humidity=data['humidity']
    #     )
    #
    # all_weather_records = Weather.objects.all()
    #
    # context = {
    #     'weather_records': all_weather_records
    # }
    #
    # return render(request, 'index.html', {'active': 'ow'})

    processed_data_list = [
        {
            'city': 'Sample City',
            'country': 'Sample Country',
            'temperature': '25°C',
            'sky_condition': 'Sunny',
            'wind_speed': '5m/s',
            'pressure': '1000hPa',
            'humidity': '60%',
        },
    ]

    context = {
        'weather_records': processed_data_list,
        'active': 'ow'
    }

    return render(request, 'index.html', context)


def wa_view(request):
    all_weather_records = Weather.objects.all()

    context = {
        'weather_records': all_weather_records,
        'active':'wa'
    }
    return render(request, 'index.html', context)


def average_view(request):
    return render(request, 'index.html')


def info_view(request):
    return render(request, 'info.html')
