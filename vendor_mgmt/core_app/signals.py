from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import PurchaseOrder

@receiver(post_save, sender=PurchaseOrder)
@receiver(post_delete, sender=PurchaseOrder)
def recalculate_metrics(sender, instance, **kwargs):
    if instance.vendor:
        instance.vendor.save()
