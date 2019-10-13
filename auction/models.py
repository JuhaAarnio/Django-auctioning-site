from django.db import models


class Auction(models.Model):
    item = models.CharField(max_length=256)
    description = models.TextField()
    minimum_price = models.FloatField()
    deadline_date = models.DateTimeField()
    creator_id = models.IntegerField()