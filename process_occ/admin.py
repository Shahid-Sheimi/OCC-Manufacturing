from django.contrib import admin
from .models import HeatTreatment,Manufacturer,Material,Coatings,Inspections,\
    Order,Product,CountryCO2Intensity, Country, MaterialMM2FinishedPrice,\
          MaterialMM3RemovedPrice, ParentMaterial,\
              Transport, TransportVehicle, KgCo2ePerTonKm, PackagingMaterial,\
                  TransportCostPerKg, TransportType, ManufacturerLead, Tolerance, Quote, ShippingAddress

admin.site.register(HeatTreatment)
admin.site.register(Manufacturer)
admin.site.register(ManufacturerLead)
admin.site.register(ParentMaterial)
admin.site.register(Material)
admin.site.register(Coatings)
admin.site.register(Inspections)
admin.site.register(Order)
admin.site.register(Product)
admin.site.register(CountryCO2Intensity)
admin.site.register( Country)
admin.site.register( MaterialMM2FinishedPrice)
admin.site.register( MaterialMM3RemovedPrice)
admin.site.register(Tolerance)
admin.site.register( Transport)
admin.site.register(TransportVehicle)
admin.site.register(KgCo2ePerTonKm)
admin.site.register(PackagingMaterial)
admin.site.register(TransportCostPerKg)
admin.site.register(TransportType)
admin.site.register(Quote)
admin.site.register(ShippingAddress)
