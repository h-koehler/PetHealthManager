from enum import Enum
from datetime import datetime, timedelta
from django.db import models


# Create your models here.

class Pet(models.Model):
    name = models.CharField(max_length=30)
    DOG = "d"
    CAT = "c"
    FISH = "f"
    SMALL = "s"
    BIRD = "b"
    REPTILE = "r"
    PET_TYPE_CHOICES = [
        (DOG, "Dog"),
        (CAT, "Cat"),
        (FISH, "Fish"),
        (SMALL, "Small Mammal"),
        (BIRD, "Bird"),
        (REPTILE, "Reptile"),
    ]
    type = models.CharField(
        max_length=1,
        choices=PET_TYPE_CHOICES,
        default=DOG
    )
    breed = models.CharField(max_length=30)
    FEMALE = "f"
    MALE = "m"
    PET_SEX_CHOICES = [
        (FEMALE, "Female"),
        (MALE, "Male"),
    ]
    sex = models.CharField(
        max_length=1,
        choices=PET_SEX_CHOICES,
        default=FEMALE
    )
    pfp = models.ImageField(upload_to="pet_profiles/", null=True, blank=True)
    dob = models.DateTimeField()
    weight = models.FloatField()
    spayed = models.BooleanField(default=False)
    vet = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, blank=True, related_name='pets_as_vet')
    owner = models.ForeignKey('User', on_delete=models.CASCADE, related_name='pets_as_owner')
    lastUpdated = models.DateTimeField(auto_now=True)
    nonOwners = models.ManyToManyField('User', related_name='pets_as_sitters', blank=True)

    def get_user_relation(self, user):
        if self.owner == user:
            return 'owner'
        elif self.vet == user:
            return 'vet'
        elif user in self.nonOwners.all():
            return 'sitter'
        return 'unauthorized'

class User(models.Model):
    VET = "v"
    OWNER = "o"
    SITTER = "s"
    USER_ROLES = [
        (VET, "vet"),
        (OWNER, "owner"),
        (SITTER, "sitter"),
    ]
    role = models.CharField(
        max_length=1,
        choices=USER_ROLES,
        default=OWNER
    )
    firstName = models.CharField(max_length=30)
    lastName = models.CharField(max_length=30)
    phone = models.CharField(max_length=11) # possibly change to phoneNumber?
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=30)
    city = models.CharField(max_length=30) # possibly utilize localflavor?
    state = models.CharField(max_length=30)
    zipCode = models.CharField(max_length=30)
    username = models.CharField(max_length=30, null=True, blank=True, unique=True)

class Condition(models.Model):
    pet = models.ForeignKey('Pet', on_delete=models.CASCADE, related_name='conditions')
    title = models.CharField(max_length=30)
    description = models.TextField()

class Vaccine(models.Model):
    pet = models.ForeignKey('Pet', on_delete=models.CASCADE, related_name='vaccines')
    name = models.CharField(max_length=30)
    lastDone = models.DateTimeField()
    nextDue = models.DateTimeField()

class FeedItem(models.Model):
    GENERAL = "gen"
    INQUIRY = 'inq'
    FEED_TYPE_CHOICES = [
        (GENERAL, "General Update"),
        (INQUIRY, "Inquiry to Vet"),
    ]
    title = models.CharField(max_length=100)
    description = models.TextField()
    pet = models.ForeignKey('Pet', on_delete=models.CASCADE, related_name='feed_items')
    created_by = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, blank=True, related_name='feed_items_created_by')
    feed_type = models.CharField(max_length=3, choices=FEED_TYPE_CHOICES, default=GENERAL)
    # comments
    dateCreated = models.DateTimeField(auto_now_add=True)
    isSolved = models.BooleanField(default=False)

owner_user = {"username": "john", "password": "owner"}
vet_user = {"username": "jane", "password": "vet"}