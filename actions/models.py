from django.contrib.auth.models import User
from django.db import models
from pets.models import Pet
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# Create your models here.

class Action(models.Model):
    # CREATE = 'c'
    # UPDATE = 'u'
    # DELETE = 'd'
    # REQUEST = 'r'
    # ACTION_TYPES = [
    #     (CREATE, 'create'),
    #     (UPDATE, 'update'),
    #     (DELETE, 'delete'),
    #     (REQUEST, 'request'),
    # ]
    # type = models.CharField(max_length=1, choices=ACTION_TYPES, default=UPDATE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    verb = models.CharField(max_length=150)
    target_ct = models.ForeignKey(ContentType,
                                  on_delete=models.CASCADE,
                                  blank=True,
                                  null=True)
    target_id = models.PositiveIntegerField(blank=True, null=True)
    target = GenericForeignKey('target_ct', 'target_id')
    created = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)