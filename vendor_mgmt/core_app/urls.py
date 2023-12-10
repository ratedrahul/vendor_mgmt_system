from django.urls import path
from .views import VendorView, VendorInfoViewSet, MyVendor, PurchaseOrderListCreateView,PurchaseOrderDetailView,PurchaseOrderListViewByVendor,VendorPerformanceView,AcknowledgePurchaseOrderView


urlpatterns = [
    path('vendors/', VendorView.as_view()),
    path('vendors/<int:pk>/',MyVendor.as_view({'get':'custom_get_method','put':'update','delete':'destroy'})),
    path('purchase_orders/', PurchaseOrderListCreateView.as_view(), name='purchase_order_list_create'),
    path('purchase_orders/<int:pk>/', PurchaseOrderDetailView.as_view(), name='purchase_order_detail'),
    path('purchase_orders/vendor/<int:vendor_id>/', PurchaseOrderListViewByVendor.as_view(), name='purchase_order_list_by_vendor'),
    path('vendors/', VendorView.as_view(), name='vendor_list_create'),
    path('vendors/<int:vendor_id>/performance/', VendorPerformanceView.as_view(), name='vendor_performance'),
    path('purchase_orders/<int:po_id>/acknowledge/', AcknowledgePurchaseOrderView.as_view(), name='acknowledge_purchase_order'),


]


