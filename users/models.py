from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse


# Create your models here
class Details(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    VET = "v"
    OWNER = "o"
    ADMIN = "a"
    USER_ROLES = [
        (VET, "vet"),
        (OWNER, "owner"),
        (ADMIN, "admin"),
    ]
    role = models.CharField(
        max_length=1,
        choices=USER_ROLES,
        default=OWNER
    )
    phone = models.CharField(max_length=11)  # possibly change to phoneNumber?
    clinic_name = models.CharField(max_length=150, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=30)  # possibly utilize localflavor?
    state = models.CharField(max_length=30)
    zip_code = models.CharField(max_length=30, blank=True, null=True)

    def get_absolute_url(self):
        return reverse('users:profile', args=[self.user.username])

@receiver(post_save, sender=User)
def create_user_details(sender, instance, created, **kwargs):
    if created:
        Details.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_details(sender, instance, **kwargs):
    instance.details.save()

class Vet(models.Model):
    email = models.EmailField(max_length=100, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    clinic_name = models.CharField(max_length=100, default="Default Clinic")
    address = models.CharField(max_length=30, default="Default Address")
    city = models.CharField(max_length=30, default="Default City")
    state = models.CharField(max_length=30)
    zip_code = models.CharField(max_length=30, default="00000")
    phone = models.CharField(max_length=10)

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    def is_claimed(self):
        return self.user is not None