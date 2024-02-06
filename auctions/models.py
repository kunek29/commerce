from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Categories(models.Model):
    category_list = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.category_list}"
    

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=1024)
    date = models.DateTimeField(auto_now_add=True)
    image_url = models.URLField(max_length = 256, blank=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "listing_seller")
    min_bid = models.DecimalField(max_digits=12, decimal_places=2)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name = "listing_category")
    status = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.id}: {self.title}, {self.description}, {self.date}, {self.image_url}, {self.seller}, {self.min_bid}, {self.category}"

    

class Bids(models.Model):
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids_user")
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name = "listing_bid")

    def __str__(self):
        return f"{self.id}: {self.amount}, {self.bidder}, {self.listing_id}"


class Comments(models.Model):
    comment = models.TextField(max_length=256)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_user")
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_comment")
    
    def __str__(self):
        return f"{self.id}: {self.comment}, {self.date}, {self.user}, {self.listing_id}"


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "watchlist_user")
    listing_id = models.ManyToManyField(Listing, related_name="watchlist_listing")

    def __str__(self):
        return f"{self.id}: {self.user}, {self.listing_id}"
    