from django.views import View
from django.http import HttpResponse, HttpResponseRedirect
from .forms import AuctionForm, EditAuctionForm, BiddingForm
from .models import Auction, Bidder
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta, timezone
from django.core import mail
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
    pass


@method_decorator(login_required, name="dispatch")
class CreateAuction(View):
    def get(self, request):
        form = AuctionForm()
        return render(request, "createauction.html", {"form": AuctionForm})

    def post(self, request):
        form = AuctionForm(request.POST)
        user = request.user
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
                messages.add_message(request, messages.INFO, "Invalid deadline")
                return HttpResponseRedirect("createauction.html",status=400)
            else:
                connection = mail.get_connection()
                message = mail.EmailMessage(
                    'Auction created',
                    'Your auction has been successfully created, use this link to edit',
                    'yaas@dontreply.com',
                    [user.email]
                )
                connection.send_messages(message)
                auction = Auction(item=a_item, description=a_description, status="Active",
                                  minimum_price=a_minimum_price, deadline_date=auction_date, creator_id=user)
                auction.save()
                return render(request, "home.html")

        else:
            return render(request, "trololoo.html")


@method_decorator(login_required, name="dispatch")
class EditAuction(View):
    def get(self, request, item_id):
        auction = get_object_or_404(Auction, id=item_id)
        if auction.status == "Active" and auction.creator_id == request.user.id:
            return render(request, "editauction.html", {"description": auction.description}, auction)
        else:
            messages.add_message(request, messages.INFO,
                                 "You are not authorized to edit this auction or the auction has already expired")

    def post(self, request, item_id):
        form = EditAuctionForm(request.POST)
        auction = get_object_or_404(Auction, id=item_id)
        if form.is_valid():
            cd = form.cleaned_data
            a_newdesc = cd["new_description"]
            auction.description = a_newdesc
            return render(request, "home.html")


def bid(request, item_id):
    user_id = request.user.id
    auction = get_object_or_404(Auction, id=item_id)
    if auction.status is not "Active":
        messages.add_message(request, messages.INFO, "You can only bid on active auctions")
        return render(request, "bidding.html", {"form": BiddingForm})
    if auction.creator_id == user_id:
        messages.add_message(request, messages.INFO, "You cannot bid on your own auction")
        return render(request, "bidding.html", {"form": BiddingForm})
    else:
        bidder = Bidder(auction_id=item_id, bidder_id=user_id)
        bidder.save()
        messages.add_message(request, messages.INFO, "Successfully bidded on auction")


def ban(request, item_id):
    auction = Auction.objects.filter(id=item_id)
    auction.status = "Banned"
    auction.save()


def resolve(request):
    pass


def changeLanguage(request, lang_code):
    translation.activate(lang_code)
    request.session[translation.LANGUAGE_SESSION_KEY] = lang_code
    messages.add_message(request, messages.INFO, "Language changed successfully")
    return HttpResponseRedirect(reverse("home"))



def changeCurrency(request, currency_code):
    pass


def browseAuctions(request):
    auctions = Auction.objects.order_by('item')
    return render(request, "auctions.html", {"auctions": auctions})

