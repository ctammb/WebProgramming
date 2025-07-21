from django import forms
from .models import Listing, Bid, Category

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'starting_bid', 'image_url', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'starting_bid': forms.NumberInput(attrs={'class': 'form-control', 'min': '0.01', 'step': '0.01'}),
            'image_url': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all()
        self.fields['category'].empty_label = "Select a Category"


class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['amount']
    def __init__(self, *args, **kwargs):
        min_bid = kwargs.pop('min_bid', None)
        super().__init__(*args, **kwargs)
        if min_bid:
            self.fields['amount'].widget = forms.NumberInput(attrs={
                'min': f"{min_bid}",
                'step': '0.01',
                'placeholder': f'Min bid: ${min_bid}'
            })