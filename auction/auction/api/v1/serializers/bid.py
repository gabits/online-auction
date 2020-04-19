# Third-party
from rest_framework import serializers

# Local
from auction.models import Bid


# Serializers used are all hyperlinked to follow REST API guidelines.
#
# TODO: Change this ModelSerializer to a HyperlinkedModelSerializer after
#  /bids/ and /user/ endpoints are implemented so we can hyperlink them
class BidListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bid


class BidDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bid
