from django import forms
from datetime import datetime


class AuctionForm(forms.Form):
    item = forms.CharField(label="Item", max_length=256)
    description = forms.CharField(label="description")
    minimum_price = forms.FloatField(label="Minimum price")
    deadline_date = forms.DateTimeField(label="Deadline", initial=datetime.now())