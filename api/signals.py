from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User


# Listen for when the User updates.
@receiver(pre_save, sender=User)
def update_user(sender, instance, **kwargs):
    """
    update_user is called before a User object is saved/updated.
    """
    print('Signal Triggered')

    user = instance

    # When a user object is saved/updated and the user's email is not empty, make the username the same as the user's email.

    if user.email != '':
        user.username = user.email