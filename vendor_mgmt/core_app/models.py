from django.db import models
import uuid

# Create your models here.
class VendorProfile(models.Model):
    name = models.CharField(max_length=50,default = None)
    contact_details = models.TextField(blank = True, null = True,default= "")
    address = models.TextField(blank= True, null = True,default = "")
    vendor_code = models.CharField(max_length=8, unique = True,blank= True)
    on_time_delivery_rate = models.FloatField(default = 0.0)
    quality_rating_avg = models.FloatField(default = 0.0)
    average_response_time = models.FloatField(default = 0.0)
    fullfillment_rate = models.FloatField(default = 0.0)

    def __str__(self) -> str:
        return self.name

    
    def save(self, *args, **kwargs):
        if not self.vendor_code:
            # Generate a UUID and truncate to 8 characters
            generated_uuid = str(uuid.uuid4())[:8]
            self.vendor_code = generated_uuid
        super().save(*args, **kwargs)

class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=20, unique=True)
    vendor = models.ForeignKey(VendorProfile, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=20)
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(VendorProfile, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()
