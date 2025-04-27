import os
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.conf import settings
from django.urls import reverse

from users.models import Vet

# Create your models here.

def _delete_old_file(file):
    if file and hasattr(file, 'path') and os.path.isfile(file.path):
        os.remove(file.path)

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
    vet = models.ForeignKey(Vet, on_delete=models.SET_NULL, null=True, blank=True, related_name='pets_vet')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='pets_owner')
    last_updated = models.DateTimeField(auto_now=True)
    non_owners = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='authorized_users', blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('pets:pet-details', args=[self.id])

    def get_user_relation(self, user):
        if self.owner == user:
            return 'owner'
        elif self.vet == user:
            return 'vet'
        elif user in self.non_owners.all():
            return 'sitter'
        return 'unauthorized'

    # check if current pfp is different from old pfp. if so, delete old pfp
    def save(self, *args, **kwargs):
        try:
            old = Pet.objects.get(pk=self.pk)
            if old.pfp and old.pfp != self.pfp:
                _delete_old_file(old.pfp)
        except Pet.DoesNotExist:
            pass
        super().save(*args, **kwargs)

# delete pet pfp if pet is deleted
@receiver(post_delete, sender=Pet)
def delete_pet_pfp_file(sender, instance, **kwargs):
    _delete_old_file(instance.pfp)

class Condition(models.Model):
    pet = models.ForeignKey('Pet', on_delete=models.CASCADE, related_name='conditions')
    title = models.CharField(max_length=30)
    description = models.TextField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('pets:pet-details', args=[self.pet.id])

class Vaccine(models.Model):
    pet = models.ForeignKey('Pet', on_delete=models.CASCADE, related_name='vaccines')
    name = models.CharField(max_length=30)
    last_done = models.DateTimeField()
    next_due = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('pets:pet-details', args=[self.pet.id])
