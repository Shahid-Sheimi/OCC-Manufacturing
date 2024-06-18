from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UploadSTPFileView,
    ProductRetrieveUpdateDestroyAPIView,
    ProductConfigViewSet,SelectManufacturerViewSet,OrderSummaryViewset,QuoteViewSet
)

# Create a router and register our viewsets with it.
router = DefaultRouter()

router.register(r'product-config', ProductConfigViewSet, basename='product-config')
router.register(r'select-manufacturer',SelectManufacturerViewSet,basename = 'select-manufacturer')

router.register(r'order-summary',OrderSummaryViewset, basename='order-summary')
router.register(r'quote-summary',QuoteViewSet, basename='quote-summary')

urlpatterns = [
    path('', include(router.urls)),
    # Product URLs
    path('products/', UploadSTPFileView.as_view(), name='upload-stp-file'),
    path('products/<int:pk>/', ProductRetrieveUpdateDestroyAPIView.as_view(), name='product_detail'),
    
]





