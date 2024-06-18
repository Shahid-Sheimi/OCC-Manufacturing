from django.shortcuts import render
from rest_framework import viewsets
from authentication.models import User
from admin_panel.serializers import UserSerializer

from admin_panel.permissions import NoPostPermission, IsAdminOrMember
from rest_framework import mixins
from datetime import datetime

from process_occ.models import Order, Quote
from .serializers import QuoteSerializer, LastOrderdSerializer, ActiveOrerdSerializer

from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema


# Create your views here.


class CustomerDashboard(viewsets.GenericViewSet,
                        mixins.ListModelMixin,):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [NoPostPermission,IsAdminOrMember]
    
    @swagger_auto_schema(responses={200: UserSerializer(many=True)})
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Quote.objects.none()  # Return an empty queryset for Swagger
        return Quote.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            self.queryset = Quote.objects.all()
            return QuoteSerializer
        
        return super().get_serializer_class()

    def list(self, request, *args, **kwargs):
        if getattr(self, 'swagger_fake_view', False):
            return Response([])  # Return an empty response or mock data for Swagger
        
        queryset = User.objects.filter(id=self.request.user.id).first()
        serialized_user = UserSerializer(queryset)

        orders = Order.objects.filter(user=queryset)
        last_order = Quote.objects.filter(user=queryset).last()
        serialized_last_order = LastOrderdSerializer(last_order)

        active_orders = Order.objects.filter(user=queryset, active=True)
        serialized_orders = ActiveOrerdSerializer(active_orders, many=True)

        active_orders_count = 0
        order_in_transit = 0
        order_delivered = 0

        for order in orders:
            if order.active:
                active_orders_count += 1
            

            if order.current_status == 'shipping':
                order_in_transit += 1

            if order.is_delivered:
                order_delivered += 1

        quotes = Quote.objects.filter(user=queryset)
        serialized_quotes = QuoteSerializer(quotes, many=True)


        amount  = 0
        for quote in quotes:
            amount += quote.order_total

        configs = orders[0].products.all().first()

        print(type(configs))

        output = {
            'active_orders_count' : active_orders_count,
            'order_in_transit': order_in_transit,
            'order_delivered':order_delivered,
            'total Order' :len(orders), 
            'user' : serialized_user.data,
            'Active orders' : serialized_orders.data,
            'quotes' : serialized_quotes.data,
            'amount' : amount,
            'serialized_last_order' : serialized_last_order.data
        }

        return Response (output)

        # return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(responses={200: UserSerializer(many=True)})
    def retrieve(self, request, *args, **kwargs):
        # print(self.get_queryset)
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        if instance:
            quote_summary = {
                "Material" : instance.order_id.products.all().first().material.name,
                "Heat Treatment": instance.order_id.products.all().first().heat_treatment.name,
                "Coatings" : instance.order_id.products.all().first().coating.name,
                "Inspection" : instance.order_id.products.all().first().inspection.name,
                "Lead Time" : instance.lead_time.strftime("%B %d, %Y"),
                "Manufacturing Location" : instance.order_id.products.all().first().country.name,
                "Carbon footprint CO2" : instance.carbon_footprint,
                "Cost to offset Carbon" : instance.cost_to_carbon
            }
            order_summary = {
                "Order id" : instance.order_id.order_id,
                "Order date" : instance.created_at,
                "Order by" : instance.user.username,
                "Payment method" : instance.payment_method,
                "Total Parts" : instance.total_parts,
                "Total Quantity" : instance.total_quantity,
                "Order Total " : instance.order_total                   
                                }
            track_summary = [
                {"date_time ": datetime.now().strftime("%B %d, %Y"),
                 "address" : "abc"
                 },
                {"date_time ": 123,
                 "address" : "abc"
                 },
                {"date_time ": 123,
                 "address" : "abc"
                 }
            ]

            output = {
                "quote_summary" : quote_summary,
                "order_summary" : order_summary,
                "track_summary" : track_summary
            }
            return Response (output)

        return Response ("Quote with id : not found")