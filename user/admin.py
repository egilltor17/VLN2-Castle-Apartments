from django.contrib import admin
from django.contrib.auth.models import User

from .models import Profile


# Register your models here.


class ProfileInline(admin.StackedInline):
    model = Profile
    extra = 1
    max_num = 1


class UserAdmin(admin.ModelAdmin):
    # fieldsets = [
    #     (None, {'fields': ['question_text']}),
    #     ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    # ]
    inlines = [ProfileInline]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Profile)
