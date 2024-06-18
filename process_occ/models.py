from django.db import models
from django.contrib.auth import get_user_model
from datetime import timedelta
from datetime import timedelta
from django.utils import timezone
from payments.models import Transaction
# from admin_panel.serializers import ManageTransactionSerializer
User = get_user_model()


class Country(models.Model):
    name = models.CharField(max_length=40, unique=True, null=True, blank=True)

    def __str__(self):
        return self.name


class MaterialMM2FinishedPrice(models.Model):
    mm2_coeff_finished_price = models.FloatField(default=0)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return f"mm2 coeff finished price for {self.country.name} is {self.mm2_coeff_finished_price}" 


class MaterialMM3RemovedPrice(models.Model):
    mm3_coeff_removed_price = models.FloatField(default=0)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"mm3 coeff removed price for {self.country.name} is {self.mm3_coeff_removed_price}" 
    

class ParentMaterial(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name
    

class Material(models.Model):
    parent_material = models.ForeignKey(ParentMaterial, on_delete=models.CASCADE, null=True, blank=True)

    name = models.CharField(max_length=20)
    price = models.FloatField(null=True, blank=True, default=0)
    active = models.BooleanField(default=True, null=False)
    density = models.FloatField(default=0)
    mega_joules_per_kg = models.FloatField(default=0)
    cost_per_kg = models.FloatField(default=0)

    kilo_gram_carbon_dioxide_equivalent_per_kg = models.FloatField(default=0)
    
    machining_mm3_coeff_removed_price = models.ManyToManyField(MaterialMM3RemovedPrice)
    machining_mm2_coeff_finished_price = models.ManyToManyField(MaterialMM2FinishedPrice)

    price_per_1000000_mm3= models.FloatField(blank= True, null= True, default=0)
    material_removed_price_per_100_mm3= models.FloatField(default=0) 

    def __str__(self):
        return self.name

    
class ManufacturerLead(models.Model):
    LEAD_CHOICES = [
        ('express', 'Express'),
        ('fast', 'Fast'),
        ('normal', 'Normal')
        ]
    name = models.CharField(max_length=25, choices=LEAD_CHOICES,default="normal")

    CHOICES = [
        ('Days', 'Days'),
        ('Weeks', 'Weeks')
        ]
    duration = models.CharField(max_length=25, choices=CHOICES,default="Weeks")

    min_time = models.PositiveIntegerField()
    max_time = models.PositiveIntegerField()

    price = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f" {self.name} - {self.min_time} - {self.max_time} {self.duration}"


class Manufacturer(models.Model):
    country = models.OneToOneField(Country, on_delete=models.CASCADE)
    lead_time = models.ManyToManyField(ManufacturerLead)
    cost = models.FloatField(default =0)
   
    def __str__(self):
        return f" {self.country.name}"

#kgCO2e/kw
class CountryCO2Intensity(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    value = models.FloatField(default=0)

    # def __str__(self):
    #     return f"CO2 Intensity in {self.country.name} is {self.value}"


class HeatTreatment(models.Model):
    name = models.CharField(max_length=40)
    mega_joules_per_kg = models.FloatField(default=0)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    cost_per_kg = models.FloatField(default=0)
    

    def __str__(self):
        return self.name


class Coatings(models.Model):
    name = models.CharField(max_length=40)
    mega_joules_per_mm_sqaure= models.FloatField(default=0)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    cost_per_mm2 = models.FloatField(default=0)

    def __str__(self):
        return self.name


class Inspections(models.Model):
    name = models.CharField(max_length=40)
    kilowatt_hours_per_mm_sqaure  = models.FloatField(default=0, null=False, blank=False)
    country = models.ForeignKey(Country, on_delete=models.CASCADE,null=True,blank=True)
    cost_per_mm2 = models.FloatField(default=0)

    def __str__(self):
        return self.name


class Product(models.Model):
    file = models.FileField(upload_to='stp_file/')  # Set the upload path to 'stp_file/' or any desired directory
    name = models.CharField(max_length=100)

    length = models.FloatField(default=0)
    width = models.FloatField(default=0)
    height = models.FloatField(default=0)

    volume_mm3 = models.FloatField(default=0)
    area_mm2 = models.FloatField(default=0)
    finished_weight = models.FloatField(default=0)
    quantity =models.PositiveIntegerField(default=1)

    length_extend_percentage = models.FloatField(default=0, null=False, blank=False)
    width_extend_percentage = models.FloatField(default=0, null=False, blank=False)
    height_extend_percentage = models.FloatField(default=0, null=False, blank=False)

    # over length in mm
    over_length_in_mm = models.FloatField( default=0)

    over_length_mm = models.FloatField(default=0) 
    over_width_mm = models.FloatField(default=0) 
    over_height_mm = models.FloatField(default=0) 

    # Initial values

    final_length = models.FloatField(default=0) 
    final_width = models.FloatField(default=0)  
    final_height = models.FloatField(default=0) 

    final_volume_mm3 = models.FloatField(default=0)
    final_area_mm2 = models.FloatField(default=0)
    
    billet_volume =models.FloatField(default=0)
    billet_weight =models.FloatField(default=0)

    material = models.ForeignKey(Material, on_delete=models.CASCADE, null=True, blank=True)
    heat_treatment = models.ForeignKey(HeatTreatment, on_delete=models.CASCADE,null=True,blank=True)
    inspection = models.ForeignKey(Inspections,on_delete=models.CASCADE,null=True,blank=True)
    coating = models.ForeignKey(Coatings,on_delete=models.CASCADE, null=True, blank=True)

    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True)
    manufacturer_lead = models.ForeignKey(ManufacturerLead, on_delete=models.CASCADE, null=True, blank=True)

    co2_intensity = models.ForeignKey(CountryCO2Intensity, on_delete=models.CASCADE, null=True, blank=True)
    carbon_footprint_CO2 = models.PositiveIntegerField(default=0)
    # tolerance =  To be added 

    kg_CO2e_material = models.FloatField(default=0)
    kg_CO2e_machining = models.FloatField(default=0)
    kg_CO2e_treatment = models.FloatField(default=0)
    kg_CO2e_inspection = models.FloatField(default=0)
    kg_CO2e_coating = models.FloatField(default=0)

    # cost fields
    cost_coating  = models.FloatField(default=0)
    cost_inspection  = models.FloatField(default=0)
    cost_heat_treatment  = models.FloatField(default=0)
    cost_machining  = models.FloatField(default=0)
    cost_material  = models.FloatField(default=0)

    machining_mm3_coeff_removed_price = models.FloatField(default=0)
    machining_mm2_coeff_finished_price = models.FloatField(default=0)
    # total_cost = models.FloatField(default=0)
    surface_area = models.FloatField(default=0)
    added_in_basket = models.BooleanField(default=False)

    # def __str__(self):
    #     return self.name
    
    def save(self, *args, **kwargs):

        if self.country:  
            self.co2_intensity = CountryCO2Intensity.objects.filter(country = self.country).first()
            
            self.over_length_mm = self.length + self.over_length_in_mm
            self.over_width_mm = self.width + self.over_length_in_mm
            self.over_height_mm = self.height + self.over_length_in_mm

            self.billet_volume =(self.over_length_mm + self.over_length_mm * self.length_extend_percentage) * (self.over_width_mm + self.over_width_mm * self.width_extend_percentage) * (self.over_height_mm + self.over_height_mm * self.height_extend_percentage)
            if self.material:
                self.billet_weight = self.billet_volume * self.material.density * 1E-9   
                self.finished_weight = self.final_volume_mm3 * self.material.density * 1E-9 
            if self.co2_intensity and self.material:
                self.kg_CO2e_machining = self.material.mega_joules_per_kg * (self.billet_weight - self.finished_weight) / 3.6 * self.co2_intensity.value * self.quantity

                self.kg_CO2e_treatment = self.heat_treatment.mega_joules_per_kg * self.billet_weight / 3.6 * self.co2_intensity.value * self.quantity
                self.kg_CO2e_inspection = self.inspection.kilowatt_hours_per_mm_sqaure * self.area_mm2 * self.co2_intensity.value * self.quantity
                self.kg_CO2e_coating = self.coating.mega_joules_per_mm_sqaure * self.area_mm2 / 3.6 * self.co2_intensity.value * self.quantity
            if self.material:
                self.kg_CO2e_material = self.material.kilo_gram_carbon_dioxide_equivalent_per_kg * self.billet_weight * self.quantity
            
                for extracted_machining_mm3_coeff_removed_price in self.material.machining_mm3_coeff_removed_price.all():
                    
                    if self.country == extracted_machining_mm3_coeff_removed_price.country:
                        self.machining_mm3_coeff_removed_price = extracted_machining_mm3_coeff_removed_price.mm3_coeff_removed_price

                for extracted_machining_mm2_coeff_finished_price in self.material.machining_mm2_coeff_finished_price.all():
                    
                    if self.country == extracted_machining_mm2_coeff_finished_price.country:
                        self.machining_mm2_coeff_finished_price = extracted_machining_mm2_coeff_finished_price.mm2_coeff_finished_price

                self.cost_material = self.billet_weight*self.material.cost_per_kg*self.quantity 
            self.cost_machining = (self.machining_mm3_coeff_removed_price * (self.billet_volume - self.final_volume_mm3)* self.quantity + self.machining_mm2_coeff_finished_price * self.final_area_mm2) * self.quantity
            self.cost_heat_treatment = self.heat_treatment.cost_per_kg * self.billet_weight * self.quantity
            self.cost_inspection = self.inspection.cost_per_mm2 * self.final_area_mm2 * self.quantity     
            self.cost_coating = self.coating.cost_per_mm2 * self.final_area_mm2 * self.quantity

            self.surface_area = 2*(self.over_length_mm * self.over_width_mm + self.over_length_mm * self.over_height_mm + self.over_width_mm * self.over_height_mm) * 1E-6
            self.carbon_footprint_CO2 =  (self.kg_CO2e_machining + self.kg_CO2e_treatment + self.kg_CO2e_inspection + self.kg_CO2e_coating + self.kg_CO2e_material)
            # self.total_cost = (self.cost_coating + self.cost_inspection + self.cost_heat_treatment + self.cost_machining + self.cost_material)
        super().save(*args, **kwargs)


class Tolerance(models.Model):
    tolerancing = models.CharField(max_length=100, null=True, blank=True)
    tolerance = models.FloatField(null=False, default=0)
    

class TransportVehicle(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
   
    def __str__(self):
        return self.name
    

class TransportType(models.Model):
    transport_type = models.CharField(max_length=10,null=True, blank=True)    

    def __str__(self):
        return self.transport_type


class TransportCostPerKg(models.Model):    
    transport_type = models.ForeignKey(TransportType, on_delete=models.CASCADE, null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True)
    cost_per_kg = models.FloatField(null=True,blank=True)

    def __str__(self):
        return f"{self.transport_type.transport_type} - {self.country.name} - {self.cost_per_kg}"


class KgCo2ePerTonKm(models.Model):
    kgCO2e_per_txkm = models.FloatField(null=True, blank=True)
    transport_mode = models.ForeignKey(TransportVehicle, on_delete=models.CASCADE, null=True ,blank=True)

    def __str__(self):
        return f"{self.transport_mode.name} - {self.kgCO2e_per_txkm}" 


class PackagingMaterial(models.Model):
    name =  models.CharField(max_length=20)
    m2 =models.FloatField(null=True, default=0)
    weight_per_m2 = models.FloatField(null=True, default=0)
    kgCO2_per_kg =models.FloatField(null=True, default=0)
    
    def __str__(self):
        return f" {self.name} - {self.m2}" 


class TermsAndConditions(models.Model):
    accept_offset_terms_and_conditions = models.CharField(max_length=100, null=True, blank=True)
    accept_manufaturing_terms_and_conditions = models.CharField(max_length=100, null=True, blank=True)


class ShippingAddress(models.Model):
    name = models.CharField(max_length=100,null=True ,blank= True)
    company = models.CharField(max_length=100,null=True ,blank= True)
    address = models.CharField(max_length=100,null=True ,blank= True)
    city_town = models.CharField(max_length=100,null=True ,blank= True)
    state_region_province = models.CharField(max_length=100, null= True , blank= True)
    zip_postal_pinconde = models.CharField(max_length=30,null=True ,blank= True)
    country = models.CharField(max_length=50,null=True ,blank= True)
    phone_number = models.CharField(max_length=30,null=True ,blank= True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_shipping_address')
     
    def __str__(self):
        return f"{self.name} - {self.address} - {self.city_town} -{self.state_region_province} - {self.zip_postal_pinconde} - {self.phone_number}"


class Order(models.Model):
    order_id = models.CharField(max_length=100,blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE , null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', null=True, blank=True)

    products = models.ManyToManyField(Product, related_name='orders')
    manufacturer_lead = models.ForeignKey(ManufacturerLead, on_delete=models.CASCADE)

    ORDER_STATUS = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("material_cutting", "Material Cutting"),
        ("machining", "Machining"),
        ("inspection", "Inspection"),
        ("shipping", "Shipping"),
        ("order_delivery", "Order Delivery"),
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]

    carbon_footprint = models.FloatField(null=True, blank=True)
    buyer_initials = models.CharField(max_length=300, null=True, blank=True)
   
    current_status = models.CharField(max_length=20, choices=ORDER_STATUS, default='pending')

    active = models.BooleanField(default=False)
    is_delivered = models.BooleanField(default=False)
   
    order_date = models.DateTimeField(auto_now_add=True)
    promise_date = models.DateTimeField(null=True, blank=True)
    supplier_due_date = models.DateTimeField(null=True, blank=True)

    payment_method = models.CharField(max_length = 100, null=True , blank= True)
    order_total = models.FloatField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.pk}"
    
   
    def save(self, *args, **kwargs):
        # Ensure created_at is set
        if self.created_at is None:
            self.created_at = timezone.now()
        
        if self.manufacturer_lead:
            promise_date = self.manufacturer_lead.max_time
            duration_unit = self.manufacturer_lead.duration
            
            if duration_unit == 'Days':
                self.promise_date = self.created_at + timedelta(days=promise_date)
            elif duration_unit == 'Weeks':
                self.promise_date = self.created_at + timedelta(weeks=promise_date)
            else:
                # Handle any unexpected duration units
                raise ValueError(f"Unexpected duration unit: {duration_unit}")
        
        
        super().save(*args, **kwargs)


class Transport(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE, null=True, blank=True )

    transport_type = models.ForeignKey(TransportType, on_delete=models.CASCADE, null=True, blank=True, related_name='select_transport_type')
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True)
 
    transport_vehicle_one = models.ForeignKey(TransportVehicle, on_delete=models.CASCADE, null=True, blank=True, related_name='select_transport_vehicle_one')
    transport_vehicle_one_cost = models.FloatField(null=True,blank=True)

    transport_vehicle_two = models.ForeignKey(TransportVehicle, on_delete=models.CASCADE, null=True, blank=True,  related_name='select_transport_vehicle_two')
    transport_vehicle_two_cost = models.FloatField(null=True,blank=True)

    cost_transport = models.FloatField(null=True,blank=True)
    
    kgCO2e_packaging = models.FloatField(null=True,blank=True)
    kgCO2e_transport = models.FloatField(null=True,blank=True)

    def __str__(self):
        return f" {self.country.name} - {self.transport_type.transport_type} - {self.cost_transport}"

    def save(self, *args, **kwargs):
        
        packaging_weight = 0
        self.kgCO2e_packaging = 0
        packaging_material = PackagingMaterial.objects.all()
        cardboard = packaging_material[0]
        plastic_4_layers = packaging_material[1]

        packaging_weight = cardboard.m2 * cardboard.weight_per_m2 + plastic_4_layers.m2 * plastic_4_layers.weight_per_m2
        self.kgCO2e_packaging = cardboard.m2 * cardboard.weight_per_m2 * cardboard.kgCO2_per_kg + plastic_4_layers.m2 * plastic_4_layers.weight_per_m2 * plastic_4_layers.kgCO2_per_kg
        
       
        transport_cost_per_kg = 0
        transport_cost_per_kg_obj = TransportCostPerKg.objects.filter(country = self.country, transport_type = self.transport_type).first()
        if transport_cost_per_kg_obj:
            transport_cost_per_kg = transport_cost_per_kg_obj.cost_per_kg

        self.cost_transport = self.transport_type.transport_type - transport_cost_per_kg * (self.order.products.finished_weight + packaging_weight) * self.order.products.quantity
        
        
        transport_1_km = KgCo2ePerTonKm.objects.filter(transport_mode = self.transport_vehicle_one)
        transport_2_km = KgCo2ePerTonKm.objects.filter(transport_mode = self.transport_vehicle_two)

        if transport_1_km and transport_2_km:
            self.kgCO2e_transport = (( self.order.products.finished_weight + packaging_weight ) /1000 * self.transport_vehicle_one_cost * transport_1_km[0].kgCO2e_per_txkm) + (( self.order.products.finished_weight + packaging_weight ) / 1000 * self.transport_vehicle_one_cost * transport_2_km[0].kgCO2e_per_txkm ) * self.order.products.quantity
        
        super().save(*args, **kwargs)


class Quote(models.Model):

    quote_id = models.IntegerField(primary_key=True)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank= True)
    products = models.ManyToManyField(Product)
    transaction = models.ForeignKey(Transaction, on_delete= models.CASCADE, null=True, blank=True)
    total_parts = models.PositiveIntegerField(default=0,null= True , blank= True)
    total_quantity = models.PositiveIntegerField(default=0,null=True, blank= True)

    lead_time = models.DateTimeField(blank=True, null=True)  
    manufacturing_location = models.ForeignKey(Country, on_delete=models.DO_NOTHING, null=True, blank=True)

    carbon_footprint = models.IntegerField(default=0,null=True , blank= True)
    cost_to_carbon = models.IntegerField(default=0,null=True , blank=True)

    payment_method = models.CharField(max_length = 100, null=True , blank= True)
    order_sub_total = models.FloatField(default=0,null=True, blank=True)
    order_total = models.FloatField(default=0,null=True , blank= True)

    approved = models.BooleanField(default=False)

    shipping = models.ForeignKey(ShippingAddress, on_delete=models.CASCADE, blank=True, null=True)
    
    manufacturing_terms_and_conditions = models.BooleanField(default=False)
    carbon_offsetting_terms_and_conditions = models.BooleanField(default=False)

    updated_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    delivery_charges = models.FloatField(null=True , blank= True )
    tax = models.FloatField(null=True, blank=True)



    def __str__(self):
        return f"Quote ID # {self.quote_id}"
    

    def save(self, *args, **kwargs):
        
        if self.products.all().first():
            self.manufacturing_location = self.products.all().first().country
            self.total_parts = sum(True for parts in self.products.all())
            self.total_quantity = sum(int(product.quantity) if product.quantity else 0 for product in self.products.all())

        super().save(*args, **kwargs)

    
