from django.contrib import admin
from django.contrib.auth.models import User

from .models import Address, Profile, PaymentInfo, Purchase, RecentlyViewed, Favorites
# Register your models here.


class ProfileInline(admin.StackedInline):
    model = Profile
    extra = 1
    max_num = 1


class FavoritesInline(admin.StackedInline):
    model = Favorites
    extra = 0


class RecViewInline(admin.StackedInline):
    model = RecentlyViewed
    extra = 0


class PurchaseInline(admin.StackedInline):
    model = Purchase
    extra = 0


class RecViewInline(admin.StackedInline):
    model = RecentlyViewed
    extra = 0


class UserAdmin(admin.ModelAdmin):
    inlines = [ProfileInline, RecViewInline, FavoritesInline, PurchaseInline]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
