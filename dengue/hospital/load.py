import os
import time

import googlemaps

from .models import Hospital


gmaps = googlemaps.Client(key=os.environ.get('GOOGLE_MAP_API_KEY'))


def run(file_path):
    with open(file_path, 'r') as myfile:
        hospital_raw_str = myfile.read()

    for line in hospital_raw_str.split('\n'):
        if line == "":
            continue

        line_split = line.split('\t')
        name = line_split[0]
        address = line_split[1]

        print(name, address)

        geocode_result = gmaps.geocode(address)
        if len(geocode_result) == 0:
            continue
        lng = geocode_result[0]['geometry']['location']['lng']
        lat = geocode_result[0]['geometry']['location']['lat']

        if len(line_split) >= 3:
            phone = line_split[2]
        else:
            phone = ""

        hospital_tuple = Hospital.objects.get_or_create(
            name=name,
            address=address,
            phone=phone,
            opening_hours="",
            lng=lng,
            lat=lat
        )
        hospital_tuple[0].save()

        time.sleep(1.5)
