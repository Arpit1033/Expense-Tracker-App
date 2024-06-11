from django.dispatch import receiver
from allauth.account.signals import user_signed_up
from .models import Profile

@receiver(user_signed_up)
def create_profile_on_social_signup(request, user, **kwargs):
    Profile.objects.get_or_create(user=user)