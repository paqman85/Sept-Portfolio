from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    modeladmin_register,
)
from .models import Subscriber


class SubscriberAdmin(ModelAdmin):
    """Subscriber Admin"""

    model = Subscriber
    menu_label = "Subscribers"
    menu_icon = "user"
    menu_order=290
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("full_name","email",)
    search_fields = ("full_name","email",)


modeladmin_register(SubscriberAdmin)

