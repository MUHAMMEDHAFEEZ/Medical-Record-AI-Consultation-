from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# تخصيص عنوان صفحة الإدارة
admin.site.site_header = "DR AI Administration"
admin.site.site_title = "DR AI Admin Portal"
admin.site.index_title = "Welcome to DR AI Administration"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('apps.authentication.urls')),
    path('api/medical-records/', include('apps.medical_records.urls')),
]

# Serve static files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
