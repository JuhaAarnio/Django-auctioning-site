from rest_framework import serializers
from auction.models import Auction


class SerializeAuctions(serializers.ModelSerializer):
    class Meta:
        model = Auction
        fields = ('item', 'description', 'minumum_price', 'deadline_date', 'status', 'creator_id')