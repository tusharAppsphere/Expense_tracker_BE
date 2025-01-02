from django.contrib import admin
from .models import User, Category, SubCategory, Expense

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['email', 'user_type']
    list_filter = ['user_type']
    fieldsets = (
        (None, {'fields': ('email', 'password','naam')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'user_type', 'is_active', 'is_staff', 'is_superuser')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)

admin.site.register(User, CustomUserAdmin)

# Register the Category model
admin.site.register(Category)

# Register the SubCategory model
admin.site.register(SubCategory)

# Register the Expense model
admin.site.register(Expense)