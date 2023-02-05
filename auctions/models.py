from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import AbstractUser
from django.db import models

fs = FileSystemStorage(location='/images')

class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.TextField(max_length=30)
    description = models.TextField(max_length=100)
    starting_bid = models.IntegerField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.title

class Bid(models.Model):
    object = models.ForeignKey(Listing, on_delete=models.CASCADE, default=None)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    amount = models.IntegerField()

    def __int__(self):
        return self.amount

class Comment(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    text = models.TextField(max_length=200)
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.text

class Watchlist(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.listing_id

class Image(models.Model):
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE, default=None)
    image = models.ImageField(default="commerce_1_Diagram.drawio.png", upload_to='images/')

    def __png__(self):
        return self.picture

