from django.forms import ModelForm, Textarea, DecimalField
from auctions.models import Listing, User, Bids, Categories, Comments, Watchlist
from django import forms


class ListingForm(ModelForm):
    #category_list = ModelMultipleChoiceField(queryset=Categories.objects.values_list('category_list', flat=True))
    class Meta:
        model = Listing
        fields = ["title", "description", "image_url", "min_bid", "category"]
        labels = {
            "image_url": "Add image Url (optional)",
            "min_bid": "Set min. bid"}


class CommentsForm(ModelForm):
    #comment = forms.CharField(widget=Textarea, label='')
    class Meta:
        model = Comments
        fields = ["comment"]
        widgets = {"comment": Textarea(attrs={
            "cols": 60, 
            "rows": 2,
            "placeholder": "Comment here",
            "id": "comment-input"})}
        labels = {"comment": ''}



class BidsForm(ModelForm):
    class Meta:
        model = Bids
        fields = ["amount"]

        