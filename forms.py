from django import forms
from django.forms import ModelForm
from django.forms.widgets import CheckboxSelectMultiple

from models import (Auction, AuctionEvent, AuctionUser, AuctionBid,
    AuctionParticipant, AuctionItem)

class AuctionForm(ModelForm):

    ''' Form to create a new Auction '''

    class Meta:
        model = Auction
        exclude = ['paddles']

class AuctionEventForm(ModelForm):

    ''' Form to create a new Auction Event '''

    class Meta:
        model = AuctionEvent
        exclude = ['auction']

class AuctionParticipantForm(forms.Form):

    ''' Form to create a new Auction Participant (i.e. check a user into
        an auction '''

    name = forms.ModelChoiceField(queryset=AuctionUser.objects.all())
    paddle = forms.IntegerField(min_value=0)

class AuctionUserForm(ModelForm):

    ''' Form to create a new User '''

    class Meta:
        model = AuctionUser

class AuctionItemForm(ModelForm):

    ''' Form to create a new Item '''

    class Meta:
        model = AuctionItem
        exclude = ['auction','donor']

class AuctionBidAddForm(forms.Form):

    ''' Form to create new Bids for an item '''

    def __init__(self, *args, **kwargs):
        winners = kwargs.pop('winners')
        auction_id = kwargs.pop('auction_id')
        super (AuctionBidAddForm, self).__init__(*args, **kwargs)

        # dynamically creates fields to create multiple bids at once
        # based off how many valid winners are remaining for the item
        for i in xrange(winners):
            self.fields['user_%s' % str(i)] = forms.ModelChoiceField(
                queryset = AuctionParticipant.objects.filter(auction__exact=auction_id).order_by('paddle'),
                required=False)
            self.fields['user_%s' % str(i)].label = "User %s" % str(i+1)
            self.fields['bid_%s' % str(i)] = forms.FloatField(min_value=0,
                required=False)
            self.fields['bid_%s' % str(i)].label = "Bid %s" % str(i+1)

class AuctionBidDelForm(forms.Form):

    ''' Form to delete existing Bids for an item '''

    def __init__(self, *args, **kwargs):
        item = kwargs.pop('item')
        super (AuctionBidDelForm, self).__init__(*args, **kwargs)

        self.fields['bids'] = forms.ModelMultipleChoiceField(
            queryset = AuctionBid.objects.filter(item=item),
            widget=CheckboxSelectMultiple)

class AuctionBidExtraForm(ModelForm):

    ''' Form to add an extra Bid without enforcing bid maximums '''

    class Meta:
        model = AuctionBid
        exclude = ['auction','item']

class ImportFileForm(forms.Form):

    ''' Form to import data from a file '''

    file = forms.FileField()
