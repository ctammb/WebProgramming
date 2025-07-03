from django import forms
from .models import Listing

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'starting_bid', 'image_url', 'category']


class BidForm(forms.Form):
    amount = forms.DecimalField(label="Your Bid", max_digits=10, decimal_places=2)