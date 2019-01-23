import uuid

from users.models import UserProfile

from django.contrib.gis.db import models
from django.contrib.gis.geos import Point

class DengueBite(models.Model):
    userprofile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    bite_uuid = models.TextField(primary_key=True, default=uuid.uuid4, editable=False)
    lng = models.FloatField()
    lat = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    location = models.PointField(geography=True, srid=4326, default='POINT(0.0 0.0)')

    def __str__(self):
        return "%s %s" % (self.userprofile.user_uuid, str(self.bite_uuid))

        def save(self, **kwargs):
            self.location = Point(float(self.lng), float(self.lat))
            super(DengueBite, self).save(**kwargs)
