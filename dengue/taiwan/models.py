from django.contrib.gis.db import models

class Substitute(models.Model):
    object_id = models.IntegerField()
    u_id = models.IntegerField()
    pro_id = models.CharField(max_length=2)
    county_id = models.CharField(max_length=5)
    town_id = models.CharField(max_length=7)
    village_id = models.CharField(max_length=20)
    v_name = models.CharField(max_length=50)
    t_name = models.CharField(max_length=50)
    c_name = models.CharField(max_length=50)
    substitute = models.CharField(max_length=50)

    mpoly = models.MultiPolygonField(geography=True, srid=4326)
