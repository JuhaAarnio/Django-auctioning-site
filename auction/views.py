from django.views import View
from django.http import HttpResponse, HttpResponseRedirect
from .forms import AuctionForm
from .models import Auction
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta, timezone



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
        user_id = request.user.id
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
                auction = Auction(item=a_item, description=a_description, status="Active",
                                  minimum_price=a_minimum_price, deadline_date=auction_date, creator_id=user_id )
                auction.save()
                return render(request, "home.html")

        else:
            return render(request, "trololoo.html")




@method_decorator(login_required, name="dispatch")
class EditAuction(View):
    def get(self, request, id):
        auction = get_object_or_404(Auction, id=id)
        if auction.status == "Active" and auction.creator_id == request.user.id:
            return render(request, "editauction.html", {"description": auction.description})
        else:
            messages.add_message(request, messages.INFO,
                                 "You are not authorized to edit this auction or the auction has already expired")


def bid(request, item_id):
    pass


def ban(request, item_id):
    pass


def resolve(request):
    pass


def changeLanguage(request, lang_code):
    pass


def changeCurrency(request, currency_code):
    pass


def browseAuctions(request):
    auctions = Auction.objects.order_by('item')
    return render(request, "auctions.html",{"auctions": auctions})

