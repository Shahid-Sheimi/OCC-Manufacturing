# serializers.py
from rest_framework import serializers
from .models import Order, Product,Material,CountryCO2Intensity,HeatTreatment,Coatings,Manufacturer,\
    Tolerance, Inspections, ManufacturerLead,ShippingAddress, ParentMaterial, Country,Quote

class ProductSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)

    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ['id']

    def __init__(self, *args, **kwargs):
        super(ProductSerializer, self).__init__(*args, **kwargs)
        self.fields['file'].required = False  


class HeatTreatmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeatTreatment
        fields = '__all__'



class CoatingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coatings
        fields = '__all__'


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = '__all__'


class ParentMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParentMaterial
        fields = "__all__"

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    country = CountrySerializer()
    class Meta:
        ref_name = 'quote_serializer'
        model = Order
        fields = '__all__'

class CountryCO2IntensitySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CountryCO2Intensity
        fields = ['id', 'country', 'value']


class ToleranceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tolerance
        fields = '__all__'

class InspectionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inspections
        fields = '__all__'

class ManufacturerLeadSerializer(serializers.ModelSerializer):
    class Meta:
        model=ManufacturerLead
        fields = '__all__'


class ManufacturerSerializerCreate(serializers.ModelSerializer):
        country = serializers.PrimaryKeyRelatedField(queryset=Country.objects.all())
        lead_time = serializers.PrimaryKeyRelatedField(queryset=ManufacturerLead.objects.all(), many=True)
        
        class Meta:
            model = Manufacturer
            fields = ['country', 'lead_time']
        
        def create(self, validated_data):
            lead_time_data = validated_data.pop('lead_time')
            manufacturer = Manufacturer.objects.create(**validated_data)
            manufacturer.lead_time.set(lead_time_data)
            return manufacturer

        def update(self, instance, validated_data):
            lead_time_data = validated_data.pop('lead_time')
            instance = super().update(instance, validated_data)
            instance.lead_time.set(lead_time_data)
            return instance

class ManufacturerSerializer(serializers.ModelSerializer):
    lead_time = ManufacturerLeadSerializer(many=True, read_only=True)
    country = CountrySerializer(read_only=True)
    class Meta:
    
        model = Manufacturer
        fields = ["country","lead_time"]


class QuoteSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)
    class Meta:
        ref_name = 'quote'
        model = Quote
        fields = '__all__'

class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model=ShippingAddress
        fields = '__all__'
