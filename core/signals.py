from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from .models import User

@receiver(pre_save, sender=User)
def delete_old_image(sender, instance, **kwargs):
    if not instance.pk:
        return  # new user, no old image

    try:
        old_user = User.objects.get(pk=instance.pk)
    except User.DoesNotExist:
        return

    # If image changed, delete the old file
    if old_user.image and old_user.image != instance.image:
        old_user.image.delete(save=False)

@receiver(post_delete, sender=User)
def delete_image_on_user_delete(sender, instance, **kwargs):
    if instance.image and instance.image.name != "defaults/user.png":
        instance.image.delete(save=False)
