from models import (AuctionUser, Auction, AuctionItem, AuctionEvent,
    AuctionParticipant, AuctionBid)
from django.contrib import admin

class AuctionUserAdmin(admin.ModelAdmin):
    ordering=('name',)
    list_display=('name','email','phone')
admin.site.register(AuctionUser, AuctionUserAdmin)
admin.site.register(Auction)

class AuctionItemAdmin(admin.ModelAdmin):
    ordering=('auction_event','item_number','name')
    list_display=('auction_event','item_number','name')
admin.site.register(AuctionItem, AuctionItemAdmin)
admin.site.register(AuctionEvent)
admin.site.register(AuctionParticipant)
admin.site.register(AuctionBid)
