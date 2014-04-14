from django.db import models

STATE_CHOICES = (
    ('pa', 'Pennsylvania'),
    ('nj', 'New Jersey'),
)

ITEM_CHOICES = (
    ('event','Event'),
    ('food','Food'),
    ('goods','Goods'),
    ('service','Service'),
    ('other','Other'),
)

PAYMENT_CHOICES = (
    ('none','None'),
    ('cash','Cash'),
    ('check','Check'),
    ('credit','Credit'),
)

class Auction(models.Model):

    ''' Model to represent an Auction '''

    name = models.CharField(max_length=255)
    date = models.DateField()

    def __unicode__(self):
        return self.name + ' ' + str(self.date)

class AuctionUser(models.Model):

    ''' Model to represent an Auction User; i.e. someone who donates
        or bids on users '''

    name = models.CharField(max_length=255)
    address_1 = models.CharField(max_length=255, blank=True)
    address_2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    state = models.CharField(max_length=2, choices=STATE_CHOICES,
        blank=True)
    zip = models.CharField(max_length=10, blank=True)
    phone = models.CharField(max_length=255, blank=True)
    email = models.EmailField(max_length=255, blank=True)

    def __unicode__(self):
        return self.name

class AuctionParticipant(models.Model):

    ''' Model to represent an Auction Participant; i.e. someone who
        will be bidding on items in the auction '''

    auction = models.ForeignKey(Auction)
    user = models.ForeignKey(AuctionUser)
    paddle = models.PositiveIntegerField()
    payment_method = models.CharField(max_length=10, choices=PAYMENT_CHOICES,
        default='none')
    payment_notes = models.TextField(blank=True)

    def __unicode__(self):
        return str(self.user) + ' (' + str(self.paddle) + ')'

class AuctionEvent(models.Model):

    ''' Model to represent an Auction Event; i.e. a collection of items
        that will be bid on during the auction '''

    name = models.CharField(max_length=255)
    abbreviation = models.CharField(max_length=10)
    auction = models.ForeignKey(Auction)

    def __unicode__(self):
        return self.name + ' ' + self.abbreviation

class AuctionItem(models.Model):

    ''' Model to represent an Item to be bid on in an auction '''

    name = models.CharField(max_length=255)
    item_type = models.CharField(max_length=20, choices=ITEM_CHOICES)
    item_number = models.IntegerField()
    description = models.TextField(blank=True)
    image = models.ImageField(max_length=255,upload_to='images',blank=True)
    valid_winners = models.PositiveIntegerField(default=1)
    auction = models.ForeignKey(Auction)
    auction_event = models.ForeignKey(AuctionEvent)
    donor = models.ForeignKey(AuctionUser)
    starting_bid = models.FloatField()
    conditions = models.TextField(blank=True)
    time_and_location = models.TextField(blank=True)

    def __unicode__(self):
        return str(self.auction_event.abbreviation) + str(self.item_number) + ' ' + self.name

class AuctionBid(models.Model):

    ''' Model to represent an individual Bid in an Auction '''

    auction = models.ForeignKey(Auction)
    bidder = models.ForeignKey(AuctionParticipant)
    item = models.ForeignKey(AuctionItem)
    ammount = models.FloatField()

    def __unicode__(self):
        return str(self.bidder) + ' ' + str(self.ammount)
