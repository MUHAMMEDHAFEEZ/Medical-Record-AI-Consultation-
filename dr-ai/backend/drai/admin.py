from django.contrib import admin
from django.contrib.admin import AdminSite

# تخصيص عنوان صفحة الإدارة
admin.site.site_header = "DR AI Administration"
admin.site.site_title = "DR AI Admin Portal"
admin.site.index_title = "Welcome to DR AI Administration"

# تخصيص النمط
class CustomAdminSite(AdminSite):
    site_header = "DR AI Administration"
    site_title = "DR AI Admin Portal"
    index_title = "Welcome to DR AI Administration"

    def each_context(self, request):
        context = super().each_context(request)
        context['site_logo'] = 'admin/img/logo.png'
        return context

# استبدال موقع الإدارة الافتراضي بالموقع المخصص
admin.site.__class__ = CustomAdminSite
