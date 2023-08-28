from django.shortcuts import render
from .models import Weather
from decouple import config
from datetime import datetime, timedelta

city_pl = config('CITY_PL')
city_en = config('CITY_EN')


def index_view(request):
    # Fetching the source parameter from the URL, default is 'average'.
    source = request.GET.get('source', 'average')

    # today's date and two preceding days.
    start_date = datetime.today().date()
    end_date = start_date + timedelta(days=2)

    # Fetching the weather instances based on the source and date range.
    weather_data = list(
        Weather.custom_objects.filter(source=source, date__range=(start_date, end_date)).order_by('-date'))

    context = {
        'weather_data': weather_data,
        'active': source,
        'ow_1': Weather.custom_objects.ow_1(),
        'ow_2': Weather.custom_objects.ow_2(),
        'ow_3': Weather.custom_objects.ow_3(),
        'wa_1': Weather.custom_objects.wa_1(),
        'wa_2': Weather.custom_objects.wa_2(),
        'wa_3': Weather.custom_objects.wa_3(),
        'av_1': Weather.custom_objects.av_1(),
        'av_2': Weather.custom_objects.av_2(),
        'av_3': Weather.custom_objects.av_3(),
    }
    return render(request, 'index.html', context)


def info_view(request):
    return render(request, 'info.html')
