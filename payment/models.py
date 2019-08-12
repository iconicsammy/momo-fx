from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

# Create your models here.

class MomoRequest(models.Model):
    '''
    Payment requests made to consumers. Intially, it will be pending
    '''

    STATUS_TYPE = (('Pending', 'Pending'), ('Confirmed',
                                                'Confirmed'), ('Rejected', 'Rejected'))

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'user_requests')
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length = 200, choices = STATUS_TYPE, default='Pending')
    amount = models.DecimalField(max_digits=5, decimal_places=3)
    transaction_code = models.CharField(max_length = 200, unique = True)


