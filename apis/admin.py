from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('email', 'is_staff', 'is_active', 'is_doc' , 'photo' , 'profession' ,'address')
    list_filter = ('email', 'is_staff', 'is_active', 'is_doc'  , 'profession' ,'address')
    fieldsets = (
        (None, {'fields': ('email', 'password' , 'first_name' , 'last_name' ,  'photo' , 'profession' ,'address','city','bgroup','state')}),
        ('Permissions', {'fields': ('is_staff', 'is_active' , 'is_doc')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active' , 'is_doc' , 'photo' , 'profession' ,'address')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(CustomUser, CustomUserAdmin)