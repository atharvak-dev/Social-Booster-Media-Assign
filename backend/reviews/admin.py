from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['brand', 'platform', 'rating', 'review_count', 'date']
    list_filter = ['platform', 'date']
    search_fields = ['brand__name']
