import uuid

from django.contrib.gis.db import models
from django.contrib.gis.geos import Point

class Hospital(models.Model):
    hospital_uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.TextField()
    address = models.TextField()
    phone = models.TextField()
    opening_hours = models.TextField()
    lng = models.FloatField()
    lat = models.FloatField()

    location = models.PointField(geography=True, srid=4326, default='POINT(0.0 0.0)')

    def __str__(self):
        return str(self.hospital_uuid)

    def save(self, **kwargs):
        self.location = Point(float(self.lng), float(self.lat))
        super(Hospital, self).save(**kwargs)
