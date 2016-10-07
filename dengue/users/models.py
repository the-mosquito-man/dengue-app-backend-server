from django.conf import settings
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    user_uuid = models.TextField(primary_key=True)
    name = models.TextField(default=str())
    phone = models.TextField(default=str())
    is_signup = models.BooleanField(default=False)

    def __str__(self):
        return "%s %s" % (self.user_uuid, self.name)
