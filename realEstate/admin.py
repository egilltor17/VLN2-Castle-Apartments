from django.contrib import admin

from .models import Address, Attribute, Property, PropertyImage
# Register your models here.


class PropertyInline(admin.StackedInline):
    model = Property
    extra = 1
    max_num = 1


class PropertyImageInline(admin.StackedInline):
    model = PropertyImage
    extra = 2


class AddressAdmin(admin.ModelAdmin):
    inlines = [PropertyInline]


class PropertyAdmin(admin.ModelAdmin):
    inlines = [PropertyImageInline]


admin.site.register(Property, PropertyAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(Attribute)