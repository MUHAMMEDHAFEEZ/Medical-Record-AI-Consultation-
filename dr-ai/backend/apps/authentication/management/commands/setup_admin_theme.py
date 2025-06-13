from django.core.management.base import BaseCommand
from admin_interface.models import Theme

class Command(BaseCommand):
    help = 'Setup custom admin theme for Dr AI'

    def handle(self, *args, **options):
        # Get or create the default theme
        theme = Theme.objects.get_or_create(name='Dr AI Theme')[0]

        # Update theme settings
        theme.title = 'Dr AI Administration'
        theme.title_visible = True
        theme.logo_visible = True
        theme.title_color = '#FFFFFF'
        theme.css_header_background_color = '#2c3e50'
        theme.css_header_text_color = '#FFFFFF'
        theme.css_header_link_color = '#FFFFFF'
        theme.css_header_link_hover_color = '#3498db'
        theme.save()

        self.stdout.write(
            self.style.SUCCESS('Successfully created/updated admin theme')
        )
