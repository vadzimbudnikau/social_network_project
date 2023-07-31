from django.contrib import admin
from . import models

# Set custom headers and titles for the Django admin site
admin.AdminSite.site_header = 'Administration'
admin.AdminSite.site_title = 'Welcome'
admin.AdminSite.index_title = 'Welcome'
admin.AdminSite.empty_value_display = '- empty -'


@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    Custom administration panel for the 'Profile' model.

    This class customizes the display of 'Profile' model instances in the Django admin panel.
    It specifies the list of fields to be displayed for each 'Profile' instance.

    Attributes:
        list_display (list): The list of fields to be displayed for each 'Profile' instance in the admin panel.
    """
    list_display = ['user', 'date_of_birth', 'location', 'website', 'slug']
