import uuid

from django.contrib.gis.db import models
from django.contrib.gis.geos import Point

from users.models import UserProfile


class Source(models.Model):
    userprofile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    source_uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    photo_url = models.URLField()
    photo_base64 = models.TextField(default='')
    source_type = models.TextField()
    lng = models.FloatField()
    lat = models.FloatField()
    address = models.TextField(default='')
    modified_address = models.TextField(default='')
    village_name = models.TextField(default='')
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    qualified_status = models.TextField(default='待審核')
    location = models.PointField(geography=True, srid=4326, default='POINT(0.0 0.0)')

    def __str__(self):
        return "%s %s" % (self.userprofile.phone, str(self.source_uuid))

    def save(self, **kwargs):
        self.location = Point(float(self.lng), float(self.lat))
        super(Source, self).save(**kwargs)
