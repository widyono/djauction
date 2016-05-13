# Django libraries
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.conf import settings

# djauction models and forms
from models import *
from forms import *

# Python libraries to support sending emails
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

@login_required
def index(request):

    ''' View to render the index page '''

    c = {}

    auctions = Auction.objects.all()
    c.update({'auctions':auctions})

    return render_to_response('djauction/index.html',c,
        context_instance=RequestContext(request))

@login_required
def profile(request):

    ''' View to render logged in user profile '''

    c = {}

    return render_to_response('djauction/profile.html',c,
        context_instance=RequestContext(request))

##### Views interacting with Auctions #####

@login_required
def add_auction(request):

    ''' View to set up a new auction '''

    c = {}

    if request.method == 'POST':
        form = AuctionForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse(index))
        else:
            c.update({'form':form})
    else:
        form = AuctionForm()
        c.update({'form':form})

    return render_to_response('djauction/addauction.html',c,
        context_instance=RequestContext(request))

@login_required
def view_auction(request,auction_id):

    ''' View to render an auction and manage items and users '''

    c = {}

    auction = Auction.objects.get(id=auction_id)
    all_bids = AuctionBid.objects.filter(auction=auction)
    net_earned = sum([bid.ammount for bid in all_bids])

    c.update({'auction':auction,'net_earned':net_earned})

    return render_to_response('djauction/viewauction.html',c,
        context_instance=RequestContext(request))

##### Views Interacting with AuctionEvents #####

@login_required
def add_event(request, auction_id):

    ''' View to add a new event to an auction '''

    c = {}

    auction = Auction.objects.get(id=auction_id)
    c.update({'auction':auction})

    if request.method == 'POST':
        form = AuctionEventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.auction = auction
            event.save()
            return HttpResponseRedirect(reverse(list_events, args=(auction.id,)))
        else:
            c.update({'form':form})
    else:
        form = AuctionEventForm()
        c.update({'form':form})

    return render_to_response('djauction/addevent.html',c,
        context_instance=RequestContext(request))

@login_required
def list_events(request,auction_id):

    ''' View to list all events configured for an auction '''

    c = {}

    auction = Auction.objects.get(id=auction_id)
    events = AuctionEvent.objects.filter(auction=auction)

    c.update({
        'auction':auction,
        'events':events,
        })

    return render_to_response('djauction/listevents.html',c,
        context_instance=RequestContext(request))

@login_required
def view_event(request, auction_id, event_id):

    ''' View to display details about an event '''

    c = {}

    auction = Auction.objects.get(id=auction_id)
    event = AuctionEvent.objects.get(id=event_id)
    items = AuctionItem.objects.filter(auction_event=event)

    c.update({
        'auction':auction,
        'event':event,
        'items':items,
        })

    return render_to_response('djauction/viewevent.html',c,
        context_instance=RequestContext(request))

##### Views Interacting with AuctionUsers #####

@login_required
def add_user(request):

    ''' View to add a new User to the system '''

    c = {}

    if request.method == 'POST':
        form = AuctionUserForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse(index))
    else:
        form = AuctionUserForm()
        c.update({'form':form})

    return render_to_response('djauction/adduser.html',c,
       context_instance=RequestContext(request))

@login_required
def view_user(request,user_id,auction_id=None):

    ''' View to render a user and all their object relationships '''

    c = {}

    auction_user = AuctionUser.objects.get(id=user_id)
    donated = AuctionItem.objects.filter(donor__exact=user_id)

    if auction_id:
        donated = donated.filter(auction__exact=auction_id)
        auction = Auction.objects.get(id=auction_id)
        participant = AuctionParticipant.objects.get(auction=auction,user=auction_user)
        bids = AuctionBid.objects.filter(auction=auction,bidder=participant)
        owed = sum([bid.ammount for bid in bids])
        c.update({
            'auction':auction,
            'participant':participant,
            'bids':bids,
            'owed':owed,
            })

    c.update({
        'auction_user':auction_user,
        'donated':donated,
        })

    return render_to_response('djauction/viewuser.html',c,
        context_instance=RequestContext(request))

@login_required
def list_users(request,auction_id):

    ''' View to list all users participating in an auction '''

    c = {}

    auction = Auction.objects.get(id=auction_id)
    participants = AuctionParticipant.objects.filter(auction__exact=auction_id).order_by('paddle')

    c.update({
        'auction':auction,
        'participants':participants
        })

    return render_to_response('djauction/listusers.html',c,
        context_instance=RequestContext(request))

@login_required
def checkin_user(request,auction_id):

    ''' View to check a user into a new auction event '''

    c = {}
    errors = []

    auction = Auction.objects.get(id=auction_id)
    c.update({'auction':auction})

    if request.method == 'POST':
        form = AuctionParticipantForm(request.POST)
        if form.is_valid():
            paddle = form.cleaned_data['paddle']
            auction_user = AuctionUser.objects.get(id=form.cleaned_data['name'].id)
            # check to see if the user has already checked in with a different paddle number;
            # if so, raise an error
            if len(AuctionParticipant.objects.filter(auction__exact=auction.id,
                user__exact=auction_user.id)) > 0:
                    errors.append('User {} is already checked in'.format(str(auction_user)))
            # check to see if the paddle has already been used; if so raise an error
            if len(AuctionParticipant.objects.filter(auction__exact=auction.id,
                paddle__exact=paddle)) > 0:
                    errors.append('Paddle {} is already in use'.format(str(paddle)))
            if len(errors) > 0:
                c.update({
                    'errors':errors,
                    'form':form,
                    })
            else:
                participant = AuctionParticipant(
                    auction = auction,
                    user = form.cleaned_data['name'],
                    paddle = paddle
                    )
                participant.save()
                return HttpResponseRedirect(reverse(list_users, args=(auction.id,)))
        else:
            c.update({'form':form})
    else:
        form = AuctionParticipantForm()
        c.update({'form':form})

    return render_to_response('djauction/checkinuser.html',c,
        context_instance=RequestContext(request))

@login_required
def checkout_user(request,auction_id,user_id):

    ''' View to check a user out of the auction'''

    c = {}

    auction = Auction.objects.get(id=auction_id)
    auction_user = AuctionUser.objects.get(id=user_id)
    paddle = AuctionParticipant.objects.get(auction=auction,
        user=auction_user)

    # user bids are the bids the user won items with
    user_bids = AuctionBid.objects.filter(auction=auction, bidder=paddle)
    # won users are the users that the current user won items from
    won_users = set([bid.item.donor for bid in user_bids])
    owed = sum([bid.ammount for bid in user_bids])

    donated_items = AuctionItem.objects.filter(auction=auction,
        donor=auction_user)
    donated_items_ids = [item.id for item in donated_items]

    # winning bids are the items donated by the current user that were won
    winning_bids = AuctionBid.objects.filter(auction=auction,
        item__in=donated_items_ids)
    # winning users are the users that won items donated by the current user
    winning_users = set([bid.bidder.user for bid in winning_bids])

    c.update({
        'auction':auction,
        'auction_user':auction_user,
        'user_bids':user_bids,
        'winning_bids':winning_bids,
        'won_users':won_users,
        'winning_users':winning_users,
        'owed':owed,
        'paddle':paddle,
        })

    if request.method == 'POST':
        form = ParticipantPaymentForm(request.POST,instance=paddle)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse(checkout_user, args=(auction.id,auction_user.id)))
        else:
            c.update({'form':form})
    else:
        form = ParticipantPaymentForm(instance=paddle)
        c.update({'form':form})

    return render_to_response('djauction/checkoutuser.html',c,
        context_instance=RequestContext(request))

@login_required
def user_paid_view(request,auction_id):

    ''' View to see the status of all users and if they have paid  '''

    c = {}

    auction = Auction.objects.get(id=auction_id)
    participants = AuctionParticipant.objects.filter(auction__exact=auction_id).order_by('paddle')
    p_data = []

    # to get around model/view restrictions, a list of tuples is being used to
    # move the data out in a non-object context. Variables need to be named inside
    # iterator on the template
    for p in participants:
        p_paddle = int(p.id)
        p_id = int(p.user.id)
        p_name = str(p.user.name)
        p_payment = str(p.payment_method)
        p_bids = AuctionBid.objects.filter(bidder = p)
        p_data.append((p_paddle,p_id,p_name,p_payment,len(p_bids)))

    c.update({
        'auction':auction,
        'p_data':p_data})

    return render_to_response('djauction/userpaidview.html',c,
        context_instance=RequestContext(request))

@login_required
def bulk_add_user(request):
    ''' View to add users from an imported CSV file '''

    ''' TODO: Actual MIME-type file enforcement and field validation to reduce
        risk of import attacks '''

    c = {}

    if request.method == 'POST':
        form = ImportFileForm(request.POST, request.FILES)
        if form.is_valid():
            status = []
            file_type = str(request.FILES['file']).split('.')[-1]
            if file_type == 'csv':
                for line in request.FILES['file'].read().split('\n'):
                    line_parts = line.split(',')
                    if len(line_parts) == 3:
                        user, created = AuctionUser.objects.get_or_create(
                            name = line_parts[0], phone = line_parts[1],
                            email = line_parts[2])
                        if created:
                            status.append('User {} added'.format(str(user)))
                        else:
                            status.append('User {} already exists'.format(str(user)))
            else:
                status.append('Unsupported file type')
            c.update({'status':status})
            form = ImportFileForm()
    else:
        form = ImportFileForm()

    c.update({'form':form})

    return render_to_response('djauction/bulkadduser.html',c,
        context_instance=RequestContext(request))

##### Views Interacting with AuctionItems #####

@login_required
def add_item(request, auction_id, user_id):

    ''' View to create a new Item and associate it with an Auction '''

    c = {}

    auction = Auction.objects.get(id=auction_id)
    auction_user = AuctionUser.objects.get(id=user_id)

    c.update({
        'auction':auction,
        'auction_user':auction_user,
        })

    if request.method == 'POST':
        form = AuctionItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.auction = auction
            item.donor = auction_user
            item.save()
            return HttpResponseRedirect(reverse(view_user, args=(auction_user.id,
                auction.id)))
        else:
            c.update({'form':form})
    else:
        form = AuctionItemForm()
        c.update({'form':form})

    return render_to_response('djauction/additem.html',c,
        context_instance=RequestContext(request))

@login_required
def list_items(request,auction_id):

    ''' View to list all items belonging to an auction '''

    c = {}

    auction = Auction.objects.get(id=auction_id)
    items = AuctionItem.objects.filter(auction=auction_id).order_by('auction_event','item_number','name')
    c.update({
        'auction':auction,
        'items':items
        })

    if request.method == 'POST':
        del_items_list = request.POST.getlist('del_items')
        del_items_set = AuctionItem.objects.filter(id__in = del_items_list)
        if 'delete_confirm' in request.POST:
            for item in del_items_set:
                bids = AuctionBid.objects.filter(item=item)
                for bid in bids:
                    bid.delete()
                item.delete()
            return HttpResponseRedirect(reverse('list_items', args=(auction_id,)))
        else:
            c.update({'del_items':del_items_set})
            return render_to_response('djauction/listitems.html',c,
                context_instance=RequestContext(request))

    return render_to_response('djauction/listitems.html',c,
        context_instance=RequestContext(request))

@login_required
def view_item(request, item_id):

    ''' View to get details about an auction item '''

    c = {}

    item = AuctionItem.objects.get(id=item_id)
    donor = AuctionUser.objects.get(id=item.donor.id)
    auction = Auction.objects.get(id=item.auction.id)
    event = AuctionEvent.objects.get(id=item.auction_event.id)
    bids = AuctionBid.objects.filter(item=item)

    event_items = AuctionItem.objects.filter(auction_event=event.id).order_by('item_number')

    # the manual bid form is used to add a bid even if the max winners has been reached
    manual_bid_form = AuctionBidExtraForm(prefix='manual')

    event_item_ids = [event_item.id for event_item in event_items]
    item_index = event_item_ids.index(item.id)
    if (item_index - 1 ) >= 0:
        prev_item = AuctionItem.objects.get(id=event_item_ids[item_index - 1])
        c.update({'prev_item':prev_item})
    if (item_index + 1 ) < len(event_item_ids):
        next_item = AuctionItem.objects.get(id=event_item_ids[item_index + 1])
        c.update({'next_item':next_item})

    c.update({
        'item':item,
        'donor':donor,
        'auction':auction,
        'bids':bids,
        'event_item_ids':event_item_ids,
        'event_items':event_items,
        'item_index':item_index,
        'manual_bid_form':manual_bid_form,
        })

    winners_left = item.valid_winners - len(bids)

    if request.method == 'POST':

        # check if bids are being added and process any non-null entries
        if 'add_bids' in request.POST:
            form = AuctionBidAddForm(request.POST,
                winners=winners_left,
                auction_id=auction.id)
            if form.is_valid():
                for i in xrange(winners_left):
                    user_name = form.cleaned_data['user_%s' % str(i)]
                    user_bid = form.cleaned_data['bid_%s' % str(i)]
                    if (user_name != None) and (user_bid != None):
                        bid = AuctionBid(auction=auction,
                            bidder=user_name, ammount=user_bid,
                            item=item)
                        bid.save()
                return HttpResponseRedirect(reverse(view_item, args=(item.id,)))
            else:
                c.update({'bid_add_form':form})

        # check if bids are being deleted and process any non-null entries
        if 'del_bids' in request.POST:
            form = AuctionBidDelForm(request.POST, item=item)
            if form.is_valid():
                for bid in form.cleaned_data['bids']:
                    bid.delete()
                return HttpResponseRedirect(reverse(view_item, args=(item.id,)))

        # if a manual bid submission was sent, process it here
        if 'manual_add_bid' in request.POST:
            form = AuctionBidExtraForm(request.POST, prefix='manual')
            if form.is_valid():
                bid = form.save(commit=False)
                bid.auction = auction
                bid.item = item
                bid.save()
                return HttpResponseRedirect(reverse(view_item, args=(item.id,)))

    else:
        # create a bid add form only if the current winner count is less than the max
        if winners_left > 0:
            form = AuctionBidAddForm(winners=winners_left,
                auction_id=auction.id)
            c.update({'bid_add_form':form})
        # create a bid delete form if the current winner count is 1 or more
        if len(bids) > 0:
            form = AuctionBidDelForm(item=item)
            c.update({'bid_del_form':form})

    return render_to_response('djauction/viewitem.html', c,
        context_instance=RequestContext(request))

@login_required
def bulk_add_item(request, auction_id):
    ''' View to add items from an imported CSV file '''

    ''' TODO: Actual MIME-type file enforcement and field validation to reduce
        risk of import attacks '''

    c = {}

    auction = Auction.objects.get(id=auction_id)
    c.update({'auction':auction})

    if request.method == 'POST':
        form = ImportFileForm(request.POST, request.FILES)
        if form.is_valid():
            status = []
            file_type = str(request.FILES['file']).split('.')[-1]
            if file_type == 'csv':
                for line in request.FILES['file'].read().split('\n'):
                    line_parts = line.split(',')
                    if len(line_parts) == 9:
                        item, created = AuctionItem.objects.get_or_create(
                            auction = auction,
                            name = line_parts[0],
                            auction_event = AuctionEvent.objects.get(name=line_parts[1],auction=auction),
                            item_number = line_parts[2],
                            item_type = line_parts[3],
                            donor = AuctionUser.objects.get(name=line_parts[4]),
                            valid_winners = line_parts[5],
                            starting_bid = line_parts[6],
                            time_and_location = line_parts[7],
                            conditions = line_parts[8],
                            )
                        if created:
                            status.append('Item {} added'.format(str(item)))
                        else:
                            status.append('Error adding item {}'.format(str(item)))
            else:
                status.append('Unsupported file type')
            c.update({'status':status})
            form = ImportFileForm()
    else:
        form = ImportFileForm()

    c.update({'form':form})

    return render_to_response('djauction/bulkadditem.html',c,
        context_instance=RequestContext(request))

##### Views For Exporting Data #####
@login_required
def export_bids(request, auction_id):

	c = {}

	auction = Auction.objects.get(id=auction_id)
	bids = AuctionBid.objects.filter(auction=auction).order_by('bidder__paddle')

	c.update({
		'auction':auction,
		'bids':bids,
		})

	return render_to_response('djauction/exportbids.html',c,
		context_instance=RequestContext(request))

##### Views For Contacting Users #####

@login_required
def send_email(request):

    ''' View to send reciept email to a user when they check out '''

    ''' TODO: Dead code for now, integrate with template output in future '''

    if request.method == 'POST':
        auction_user = AuctionUser.objects.get(id=user_id)
        auction = Auction.objects.get(id=auction_id)

        msg = MIMEMultipart()
        msg['Subject'] = "Reciept from {}".format(str(auction.name))
        msg['From'] = settings.DJAUCTION_SMTP_USER
        msg['To'] = auction_user.email
        msg_text = ''
        mime_text = MIMEText(msg_text, 'plain')
        msg.attach(mime_text)

        server = smtplib.SMTP(settings.DJAUCTION_SMTP_SERVER, settings.DJAUCTION_SMTP_PORT)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(settings.DJAUCTION_SMTP_USER, settings.DJAUCTION_SMTP_PASS)
        server.sendmail(settings.DJAUCTION_SMTP_USER, auction_user.email, msg.as_string())
        server.close()
        return HttpResponseRedirect(reverse(view_user, args=(auction_user.id,auction.id)))
