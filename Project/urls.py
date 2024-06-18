# urls.py
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static

schema_view = get_schema_view(
    openapi.Info(
        title="OCC Maunfacturer",
        default_version='v1',
        description="Project API description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@yourproject.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    # permission_classes=(permissions.AllowAny,),
)

# Manually define the schema URL with HTTPS
# swagger_schema_url = 'https://api.staging.offsetprototypes.com/'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('admin_panel.urls')),
    path('api/customer/', include('customer_panel.urls')),
    path('auth/', include('authentication.urls')),
    path('api/', include('process_occ.urls')),
    path('api/', include('payments.urls')),  # Include payments app URLs
    # Swagger URL with HTTPS
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # ReDoc URL
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
