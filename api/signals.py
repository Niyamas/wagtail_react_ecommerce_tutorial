from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User


# Listen for when the User updates.
@receiver(pre_save, sender=User)
def update_user(sender, instance, **kwargs):
    """
    
    """
    print('Signal Triggered')