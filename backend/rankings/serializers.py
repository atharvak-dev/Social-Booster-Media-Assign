from rest_framework import serializers
from .models import SearchRanking


class SearchRankingSerializer(serializers.ModelSerializer):
    """Serializer for SearchRanking model."""
    brand_name = serializers.CharField(source='brand.name', read_only=True)
    
    class Meta:
        model = SearchRanking
        fields = ['id', 'brand', 'brand_name', 'keyword', 'position', 'search_url', 'date', 'created_at']
        read_only_fields = ['id', 'created_at']
