from django.contrib import admin

from .models import Categories, User, Bids, Comments, Listing, Watchlist

# Register your models here.

admin.site.register(Categories)
admin.site.register(User)
admin.site.register(Bids)
admin.site.register(Comments)
admin.site.register(Listing)
admin.site.register(Watchlist)
