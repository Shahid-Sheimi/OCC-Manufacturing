from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser

from rest_framework import mixins, generics
from rest_framework_simplejwt.authentication import JWTAuthentication 
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import viewsets, status
from rest_framework.response import Response
from .main import process_stp_file
import os
from django.conf import settings
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from datetime import timedelta, datetime
from .permissions import IsOwnerOrAdmin, IsAdmin

from .models import Order, Product,Material,CountryCO2Intensity, HeatTreatment, ParentMaterial,\
      Tolerance,Manufacturer, Coatings, Inspections, Country, ManufacturerLead, Quote, ShippingAddress

from .serializers import OrderSerializer,ManufacturerSerializer, ProductSerializer,MaterialSerializer,\
    CountryCO2IntensitySerializer, HeatTreatmentSerializer, ToleranceSerializer, CoatingsSerializer, \
        InspectionsSerializer, ShippingAddressSerializer, ManufacturerLeadSerializer, ParentMaterialSerializer, QuoteSerializer



class UploadSTPFileView(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'stp_file', openapi.IN_FORM, description="The STP file to upload. Must be a valid STP file.", 
                type=openapi.TYPE_FILE, required=True
            ),
        ],
        responses={
            201: 'Created',
            400: 'Bad Request',
            415: 'Unsupported Media Type: Only STP files are allowed.'
        }
    )
    def post(self, request, *args, **kwargs):
        try:
            product_data_list = []
            material_id = request.data.get('material', None)
            heat_treatment_id = request.data.get('heat_treatment', None)
            tolerance_id = request.data.get('tolerance', None)
            coatings_id = request.data.get('coatings', None)
            inspections_id = request.data.get('inspections', None)
            quantity = request.data.get('quantity', None)
            country = request.data.get('country', None)

            for stp_file in request.FILES.getlist('stp_file'):
                if stp_file:
                    if not os.path.exists(settings.MEDIA_ROOT):
                        os.makedirs(settings.MEDIA_ROOT)
                    file_path = os.path.join(settings.MEDIA_ROOT, stp_file.name)
                    with open(file_path, 'wb+') as destination:
                        for chunk in stp_file.chunks():
                            destination.write(chunk)

                        # Process the STP file
                        _, _, length, width, height, surface_area_cal, finished_volume_mm3, finished_area_mm2, _, _, _, _, _ = process_stp_file(file_path)
                        
                        # Optionally, you can save measurements and tolerances to the product instance
                        
                        product_data = {
                            'name': stp_file.name,  # Set the product name to the file name
                            'file': stp_file,
                            'length': length,
                            'width': width,
                            'height': height,
                            'volume_mm3': finished_volume_mm3,
                            'area_mm2': finished_area_mm2,
                            'final_length': length,
                            'final_width': width,
                            'final_height': height,
                            'final_volume_mm3': finished_volume_mm3,
                            'final_area_mm2': finished_area_mm2,
                            'surface_area': surface_area_cal
                        }
                        
                        if material_id:
                            product_data.update({'material' : material_id })
                        if heat_treatment_id:
                            product_data.update({'heat_treatment' : heat_treatment_id })
                        if tolerance_id:
                            product_data.update({'tolerance' : tolerance_id })
                        if coatings_id:
                            product_data.update({'coatings' : coatings_id })
                        if inspections_id:
                            product_data.update({'inspections' : inspections_id })
                        if country:
                            product_data.update({'country' : country})

                        product_data_list.append(product_data)
                if not product_data_list:
                    return Response({'error': 'No files found in request'}, status=status.HTTP_400_BAD_REQUEST)
                products = []
                for product_data in product_data_list:
                    product_serializer = ProductSerializer(data=product_data)
                    if product_serializer.is_valid():
                        product_serializer.save()
                        products.append(product_serializer.data)
                    else:
                        return Response(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response(products, status=status.HTTP_201_CREATED)
        except Exception as e:
            print("An error occurred:", e)  # Debugging output
            return Response({'error': 'An error occurred'}, status=status.HTTP_400_BAD_REQUEST)
        

    @swagger_auto_schema(responses={200: 'Success'})
    def get(self, request):
        products = Product.objects.all()
        data = []
        for product in products:
            product_data = {
                'id': product.id,
                'name': product.name,
                'length': product.length,
                'width': product.width,
                'height': product.height,
                'volume_mm3': product.volume_mm3,
                'area_mm2': product.area_mm2,
                'finished_weight': product.finished_weight,
                'final_length': product.final_length,
                'final_width': product.final_width,
                'final_height': product.final_height,
                'final_volume_mm3': product.final_volume_mm3,
                'final_area_mm2': product.final_area_mm2,
                'surface_area' :product.surface_area,
                'final_weight': product.finished_weight,
            }
            data.append(product_data)
        return Response(data)



class ProductConfigViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def list(self, request):

        parent_material = ParentMaterial.objects.all()
        serialized_parent_materials = ParentMaterialSerializer(parent_material, many=True)

        materials = Material.objects.all()
        serialized_materials = MaterialSerializer(materials, many=True)

        heat_treatments = HeatTreatment.objects.all()
        serialized_heat_treatments = HeatTreatmentSerializer(heat_treatments, many=True)

        tolerances = Tolerance.objects.all()
        serialized_tolerances = ToleranceSerializer(tolerances, many=True)

        coatings = Coatings.objects.all()
        serialized_coatings = CoatingsSerializer(coatings, many=True)

        inspections = Inspections.objects.all()
        serialized_inspections = InspectionsSerializer(inspections, many=True)

        all_materials =[]
        for parent in serialized_parent_materials.data:
            parent_dic = {
                'parent_material' : parent
            }

            all_childs = []
            for child_material in serialized_materials.data:
                if parent.get('id') == child_material.get('parent_material'):
                    child = {
                        'id' : child_material.get('id'),
                        'name' : child_material.get('name')
                        }
                    all_childs.append(child)
            parent_dic.update({'material':all_childs})

            all_materials.append(parent_dic)

        heat_treatment_list = []
        for heat_treatment in serialized_heat_treatments.data:
            ht = {
                'id' : heat_treatment.get('id'),
                'name' : heat_treatment.get('name')
            }
            heat_treatment_list.append(ht)

        data = {
            'materials' : all_materials,
            'heat_treatments': heat_treatment_list,
            'tolerances': serialized_tolerances.data,
            'coatings': serialized_coatings.data,
            'inspections': serialized_inspections.data
        }
        return Response(data)

    def create(self, request):
        product_ids = list(request.data.get('product_ids'))
        material_id = request.data.get('material')
        heat_treatment_id = request.data.get('heat_treatment')
        tolerance_id = request.data.get('tolerance')
        coatings_id = request.data.get('coatings')
        inspections_id = request.data.get('inspections')
        quantity = request.data.get('quantity')
        
        
        material_instance = None
        heat_treatment_instance = None
        tolerance_instance = None
        coatings_instance = None
        inspections_instance = None

        # Retrieve instances for each model if ID is provided
        if material_id:
            try:
                material_instance = Material.objects.get(id=material_id)
            except Material.DoesNotExist:
                return Response({'material': 'Material with provided ID does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        if heat_treatment_id:
            try:
                heat_treatment_instance = HeatTreatment.objects.get(id=heat_treatment_id)
            except HeatTreatment.DoesNotExist:
                return Response({'heat_treatment': 'Heat Treatment with provided ID does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        if tolerance_id:
            try:
                tolerance_instance = Tolerance.objects.get(id=tolerance_id)
            except Tolerance.DoesNotExist:
                return Response({'tolerance': 'Tolerance with provided ID does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        if coatings_id:
            try:
                coatings_instance = Coatings.objects.get(id=coatings_id)
            except Coatings.DoesNotExist:
                return Response({'coatings': 'Coatings with provided ID does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        if inspections_id:
            try:
                inspections_instance = Inspections.objects.get(id=inspections_id)
            except Inspections.DoesNotExist:
                return Response({'inspections': 'Inspections with provided ID does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        
        products = []

        for p_id in product_ids:
            product = Product.objects.filter(pk=p_id).first()
            if product:
                product.material = material_instance 
                product.heat_treatment = heat_treatment_instance 
                product.inspection = inspections_instance  
                product.coating = coatings_instance  
                product.quantity = quantity
                product.save()
                
                products.append(product)

        products = ProductSerializer(products, many=True)
        return Response(products.data, status=status.HTTP_201_CREATED)            


class SelectManufacturerViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer

    def list(self, request):

        all_leads = Manufacturer.objects.all()
        serialized_leads = ManufacturerSerializer(all_leads, many=True)
    
        return Response(serialized_leads.data)


    def create(self, request, *args, **kwargs):

        product_ids = list(request.data.get('product_ids'))
        country_id = request.data.get("country")
        lead_time = request.data.get("lead_time")
        order_id = request.data.get("order_id")


        
        country_instance = Country.objects.filter(id=country_id).first()
        manufacturer_lead_instance = ManufacturerLead.objects.filter(id=lead_time).first()

        carbon_footprint_CO2 = 0
        products = []

        for p_id in product_ids:
            product = Product.objects.filter(pk=p_id).first()
            if product:
                products.append(product.id)
                
                product.country = country_instance 
                product.manufacturer_lead = manufacturer_lead_instance
                product.save()
                carbon_footprint_CO2 += product.carbon_footprint_CO2 

        if products and not order_id:
            try:
                order = Order.objects.create()
                current_timestamp = datetime.now().timestamp()
                order.order_id = current_timestamp
                order.country = country_instance
                order.products.set(p_id for p_id in products)
                order.manufacturer_lead = manufacturer_lead_instance
                order.user = self.request.user
                order.carbon_footprint = carbon_footprint_CO2
                order.save()
                serialized_order = OrderSerializer(order)
            except Exception as e:
                return Response(f"Failed to create order..{e}",status=status.HTTP_201_CREATED)
        
        if order_id:
            try:
                order = Order.objects.filter(pk=order_id).first()
                order.country = country_instance
                order.products.set(p_id for p_id in products)
                order.manufacturer_lead = manufacturer_lead_instance
                order.carbon_footprint = carbon_footprint_CO2
                order.save()
                serialized_order = OrderSerializer(order)
            except Exception as e:
                return Response(f"Failed to update order..{e}",status=status.HTTP_201_CREATED)
        
        data = {
            'order' : serialized_order.data,
            "kgCO2e" : carbon_footprint_CO2
        }

        return Response(data,status=status.HTTP_201_CREATED)
    

class ProductRetrieveUpdateDestroyAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    authentication_classes = [JWTAuthentication]

    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        try:
            product = self.get_object(pk)
            product_data = {

                'length': product.length,
                'width': product.width,
                'height': product.height,
                'volume_mm3': product.volume_mm3,
                'area_mm2': product.area_mm2,
                'finished_weight': product.finished_weight,

            }
            return Response(product_data)
        except product.DoesNotExist as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            product = self.get_object(pk)
        except Product.DoesNotExist:
            return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        data = request.data
        length_change_percent = data.get('extend_length', 0)
        width_change_percent = data.get('extend_width', 0)
        height_change_percent = data.get('extend_height', 0)
        over_length_in_mm = data.get('over_length_in_mm', 0)
       
        if length_change_percent or width_change_percent or height_change_percent:
            if length_change_percent:
                product.length_extend_percentage = length_change_percent
                product.final_length = product.length * (1 + length_change_percent / 100)
            if width_change_percent:
                product.width_extend_percentage = width_change_percent
                product.final_width = product.width * (1 + width_change_percent / 100)
            if height_change_percent:
                product.height_extend_percentage = height_change_percent
                product.final_height = product.height * (1 + height_change_percent / 100)
            
            product.final_volume_mm3 = product.over_length_mm * product.over_width_mm * product.over_height_mm
            product.final_area_mm2 = product.over_length_mm * product.over_width_mm

            if product.material:
                product.finished_weight = product.final_volume_mm3 * product.material.density * 1E-9    
        
        
        if  product.billet_volume:
            try:
                product.billet_weight = product.billet_volume * product.material.density * 1E-9
            except Exception as e:
                    return Response(status=status.HTTP_404_NOT_FOUND)
        product.over_length_in_mm = over_length_in_mm
        product.save()
        product_data = {
            'final_length': product.length,
            'final_width': product.width,
            'final_height': product.height,
            'final_volume_mm3': product.final_volume_mm3,
            'final_area_mm2': product.final_area_mm2,
            'final_finished_weight': product.finished_weight,
            'billet_volume':product.billet_volume,
            'billet_weight':product.billet_weight,
            'over_length_in_mm' : over_length_in_mm
        }
        return Response(product_data)       

    def delete(self, request, pk):
        try:
            product = self.get_object(pk)
            product.delete()
            return Response({"message": "Product deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except product.DoesNotExist as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)



class OrderSummaryViewset(viewsets.ModelViewSet):
    # permission_classes = [IsOwnerOrAdmin]
    authentication_classes = [JWTAuthentication]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def calculate_delivery_charges(self, order):
        # Implement your logic to calculate delivery charges here
        # For example:
        if not order.country:
            # 
            return 0
        else:
            # Flat rate delivery charge for international orders
            return 20
    
    def calculate_tax(self, order):
        
        return order.order_total * 0.15
    
    def calculate_order_total(self, order):
       
        total = 0
        for product in order.products.all():
            if product.added_in_basket:
                total +=  product.quantity 
            order.order_total = total
            order.save()
        return total
    
    def show_order(self,order_id):
        order = Order.objects.filter(id=order_id).first()
        summary = []
        
        if order:
            today = order.created_at
            order_total = self.calculate_order_total(order)
            products = order.products.all()
            all_products = []
            
            for product in products:
                material = MaterialSerializer(product.material)
                heat_treatment = HeatTreatmentSerializer(product.heat_treatment)
                coating = CoatingsSerializer(product.coating)
                inspection = InspectionsSerializer(product.inspection)
                manufacturer_lead = ManufacturerLeadSerializer(order.manufacturer_lead)
                lead_duration = manufacturer_lead.data.get('duration')
                lead_max = manufacturer_lead.data.get('max_time')
                if lead_duration == 'Weeks':
                    lead_time = today + timedelta(weeks=lead_max)
                else:
                    lead_time = today + timedelta(days=lead_max)
                formatted_lead_time = lead_time.strftime("%B %d, %Y")

                product = {
                    'id' : product.id,
                    'name' : product.name,
                    'quantity' : product.quantity,
                    'carbon_footprint_CO2' : product.carbon_footprint_CO2,
                    'material' :material.data.get('name'),
                    'heat_treatment' : heat_treatment.data.get('name'),
                    'tolerancing' : 10,
                    'coatings' : coating.data.get('name'),
                    'inspection' : inspection.data.get('name'),
                    'lead_time' : formatted_lead_time,
                    'added_in_basket' : product.added_in_basket,
                    'Manufacturing Location': product.country.name,

                }
                all_products.append(product)
            
            order_summary = {
                "Order_id" : order.id,
                'Products' : all_products,
                "Basket" : {
                    "Total Part Added": sum(True if product.added_in_basket else False for product in order.products.all()),  
                    "Total Carbon Footprints": sum(product.carbon_footprint_CO2 for product in products),
                    "Delivery": 50,
                    "Tax": 10,
                    "Order Total": order_total + 50 + 10  if order_total else None,
                },
            }
            summary.append(order_summary)
        
        return summary

    
    def list(self, request, *args, **kwargs):
        order_id = request.GET.get('order_id')
        return Response(self.show_order(order_id), status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
         
        order_id = request.data.get('order_id')
        product_ids = request.data.get('product_id')
        added_in_basket = bool(request.data.get('added_in_basket'))
        quantity = request.data.get('quantity')

        product = Product.objects.filter(id=product_ids).first()
        if product:
            if added_in_basket != product.added_in_basket:
                product.added_in_basket = added_in_basket
            if quantity:
                product.quantity = quantity
            
            product.save()

        return Response(self.show_order(order_id), status=status.HTTP_201_CREATED)
        

    def delete(self, request, *args, **kwargs):
        product_ids = request.data.get('product_ids')
        order_id = request.data.get('order_id')

        product = get_object_or_404(Product, pk=product_ids)
        product.delete()

        return Response(self.show_order(order_id), status=status.HTTP_200_OK)


class QuoteViewSet(viewsets.ModelViewSet):
    queryset = Quote.objects.all()
    serializer_class = QuoteSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_authenticated:
            user = self.request.user
            return queryset.filter(user=user)
    

    def create(self, request, *args, **kwargs):

        manufacturing_terms = request.data.get('manufacturing_terms')
        carbon_offsetting_terms = request.data.get("carbon_offsetting_terms")
        promise_date = request.data.get("promise_date")
        order_id = request.data.get("order_id")
        payment_method = request.data.get("payment_method", None)


        order_instance = Order.objects.filter(id=order_id).first()
        if order_instance:
            if payment_method:
                order_instance.payment_method = payment_method
                order_instance.save()
            products = order_instance.products.all().filter(added_in_basket=True)

            quote = Quote()
            current_timestamp = datetime.now().timestamp()

            if isinstance( manufacturing_terms, bool)  and isinstance(carbon_offsetting_terms, bool):
            
                shipping_address = ShippingAddress.objects.filter(user=self.request.user).first()

                if shipping_address:
                    quote.shipping = shipping_address

                quote.quote_id = current_timestamp
                quote.manufacturing_terms_and_conditions = manufacturing_terms
                quote.carbon_offsetting_terms_and_conditions = carbon_offsetting_terms
                quote.lead_time = promise_date
                quote.user = self.request.user
                quote.save()
                quote.products.set(p_id.id for p_id in products)
                quote.save()

            shipping_addresses = ShippingAddress.objects.filter(user = self.request.user)
            serialized_shipping_addresses = ShippingAddressSerializer(shipping_addresses)
            serialized_quote = QuoteSerializer(quote)
            data = {
                'quote' : serialized_quote.data,
                'shipping' : serialized_shipping_addresses.data
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(f"Order with id {order_id} not found", status=status.HTTP_201_CREATED)


    def update(self, request, *args, **kwargs ):
        # quote_id = request.data.get('quote_id')
        quote_id = kwargs.get('pk')
        shipping_id = int(request.data.get('shipping_address_id'))

        quote = Quote.objects.filter(quote_id = quote_id).first()
        
        selected_shipping_address = ShippingAddress.objects.filter(id=shipping_id).first()
      
        if quote and selected_shipping_address:
            quote.shipping = selected_shipping_address
            quote.save()

            shipping_addresses = ShippingAddress.objects.filter(user = self.request.user)
            serialized_shipping_addresses = ShippingAddressSerializer(shipping_addresses, many=True)
            
            serialized_quote = QuoteSerializer(quote)
            data = {
                'quote' : serialized_quote.data,
                'shipping' : serialized_shipping_addresses.data,
            }
            return Response(data, status=status.HTTP_201_CREATED)            
        
        return Response("data", status=status.HTTP_201_CREATED)
