from django.contrib import admin
from .models import SearchRanking

@admin.register(SearchRanking)
class SearchRankingAdmin(admin.ModelAdmin):
    list_display = ['brand', 'keyword', 'position', 'date']
    list_filter = ['brand', 'date']
    search_fields = ['keyword']
