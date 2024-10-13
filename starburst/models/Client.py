from django.db import models


class Client(models.Model):
    str_id = models.CharField(max_length=64, primary_key=True, unique=True)
    name = models.CharField(max_length=255, db_index=True)
    max_delays = models.IntegerField(default=0)
    min_sequence = models.IntegerField(default=0)

    objects = models.Manager()
