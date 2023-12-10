from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from .serializers import VendorProfileSerializer, PurchaseOrderSerializer
from .models import VendorProfile,PurchaseOrder
from django.http import HttpResponse
from rest_framework.decorators import action
from django.utils import timezone
from django.db.models import Avg, F, Case, When, Value, FloatField
from django.db import models
from rest_framework import viewsets

class VendorView(APIView):
    def get(self,request,*args,**kwargs):
        vendors = VendorProfile.objects.all()
        serializer = VendorProfileSerializer(vendors, many = True)
        # return Response(serializer.data)
        # return HttpResponse(serializer.data)
        return Response({
            'status': 'success',
            'message': 'Vendors retrieved successfully',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    
    def post(self, request, *args, **kwargs):
        serializer = VendorProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VendorInfoViewSet(viewsets.GenericViewSet, ListModelMixin, CreateModelMixin):
    queryset = VendorProfile.objects.all()
    serializer_class = VendorProfileSerializer


class MyVendor(viewsets.ModelViewSet):
    queryset = VendorProfile.objects.all()
    serializer_class = VendorProfileSerializer

    @action(detail=False,methods=["GET"])
    def custom_get_method(self,request,pk = None):
        instance = self.get_object()
        return Response({'detail': f'Custom method for GET executed successfully:\n{instance.__dict__}'})

    @action(detail=False,methods=["PUT"])
    def update(self, request, *args, **kwargs):
        # Your custom logic for PUT method here
        response = super().update(request, *args, **kwargs)
        return response

    def destroy(self, request, *args, **kwargs):
        # Your custom logic for DELETE method here
        response = super().destroy(request, *args, **kwargs)
        return response


class PurchaseOrderListCreateView(generics.ListCreateAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

class PurchaseOrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

class PurchaseOrderListViewByVendor(generics.ListAPIView):
    serializer_class = PurchaseOrderSerializer

    def get_queryset(self):
        vendor_id = self.kwargs['vendor_id']
        return PurchaseOrder.objects.filter(vendor__id=vendor_id)


class VendorPerformanceView(APIView):
    def get(self, request, *args, **kwargs):
        vendor_id = kwargs.get('vendor_id')
        try:
            vendor = VendorProfile.objects.get(pk=vendor_id)
            serializer = VendorProfileSerializer(vendor)
            return Response({
                'on_time_delivery_rate': vendor.on_time_delivery_rate,
                'quality_rating_avg': vendor.quality_rating_avg,
                'average_response_time': vendor.average_response_time,
                'fullfillment_rate': vendor.fullfillment_rate,
            })
        except VendorProfile.DoesNotExist:
            return Response({"error": "Vendor not found"}, status=404)


class AcknowledgePurchaseOrderView(APIView):
    def post(self, request, *args, **kwargs):
        po_id = kwargs.get('po_id')
        try:
            po = PurchaseOrder.objects.get(pk=po_id)
            po.acknowledgment_date = timezone.now()
            po.save()
            return Response({"success": "Purchase Order acknowledged successfully."})
        except PurchaseOrder.DoesNotExist:
            return Response({"error": "Purchase Order not found"}, status=404)


class VendorPerformanceView(APIView):
    def get(self, request, *args, **kwargs):
        vendor_id = kwargs.get('vendor_id')
        try:
            vendor = VendorProfile.objects.get(pk=vendor_id)
            
            completed_orders = PurchaseOrder.objects.filter(vendor=vendor, status='completed').select_related('vendor')
            
            on_time_delivery_rate = completed_orders.annotate(
                on_time_delivery=Case(
                    When(delivery_date__lte=F('acknowledgment_date'), then=Value(1)),
                    default=Value(0),
                    output_field=models.FloatField(),
                )
            ).aggregate(on_time_delivery_rate=Avg('on_time_delivery'))['on_time_delivery_rate'] or 0.0

            quality_rating_avg = completed_orders.exclude(quality_rating__isnull=True).aggregate(avg_quality=Avg('quality_rating'))['avg_quality'] or 0.0

            avg_response_time = completed_orders.exclude(acknowledgment_date__isnull=True).aggregate(avg_time=Avg(F('acknowledgment_date') - F('issue_date'), output_field=models.DurationField()))['avg_time'] or 0.0

            fulfillment_rate = completed_orders.annotate(
                fulfilled=Case(
                    When(status='completed', issue_date__lte=F('acknowledgment_date'), then=Value(1)),
                    default=Value(0),
                    output_field=models.FloatField(),
                )
            ).aggregate(fulfillment_rate=Avg('fulfilled'))['fulfillment_rate'] or 0.0

            return Response({
                'on_time_delivery_rate': on_time_delivery_rate,
                'quality_rating_avg': quality_rating_avg,
                'average_response_time': avg_response_time.total_seconds() if avg_response_time else 0.0,
                'fulfillment_rate': fulfillment_rate,
            })
        except VendorProfile.DoesNotExist:
            return Response({"error": "Vendor not found"}, status=404)
