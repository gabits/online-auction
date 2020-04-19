# # Django
# from django.contrib.auth import get_user_model
# from django.db.models.signals import post_save
# from django.dispatch import receiver
#
# # Local
# from account.models import UserProfile
# from auction.models import Bid
#
#
# @receiver(post_save, sender=Bid)
# def increase_highest_bid(
#         sender, instance=None, created=False, **kwargs
# ):
#     """
#     Recalculate the highest_bid recorded for a Lot every time a new Bid is
#     created in the system.
#     """
#     if created:
#         instance.lot.highest_bid
