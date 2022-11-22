from django.db import models
import uuid

# Product Table Schema: Each object of this class is a product record in the table
class Product(models.Model):
    id = models.UUIDField(verbose_name="id", primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(verbose_name="name", max_length=20, blank=False)
    desc = models.TextField(verbose_name="description", blank=True)
    bid = models.IntegerField(verbose_name="bid",blank=False, default=0)
    img = models.TextField(verbose_name="image", blank=True, default='')
    owner = models.IntegerField(verbose_name="owner_id", blank=False, default=1)
    previousOwner = models.IntegerField(verbose_name="previous_owner", blank=False, default=2)
    running = models.BooleanField(verbose_name="running", blank=False, default=True)
    highestBidder = models.IntegerField(verbose_name="highest_bidder", blank=False, default=1)
