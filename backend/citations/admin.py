from django.contrib import admin
from .models import AICitation

@admin.register(AICitation)
class AICitationAdmin(admin.ModelAdmin):
    list_display = ['brand', 'ai_model', 'mentioned', 'date']
    list_filter = ['ai_model', 'mentioned', 'date']
    search_fields = ['query', 'citation_context']
