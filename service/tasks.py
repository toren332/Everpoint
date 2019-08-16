from celery import shared_task
from os import listdir
from django.conf import settings
from . import models
import pandas as pd
import datetime



@shared_task
def xlsx_to_db():
    way = settings.MEDIA_ROOT+"/files/"
    old_files = []
    for file in models.XlsxFile.objects.all():
        old_files.append(file.file_name)

    current_files = listdir(way)
    new_files = list(set(current_files) - set(old_files))
    for file_name in new_files:
        df = pd.read_excel(way+file_name)
        for i in df.values:
            code = i[0]
            dt = datetime.datetime.combine(datetime.datetime.date(i[1]), i[2])
            lat = i[3]
            lng = i[4]
            name = i[5]

            if not models.Ship.objects.filter(code=code):
                models.Ship.objects.create(name=name, code=code)
            ship = models.Ship.objects.get(code=code)
            models.LatLngHistory.objects.create(
                dt=dt,
                lat=lat,
                lng=lng,
                ship=ship
            )

        models.XlsxFile.objects.create(file_name=file_name)

    return new_files
