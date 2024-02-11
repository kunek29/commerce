from django.contrib import admin

from .models import Categories, User, Bids, Comments, Listing, Watchlist

class BidsAdmin(admin.ModelAdmin):
    list_display = ("id", "bidder", "amount", 'listing_id')
# Register your models here.

admin.site.register(Categories)
admin.site.register(User)
admin.site.register(Bids, BidsAdmin)
admin.site.register(Comments)
admin.site.register(Listing)
admin.site.register(Watchlist)
