from rest_framework import serializers
from authentication.models import User
from process_occ.models import Quote, Order, Manufacturer, Material, ParentMaterial,HeatTreatment,Inspections,Coatings, Country
from django.db import models
from payments.models import Transaction
from .models import Shipping, CarbonOffset
from process_occ.serializers import CountrySerializer,ManufacturerLeadSerializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username', 'email', 'role']


class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['role']

class ManageCustomerSerializer(serializers.ModelSerializer):
    total_parts = serializers.SerializerMethodField()

    def get_total_parts(self, obj):
        return Quote.objects.filter(user=obj).aggregate(total_parts=models.Sum('total_parts'))['total_parts'] or 0

    class Meta:
        model = User
        fields = ['username', 'email','last_login', 'total_parts']



class ManageQuoteSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Quote
        fields = ['quote_id', 'created_at','total_parts', 'total_quantity', 'order_total', 'approved'] 


class ManageQuoteUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quote
        fields = ['approved'] 


class ManageOrderSerilizer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()

    def get_user_name(self, obj):
        return obj.user.username if obj.user else None
    class Meta:
        model = Order
        fields = ['id','order_id','user_name','order_date','promise_date','buyer_initials','supplier_due_date','current_status']



class OrderDetailSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()

    def get_user_name(self, obj):
        return obj.user.username if obj.user else None
    
    class Meta:
        model= Order
        fields = ['order_id','order_date','promise_date','buyer_initials','supplier_due_date','current_status','user_name','payment_method','order_total']

        

class ManageTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"



class ManageShippingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipping
        exclude = ['transaction']






class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ["txn_id", "transaction_date" ,"amount_status"]

class ShippingSerializer(serializers.ModelSerializer):
    transaction = TransactionSerializer(read_only=True)
    class Meta:
        model = Shipping
        fields = '__all__'

class ManageManufaturerSerializer(serializers.ModelSerializer):
    country = CountrySerializer(read_only=True)
    lead_time = ManufacturerLeadSerializer(many=True,read_only=True)

    class Meta:
        model = Manufacturer
        fields = "__all__"


class MaterialSerializer(serializers.ModelSerializer):

    class Meta:
        model = Material
        fields = ['id','price_per_1000000_mm3', 'material_removed_price_per_100_mm3']


class ParentMaterialSerializer(serializers.ModelSerializer):
    sub_material = MaterialSerializer(many=True, read_only=True, source='material_set')
    class Meta:
        model = ParentMaterial
        fields = "__all__"




class HeatTreatmentsSerializer(serializers.ModelSerializer):
    country = CountrySerializer()
    class Meta:
        model = HeatTreatment
        fields = ['mega_joules_per_kg', 'country']
    #added extra
    def create(self, validated_data):
        country_data = validated_data.pop('country')
        country, created = Country.objects.get_or_create(**country_data)
        heat_treatment = HeatTreatment.objects.create(country=country, **validated_data)
        return heat_treatment




class InspectionSerializer(serializers.ModelSerializer):
    country = CountrySerializer(read_only = True)
    class Meta:
        model= Inspections
        fields = ['kilowatt_hours_per_mm_sqaure', 'country',]



class FinishSerializer(serializers.ModelSerializer):
    country = CountrySerializer(read_only = True)
    class Meta:
        model = Coatings
        fields = ['id','mega_joules_per_mm_sqaure','country', 'cost_per_mm2']


class ManageCarbonOffSetSerializer(serializers.ModelSerializer):
    order = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all())

    class Meta:
        model = CarbonOffset
        fields = "__all__"

