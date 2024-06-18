        
from  rest_framework.routers import DefaultRouter
from .views import CustomerDashboard
from django.urls import path, include



router = DefaultRouter()


router.register(r'customer-dashboard', CustomerDashboard, basename='manage_roles')


urlpatterns = [
    path('', include(router.urls)),
]