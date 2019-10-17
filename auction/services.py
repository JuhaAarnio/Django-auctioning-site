from rest_framework.views import APIView
from rest_framework.authentication import BasicAuthentication
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view, renderer_classes, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from auction.models import Auction
from auction.serializers import SerializeAuctions


@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
@renderer_classes([JSONRenderer])
class BrowseAuctionApi(APIView):
    def post(self, request):
        auctions = Auction.objects.all()
        serializer = SerializeAuctions(auctions, many=True)
        return Response(serializer.data)


class SearchAuctionApi(APIView):
    pass


class SearchAuctionWithTermApi(APIView):
    pass


class SearchAuctionApiById(APIView):
    pass


class BidAuctionApi(APIView):
    pass
