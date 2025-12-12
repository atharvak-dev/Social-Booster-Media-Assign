from django.contrib import admin
from .models import Brand

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'website', 'created_at']
    list_filter = ['category', 'created_at']
    search_fields = ['name', 'website']
