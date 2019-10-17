from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .views import get_client_ip
from .models import profile

@receiver(post_save,sender=User)
def create_profile(sender, instance, created, **kwargs):
        print(instance)
        if created:
                profile.objects.create(user = instance)
        
@receiver(post_save,sender=User)
def save_profile(sender, instance, **kwargs):
        instance.profile.save()
        