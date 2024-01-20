from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
       title="API Aisle Optimizer",
       default_version='v1',
       description="",
       terms_of_service="",
       contact=openapi.Contact(email="lesueur.yohann@hotmail.fr"),
       license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0)),
    path('api/v1/', include('api.urls')),
]
