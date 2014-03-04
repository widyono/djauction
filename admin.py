from models import (AuctionUser, Auction, AuctionItem, AuctionEvent,
    AuctionParticipant, AuctionBid)
from django.contrib import admin

admin.site.register(AuctionUser)
admin.site.register(Auction)
admin.site.register(AuctionItem)
admin.site.register(AuctionEvent)
admin.site.register(AuctionParticipant)
admin.site.register(AuctionBid)
