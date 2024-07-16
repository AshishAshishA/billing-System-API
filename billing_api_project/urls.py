from rest_framework.authtoken import views
from django.contrib import admin
from django.urls import path, include

from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.authentication import TokenAuthentication
import rest_framework


schema_view = get_schema_view(
   openapi.Info(
      title="Billing Sys Api",
      default_version='v1',
      description="An api for customer registrations and billing in the store",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
   authentication_classes=(TokenAuthentication,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('billing_api_app.urls')),
    path('api-token-auth/', views.obtain_auth_token),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
