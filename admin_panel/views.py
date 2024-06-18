from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import viewsets, status
from rest_framework.response import Response
import os
from django.db.models import Q,Sum,F,FloatField

from django.conf import settings
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
# from .permissions import IsOwnerOrAdmin
from rest_framework_simplejwt.authentication import JWTAuthentication 
from .serializers import UserRoleSerializer, UserSerializer, ManageCustomerSerializer, \
    ManageQuoteSerializer, ManageQuoteUpdateSerializer, ManageOrderSerilizer, OrderDetailSerializer,\
         ManageTransactionSerializer, ManageShippingSerializer, ShippingSerializer,\
         MaterialSerializer,HeatTreatmentsSerializer,InspectionSerializer,ParentMaterialSerializer,FinishSerializer,TransactionSerializer,\
         ManageCarbonOffSetSerializer
         
         

from authentication.models import User
from rest_framework.pagination import PageNumberPagination
from .permissions import IsAdminOrMember, NoPostPermission
from process_occ.models import Quote, Order, Manufacturer,Tolerance,ParentMaterial,Material,Product,CountryCO2Intensity,\
    ShippingAddress, HeatTreatment,Inspections,Coatings,Country,ManufacturerLead
from rest_framework.response import Response
import json
from payments.models import Transaction
from .models import Shipping,CarbonOffset
from process_occ.serializers import ManufacturerSerializer,ToleranceSerializer ,\
CountryCO2IntensitySerializer,ShippingAddressSerializer,\
 CountrySerializer, ManufacturerSerializerCreate,ManufacturerLeadSerializer
from rest_framework import mixins

# Create your views here.

class ManageUserOrRoles(viewsets.GenericViewSet,
                        mixins.ListModelMixin,
                        mixins.DestroyModelMixin,
                        mixins.UpdateModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    pagination_class.page_size = 10
    permission_classes = [NoPostPermission,IsAdminOrMember]

    def get_serializer_class(self):
        if getattr(self, 'swagger_fake_view', False):
            return UserSerializer
        if self.action == 'update':
            return UserRoleSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return User.objects.none()
        return super().get_queryset()
    

class ManageCustomerViewset(viewsets.GenericViewSet,
                        mixins.ListModelMixin,
                        mixins.DestroyModelMixin,
                        ):
    serializer_class = ManageCustomerSerializer
    permission_classes = [IsAdminOrMember]

    def get_queryset(self):
        return User.objects.filter(role='customer')
    

class ManageQuoteViewset(viewsets.GenericViewSet,
                        mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin):
    queryset = Quote.objects.all()
    serializer_class = ManageQuoteSerializer
    permission_classes = [IsAdminOrMember]
    
    @swagger_auto_schema(responses={200: ManageQuoteSerializer(many=True)})

    def get_serializer_class(self):
        if self.action == 'update':
            return ManageQuoteUpdateSerializer
        
        return super().get_serializer_class()
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        product = instance.products.all().first()
        
        output = json.loads(json.dumps(serializer.data))

        if product:
            output.update({
                "material" : product.material.name,
                "cost_to_offset_carbon" : instance.cost_to_carbon,
                "carbon_footprint" : instance.carbon_footprint,
                "heat_treatment" : product.heat_treatment.name,
                "coatings" : product.coating.name,
                "inspection" : product.inspection.name,
                "lead_time" : instance.lead_time,
                "manufacturing_location" : instance.manufacturing_location.name,
                "customer_name" : instance.user.username,
                "payment" : instance.payment_method,
                "order_total" : instance.order_total
                 })
        return Response(output) 


class ManageOrdersViewSet(viewsets.GenericViewSet,
                        mixins.ListModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.DestroyModelMixin):
    queryset = Order.objects.all()
    serializer_class = ManageOrderSerilizer
    permission_classes = [IsAdminOrMember]

    @swagger_auto_schema(responses={200: ManageOrderSerilizer(many=True)})
    def get_serializer_class(self):
        if self.action == 'update':
            return ManageQuoteUpdateSerializer
        if self.action == 'retrieve':
            return OrderDetailSerializer
        return super().get_serializer_class()
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        product = instance.products.all().first()
        
        output = json.loads(json.dumps(serializer.data))

        if product:
            output.update({
                "material" : product.material.name,

                 })
        return Response(output) 
    

class ManageTransactionViewSet(viewsets.GenericViewSet,
                        mixins.ListModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.DestroyModelMixin):
    queryset = Transaction.objects.all()
    serializer_class = ManageTransactionSerializer
    permission_classes = [IsAdminOrMember]
  
class ManageShipping(viewsets.GenericViewSet,
                        mixins.ListModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.DestroyModelMixin):
    queryset = Shipping.objects.all()
    serializer_class = ManageShippingSerializer
    permission_classes = [IsAdminOrMember]
    
    @swagger_auto_schema(responses={200: ManageShippingSerializer(many=True)})
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ShippingSerializer
        return super().get_serializer_class()
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        return Response(serializer.data) 


class ManageManufacturer(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminOrMember]
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer

    def get_serializer_class(self):
        if self.action == "create":
            return ManufacturerSerializerCreate
        return super().get_serializer_class()

    @swagger_auto_schema(
        operation_summary="List all manufacturers",
        responses={200: ManufacturerSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve a manufacturer",
        responses={200: ManufacturerSerializer}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create a manufacturer",
        request_body=ManufacturerSerializer,
        responses={201: ManufacturerSerializer}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update a manufacturer",
        request_body=ManufacturerSerializer,
        responses={200: ManufacturerSerializer}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete a manufacturer",
        responses={204: 'No Content'}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

class ManufacturerLeadViewset(viewsets.ModelViewSet):
    queryset= ManufacturerLead.objects.all()
    serializer_class = ManufacturerLeadSerializer


class ManageParentMaterial(viewsets.GenericViewSet,
                        mixins.ListModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin):
    permission_classes = [IsAuthenticated]
    permission_classes = [IsAdminOrMember]

    queryset = ParentMaterial.objects.all()
    serializer_class = ParentMaterialSerializer
    
    @swagger_auto_schema(responses={200: ParentMaterialSerializer(many=True)})
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        sub_material = request.query_params.get("sub_material", "")
        if "sub_material":
            try:
                Material.objects.get(id=sub_material).delete()
            except Material.DoesNotExist:
                return Response({"detail":"No Material matches the given query"}, status=status.HTTP_404_NOT_FOUND)
        else:
            instance.delete()
        return Response({"detail":"record deleted"}, status=status.HTTP_204_NO_CONTENT)

class ToleranceViewSet(viewsets.GenericViewSet,
                        mixins.ListModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin):
    permission_classes = [IsAuthenticated]
    permission_classes = [IsAdminOrMember]

    queryset = Tolerance.objects.all()
    serializer_class = ToleranceSerializer

class MaterialRetrieveUpdateDestroyAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrMember]

    @swagger_auto_schema(   
        responses={200: 'Success', 404: 'Not Found'}
    )
    def get(self, request, pk):
        """
        Get details of a specific material.
        """
        material = get_object_or_404(Material, id=pk)
        serializer = MaterialSerializer(material)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='Material name'),
                'price': openapi.Schema(type=openapi.TYPE_NUMBER, description='Material price'),
                'is_material_category': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Is material category'),
                'parent_material': openapi.Schema(type=openapi.TYPE_STRING, description='Parent material'),
                'active': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Is material active'),
                'density': openapi.Schema(type=openapi.TYPE_NUMBER, description='Material density'),
                'mega_joules_per_kg': openapi.Schema(type=openapi.TYPE_NUMBER, description='Mega joules per kg'),
                'kilo_gram_carbon_dioxide_equivalent_per_kg': openapi.Schema(type=openapi.TYPE_NUMBER, description='KG carbon dioxide equivalent per kg'),
            }
        ),
        responses={200: 'Success', 400: 'Bad Request'}
    )
    def put(self, request, pk):
        """
        Update details of a specific material.
        """
        material = get_object_or_404(Material, id=pk)

        serializer = MaterialSerializer(material, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'pk',
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description='ID of the material to retrieve/update/delete'
            )
        ],
        responses={204: 'No Content', 404: 'Not Found'}
    )
    def delete(self, request, pk):
        """
        Delete a specific material.
        """
        material = get_object_or_404(Material, id=pk)
        material.delete()
        return Response({"message": "Material deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


class CountryCo2IntesityListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrMember]

    def get(self, request):
        countries = CountryCO2Intensity.objects.all()
        serializer = CountryCO2IntensitySerializer(countries, many=True)
        return Response(serializer.data)
    
    @swagger_auto_schema(request_body=CountryCO2IntensitySerializer)
    def post(self, request):
        
        serializer = CountryCO2IntensitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "CO2Intensity for country Created successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CountryCO2IntensityRetrieveUpdateDestroyAPIView(APIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    permission_classes = [IsAdminOrMember]

    def create(self, validated_data):
            return CountryCO2Intensity.objects.create(**validated_data)
    def update(self, instance, validated_data):
        instance.country_name = validated_data.get('country_name', instance.country_name)
        instance.value = validated_data.get('value', instance.value)
        instance.save()
        return instance

    def get_object(self, pk):
        try:
            return CountryCO2Intensity.objects.get(pk=pk)
        except CountryCO2Intensity.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(request_body=CountryCO2IntensitySerializer)
    def put(self, request, pk):
        country = self.get_object(pk)
        serializer = CountryCO2IntensitySerializer(country, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "CO2Intensity for country Updated successfully."})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        country = self.get_object(pk)
        country.delete()
        return Response({"message": "CO2Intensity for country Deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

class MaterialListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrMember]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='Material name'),
                'price': openapi.Schema(type=openapi.TYPE_NUMBER, description='Material price'),
                'is_material_category': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Is material category'),
                'parent_material': openapi.Schema(type=openapi.TYPE_STRING, description='Parent material'),
                'active': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Is material active'),
                'density': openapi.Schema(type=openapi.TYPE_NUMBER, description='Material density'),
                'mega_joules_per_kg': openapi.Schema(type=openapi.TYPE_NUMBER, description='Mega joules per kg'),
                'kilo_gram_carbon_dioxide_equivalent_per_kg': openapi.Schema(type=openapi.TYPE_NUMBER, description='KG carbon dioxide equivalent per kg'),
                
                'mm3_coeff_uk_removed': openapi.Schema(type=openapi.TYPE_NUMBER, description='mm3 coeff uk removed'),
                'mm3_coeff_eu_removed': openapi.Schema(type=openapi.TYPE_NUMBER, description='mm3 coeff eu removed'),
                'mm3_coeff_cn_removed': openapi.Schema(type=openapi.TYPE_NUMBER, description='mm3 coeff cn removed'),
                'mm2_coeff_uk_finished': openapi.Schema(type=openapi.TYPE_NUMBER, description='mm2 coeff uk finished'),
                'mm2_coeff_eu_finished': openapi.Schema(type=openapi.TYPE_NUMBER, description='mm2 coeff eu finished'),
                'mm2_coeff_cn_finished': openapi.Schema(type=openapi.TYPE_NUMBER, description='mm2 coeff cn finished'),


            },
            required=['name']  # Make 'name' required
        ),
        responses={201: 'Created', 400: 'Bad Request'}
    )
    def post(self, request):
        """
        Create a new material.
        """
        serializer = MaterialSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        return Material.objects.all()

    def get(self, request):
        materials = self.get_queryset()
        serializer = MaterialSerializer(materials, many=True)
        return Response(serializer.data)



class ManageMaterials(viewsets.GenericViewSet,
                        mixins.ListModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin):
    serializer_class = MaterialSerializer
    queryset = Material.objects.all()
    permission_classes = [IsAdminOrMember]

class ManageHeatTreatments(viewsets.GenericViewSet,
                           mixins.ListModelMixin,
                           mixins.CreateModelMixin,  # Add CreateModelMixin
                           mixins.UpdateModelMixin,
                           mixins.DestroyModelMixin):
    queryset = HeatTreatment.objects.all()
    serializer_class = HeatTreatmentsSerializer
    permission_classes = [IsAdminOrMember]

    @swagger_auto_schema(responses={200: HeatTreatmentsSerializer(many=True)})
    def list(self, request, *args, **kwargs):
        all_heat_treatments_names = [] 
        for heat_treatment in HeatTreatment.objects.all():
            if heat_treatment.name not in all_heat_treatments_names:
                all_heat_treatments_names.append(heat_treatment.name)  
        
        output = []
        for name in all_heat_treatments_names:
            data = {}
            for country in Country.objects.all():
                instance = HeatTreatment.objects.filter(name=name, country=country).first()
                if instance:
                    serializer = HeatTreatmentsSerializer(instance)
                    data.update({name: serializer.data})
            output.append(data)
        
        return Response(output, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=HeatTreatmentsSerializer, responses={201: HeatTreatmentsSerializer})
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save()

class ManageInspection(viewsets.GenericViewSet,
                        mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin):
    queryset = Inspections.objects.all()
    serializer_class = InspectionSerializer 
    permission_classes = [IsAdminOrMember]


    def list(self, request, *args, **kwargs):
        all_inspection_names = [] 
        for inspection in Inspections.objects.all():
            if inspection.name not in  all_inspection_names:
                 all_inspection_names.append(inspection.name)  
        
        output = []
        for name in  all_inspection_names:
            data = {
                }
            for country in Country.objects.all():
                instance = Inspections.objects.filter(name=name, country=country).first()

                if instance:
                    serializer = InspectionSerializer(instance)
                    data.update({name : serializer.data })

            output.append(data)
        
        return Response(output, status=status.HTTP_200_OK)
    @swagger_auto_schema(request_body=InspectionSerializer, responses={201: InspectionSerializer})
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save()

class ManageFinish(viewsets.GenericViewSet,
                        mixins.ListModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin):
    queryset = Coatings.objects.all()
    serializer_class = FinishSerializer
    permission_classes = [IsAuthenticated]
    permission_classes = [IsAdminOrMember]
    
    @swagger_auto_schema(responses={200: FinishSerializer(many=True)})
    def list(self, request, *args, **kwargs):
        all_finish_names = [] 
        for coating in Coatings.objects.all():
            if coating.name not in all_finish_names:
                all_finish_names.append(coating.name)  
        
        output = []
        for name in all_finish_names:
            data = {
                }
            for country in Country.objects.all():
                instance = Coatings.objects.filter(name=name, country=country).first()

                if instance:
                    serializer = FinishSerializer(instance)
                    data.update({name : serializer.data })

            output.append(data)
        
        return Response(output, status=status.HTTP_200_OK)

class ManageReport(viewsets.GenericViewSet,
                        mixins.ListModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.DestroyModelMixin):
   
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer  
    permission_classes = [IsAdminOrMember]

    
    def list(self, request, *args, **kwargs):
        # Calculate total sales
        total_sales = Transaction.objects.filter(amount_status="Received").aggregate(total=Sum('amount'))['total'] or 0.0

        # Aggregate data from quotes excluding those with refund status
        quote_aggregate = Quote.objects.exclude(transaction__amount_status="Refund").aggregate(
            total_revenue=Sum('order_total'),
            total_delivery_charges=Sum('delivery_charges'),
            total_tax=Sum('tax')
        )

        total_delivery_charges = quote_aggregate.get('total_delivery_charges', 0.0) or 0.0
        total_tax = quote_aggregate.get('total_tax', 0.0) or 0.0
        price_exclude = total_delivery_charges + total_tax

        # Calculate total cost of products
        products = Product.objects.all()
        total_cost = sum(
            (product.cost_coating or 0) + 
            (product.cost_inspection or 0) + 
            (product.cost_heat_treatment or 0) + 
            (product.cost_machining or 0) + 
            (product.cost_material or 0)
            for product in products
        )
        total_quantity = sum(product.quantity for product in products)

        # Compute total revenue
        total_revenue = 0
        orders = Order.objects.all()
        for order in orders:
            total_revenue += total_quantity * order.order_total + total_cost

        total_revenue = total_revenue - price_exclude

        quote_count = Quote.objects.count()

        visit_count = 0
        top_countries = Product.objects.values('country__name','cost_machining').annotate(
            total_machining_cost=Sum('cost_machining')
        ).order_by('-total_machining_cost')
        top_countries = top_countries[:3]
         # Get the top 5 products by quantity, including country and manufacture_lead
        top_products = Product.objects.values('id', 'quantity', 'country__name','material__name','cost_machining').annotate(
            total_quantity=F('quantity')
        ).order_by('-total_quantity')[:5]
        top_products_dict = {
            product['id']: {
                'quantity': product['total_quantity'],
                'country': product['country__name'],
                'product_name': product['material__name'],
                "cost_machining":product['cost_machining']
            } for product in top_products
        }

        response_data = {
            'total_revenue': total_revenue,
            'total_sales': total_sales,
            'quote_count': quote_count,
            'visit_count': visit_count,
            'best_selling_products': top_products_dict,
            'countries':top_countries
        }

        return Response(response_data)


class ManageCarbonOffset(viewsets.GenericViewSet,
                        mixins.ListModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin):
    queryset = CarbonOffset.objects.all()
    serializer_class = ManageCarbonOffSetSerializer
   
class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [IsAdminOrMember]

    @swagger_auto_schema(
        operation_summary="List all countries",
        responses={200: CountrySerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create a new country",
        request_body=CountrySerializer,
        responses={201: CountrySerializer}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve a country",
        responses={200: CountrySerializer}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update a country",
        request_body=CountrySerializer,
        responses={200: CountrySerializer}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partial update a country",
        request_body=CountrySerializer,
        responses={200: CountrySerializer}
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete a country",
        responses={204: 'No Content'}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

class AdvancedSearchQuery(viewsets.ViewSet):


    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
    permission_classes = [IsAdminOrMember]
    permission_classes = [IsAuthenticated] 
    def list(self, request):
        try:
            # Check if the query is in the request parameters
            query_param = request.query_params.get('query', '')
            # Check if the query is in the request body
            query_body = request.data.get('query', '')

            # Combine the queries, giving precedence to the query parameter
            query = query_param if query_param else query_body

            material_results = self.search_material(query)
            sub_material_results = self.search_sub_material(query)
            customer = self.search_customer(query)
        
            # Serialize the data
            material_serializer = MaterialSerializer(material_results, many=True)
            sub_material_serializer = ParentMaterialSerializer(sub_material_results, many=True)
            shipping_serializer = ShippingAddressSerializer(customer, many=True)

            return Response({
                'material': material_serializer.data,
                'sub_material': sub_material_serializer.data,
                'customer':shipping_serializer.data,
            })
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def search_material(self, query):
        return Material.objects.filter(
            Q(name__icontains=query) |
            Q(parent_material__name__icontains=query) 
        )
    
    def search_sub_material(self, query):
        return ParentMaterial.objects.filter(
            Q(name__icontains=query) 
        )
    
  
    def search_customer(self,query):
        return ShippingAddress.objects.filter(
            Q(name__icontains=query) |
            Q(country__icontains = query) |
            Q(address__icontains =query) |
            Q(phone_number__icontains = query) |
            Q(user__email__icontains = query) |
            Q(zip_postal_pinconde__icontains =query) |
            Q(company__icontains =query) |
            Q(state_region_province__icontains=query)
        )
