from django import forms
from datetime import datetime


class AuctionForm(forms.Form):
    item = forms.CharField(label="Item", max_length=256)
    description = forms.CharField(label="description")
    minimum_price = forms.FloatField(label="Minimum price")
    deadline_date = forms.CharField(label="Deadline", initial=datetime.now().strftime("%d-%m-%Y %H:%M:%S"))


class EditAuctionForm(forms.Form):
    new_description = forms.CharField(label="New Description", max_length=256)


class BiddingForm(forms.Form):
    bid = forms.FloatField(label="Your bid")