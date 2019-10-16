from django.db import models


class Auction(models.Model):
    item = models.CharField(max_length=256)
    description = models.TextField()
    minimum_price = models.FloatField()
    deadline_date = models.DateTimeField()
    status = models.CharField(max_length=60)
    creator_id = models.IntegerField()


class Bidder(models.Model):
    auction_id = models.IntegerField()
    bidder_id = models.IntegerField()