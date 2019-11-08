from django.views import View
from django.http import HttpResponse, HttpResponseRedirect
from .forms import AuctionForm, EditAuctionForm, BiddingForm
from .models import Auction, Bidder
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta, timezone
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import translation
from django.utils.translation import gettext as _


def index(request):
    print(request.headers)
    print("creating response...")
    html = "<html><body>Hello! <br> <p> This was your request: %s %s <p> sent from the following browser: %s </body></html>" % (
    request.method, request.path, request.headers['User-Agent'])
    return HttpResponse(html)


def search(request):
    search_term = request.POST
    matching_auctions = Auction.objects.all().filter(Auction.item.__contains__(search_term))
    if len(matching_auctions) < 1 and search_term != ' ':
        messages.add_message(request, messages.INFO, _("No auctions found"))
        return render(request, 'auctions.html')
    else:
        return render(request, 'searchresults.html', {"matching_auctions": matching_auctions})


@method_decorator(login_required, name="dispatch")
class CreateAuction(View):
    def get(self, request):
        form = AuctionForm()
        return render(request, "createauction.html", {"form": AuctionForm})

    def post(self, request):
        form = AuctionForm(request.POST)
        user = request.user
        username = request.user.username
        if form.is_valid():
            form_data = form.cleaned_data
            a_item = form_data["item"]
            a_description = form_data["description"]
            a_minimum_price = form_data["minimum_price"]
            a_deadline_date = form_data["deadline_date"]
            current_date = datetime.now(timezone.utc)
            auction_date = datetime.strptime(a_deadline_date, "%d-%m-%Y %H:%M:%S").astimezone(timezone.utc)
            difference = auction_date - current_date
            if difference < timedelta(hours=72):
                messages.add_message(request, messages.INFO, _("Invalid deadline"))
                return HttpResponseRedirect("createauction.html", status=400)
            else:
                send_mail('Auction created', 'Your auction has been successfully created, use this link to edit',
                          'yaas@dontreply.com', [user.email])
                auction = Auction(item=a_item, description=a_description, status="Active", minimum_price=a_minimum_price,
                                  deadline_date=auction_date, creator=username, highest_bidder_id=-1)
                auction.save()
                return render(request, "home.html")

        else:
            return render(request, "trololoo.html")


@method_decorator(login_required, name="dispatch")
class EditAuction(View):
    def get(self, request, item_id):
        auction = get_object_or_404(Auction, id=item_id)
        if auction.status == "Active" and auction.creator == request.user.username:
            return render(request, "editauction.html", {"description": auction.description, "form": EditAuctionForm},
                          auction)
        else:
            messages.add_message(request, messages.INFO,
                                 _("You are not authorized to edit this auction or the auction has already expired"))
            return render(request, 'home.html')

    def post(self, request, item_id):
        form = EditAuctionForm(request.POST)
        auction = get_object_or_404(Auction, id=item_id)
        if form.is_valid():
            cd = form.cleaned_data
            a_newdesc = cd["new_description"]
            auction.description = a_newdesc
            auction.save()
            return render(request, "home.html")


@login_required()
def bid(request, item_id):
    user = request.user
    auction = get_object_or_404(Auction, id=item_id)
    bid_amount = request.POST.get('bid_amount')
    if auction.status != 'Active':
        messages.add_message(request, messages.INFO, _("You can only bid on active auctions"))
        return render(request, "auctions.html", {"form": BiddingForm})
    if auction.creator == user.username:
        messages.add_message(request, messages.INFO, _("You cannot bid on your own auction"))
        return render(request, "auctions.html", {"form": BiddingForm})
    if auction.minimum_price >= float(bid_amount):
        messages.add_message(request, messages.INFO, _("There already exists a higher bid"))
        return render(request, "auctions.html")
    if auction.highest_bidder_id == user.id:
        messages.add_message(request, messages.INFO, _("You are already the highest bidder"))
        return render(request, "auctions.html")
    if len(bid_amount.rsplit('.')[-1]) > 2:
        messages.add_message(request, messages.INFO, _("Too many decimals, "
                                                       "you can only specify bids with maximum of two decimals"))
        return render(request, "auctions.html")
    else:
        creator = User.objects.filter(username=auction.creator).first()
        send_mail('Auction update', 'A bid has been placed on your auction', 'yaas@dontreply.com', [creator.email])
        bidder = Bidder(auction_id=item_id, bidder=user.id)
        auction.minimum_price = bid_amount
        auction.highest_bidder_id = user.id
        bidder.save()
        auction.save()
        messages.add_message(request, messages.INFO, _("Successfully bidded on auction"))
        if auction.highest_bidder_id != -1:
            prev_bidder = User.objects.filter(id=auction.highest_bidder_id).first()
            send_mail('You have been outbidded', 'Your bid on an auction has been exceeded',
                      'yaas@dontreply.com', [prev_bidder.email])
        return HttpResponseRedirect(reverse("home"))


def ban(request, item_id):
    user = request.user
    if user.is_superuser:
        auction = Auction.objects.filter(id=item_id)
        auction.status = "Banned"
        auction.save()
        return HttpResponseRedirect(reverse("home"))
    else:
        messages.add_message(request, messages.INFO, _("Only moderators can ban auctions"))
        return HttpResponseRedirect(reverse("home"))


def resolve(request):
    pass


def changeLanguage(request, lang_code):
    translation.activate(lang_code)
    request.session[translation.LANGUAGE_SESSION_KEY] = lang_code
    messages.add_message(request, messages.INFO, _("Language changed successfully" + lang_code))
    return HttpResponseRedirect(reverse("home"))


def changeCurrency(request, currency_code):
    currency = currency_code
    currencies = {'EUR', 'USD'}


def browseAuctions(request):
    auctions = Auction.objects.order_by('item')
    return render(request, "auctions.html", {"auctions": auctions})

