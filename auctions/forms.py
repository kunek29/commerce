from django.forms import ModelForm, ModelMultipleChoiceField
from auctions.models import Listing, User, Bids, Categories, Comments, Watchlist
from django import forms


class ListingForm(ModelForm):
    #category_list = ModelMultipleChoiceField(queryset=Categories.objects.values_list('category_list', flat=True))
    class Meta:
        model = Listing
        fields = ["title", "description", "image_url", "min_bid", "category"]


class CommentsForm(ModelForm):
    class Meta:
        model = Comments
        fields = ["comment"]


class BidsForm(ModelForm):
    class Meta:
        model = Bids
        fields = ["amount"]

        