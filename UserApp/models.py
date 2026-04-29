from django.db import models

class Crop(models.Model):
    name = models.CharField(max_length=100)
    soil_type = models.CharField(max_length=100)
    ph = models.FloatField()
    moisture = models.FloatField()

    def __str__(self):
        return self.name