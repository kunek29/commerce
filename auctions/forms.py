from django.forms import ModelForm, Textarea, TextInput, NumberInput, Select
from auctions.models import Listing, User, Bids, Categories, Comments, Watchlist


class ListingForm(ModelForm):
    #category_list = ModelMultipleChoiceField(queryset=Categories.objects.values_list('category_list', flat=True))
    class Meta:
        model = Listing
        fields = ["title", "description", "image_url", "min_bid", "category"]
        labels = {
            "image_url": "Add image Url (optional)",
            "min_bid": "Set min. bid"}
        widgets = {
            "description": Textarea(attrs={
                "placeholder": "Add description",
                "class": "input",
                "id": "description"}),
            "title": TextInput(attrs={
                "placeholder": "Add title",
                "class": "input"}),
            "image_url": TextInput(attrs={
                "placeholder": "Add image URL",
                "class": "input"}),
            "min_bid": NumberInput(attrs={
                "placeholder": "Add min. amount",
                "class": "input"}),
            "category": Select(attrs={
                "class": "input"})
                }


class CommentsForm(ModelForm):
    #comment = forms.CharField(widget=Textarea, label='')
    class Meta:
        model = Comments
        fields = ["comment"]
        widgets = {"comment": Textarea(attrs={
            "placeholder": "Comment here",
            "class": "input",
            "id": "comment"})}
        labels = {"comment": ''}



class BidsForm(ModelForm):
    class Meta:
        model = Bids
        fields = ["amount"]

        