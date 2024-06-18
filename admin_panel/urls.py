from  rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import ManageUserOrRoles, ManageCustomerViewset, ManageQuoteViewset,ManageOrdersViewSet, \
    ManageTransactionViewSet,ManageShipping,ManageManufacturer,ToleranceViewSet,\
        ManageMaterials,\
    MaterialListCreateAPIView,MaterialRetrieveUpdateDestroyAPIView,\
        CountryCO2IntensityRetrieveUpdateDestroyAPIView,CountryCo2IntesityListCreateAPIView,\
        ManageHeatTreatments,ManageInspection,ManageParentMaterial,ManageFinish,AdvancedSearchQuery,ManageReport,ManageCarbonOffset,\
        CountryViewSet,ManufacturerLeadViewset  


router = DefaultRouter()

router.register(r'manage-roles', ManageUserOrRoles, basename='manage_roles')
router.register(r'manage-customers', ManageCustomerViewset, basename='manage_customers')
router.register(r'manage-quote', ManageQuoteViewset, basename='manage_quote')
router.register(r'manage-orders', ManageOrdersViewSet, basename='manage-orders')
router.register(r'manage-transactions',ManageTransactionViewSet , basename='manage-transaction'),
router.register(r'manage-shipping',ManageShipping , basename='manage-shipping'),
router.register(r'manage-manufacturer',ManageManufacturer , basename='manage-manufacturer'),
router.register(r'manufacturer-lead',ManufacturerLeadViewset , basename='manufacturer-lead'),

router.register(r'manage-materials',ManageMaterials , basename='manage-materials'),
router.register(r'manage-heat_treatments',ManageHeatTreatments , basename='manage-heat-treatment'),
router.register(r'parent-material',ManageParentMaterial,basename= 'parent-material'),
router.register(r'manage-finish',ManageFinish,basename= 'manage-finish')
router.register(r'manage-inspection',ManageInspection , basename='manage-inspection'),

router.register(r'manage-report',ManageReport , basename='manage-report'),
router.register(r'upload-certificate',ManageCarbonOffset ,basename= 'upload_certificate' )

router.register(r'advanced-search-query', AdvancedSearchQuery,basename= 'advanced-search-query')
router.register(r'manage-country', CountryViewSet,basename= 'manage-country')


urlpatterns = [
    path('admin-panel/', include(router.urls)),

    path('materials/', MaterialListCreateAPIView.as_view(), name='material-list-create'),
    path('materials/<int:pk>/', MaterialRetrieveUpdateDestroyAPIView.as_view(), name='material-retrieve-update-destroy'),

    path('country-CO2e/', CountryCo2IntesityListCreateAPIView.as_view(), name='country_vlaue'),
    path('country-CO2e/<int:pk>/', CountryCO2IntensityRetrieveUpdateDestroyAPIView.as_view(), name='country-retrive-update-destroy')
]
