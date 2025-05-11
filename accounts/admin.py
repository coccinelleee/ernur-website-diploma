from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html

from .models import Account, UserProfile

# Register your models here.


class AccountAdmin(UserAdmin):
    list_display = ('электрондық_пошта', 'аты_жөні', 'тегі', 'username', 'last_login', 'date_joined', 'is_active')
    list_display_links = ('электрондық_пошта', 'аты_жөні', 'тегі')
    readonly_fields = ('last_login', 'date_joined')
    ordering = ('-date_joined',)

    fieldsets = (
        (None, {'fields': ('электрондық_пошта', 'password')}),
        ('Personal Info', {'fields': ('аты_жөні', 'тегі', 'телефон_нөмірі', 'username')}),
        ('Permissions', {'fields': ('is_admin', 'is_staff', 'is_active', 'is_superadmin', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('электрондық_пошта', 'аты_жөні', 'тегі', 'телефон_нөмірі', 'username', 'password1', 'password2'),
        }),
    )

    search_fields = ('электрондық_пошта', 'username')
    filter_horizontal = ()
    list_filter = ()

class UserProfileAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        return format_html('<img src="{}" style="border-radius:50%; height:50px; width:50px;"'.format(object.profile_picture.url))
    thumbnail.short_description = 'Profile Picture'
    list_display = ('thumbnail', 'user', 'city', 'state', 'country')


admin.site.register(Account, AccountAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
