from django.db import models
from django.contrib.auth.models import User


class Auction(models.Model):
    item = models.CharField(max_length=256)
    description = models.TextField()
    minimum_price = models.FloatField()
    deadline_date = models.DateTimeField()
    status = models.CharField(max_length=60)
    creator = models.CharField(max_length=256)
    highest_bidder_id = models.IntegerField()


class Bidder(models.Model):
    auction_id = models.ForeignKey(Auction, on_delete=models.CASCADE)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
