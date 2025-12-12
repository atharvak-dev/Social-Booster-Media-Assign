from rest_framework import serializers
from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for Review model."""
    brand_name = serializers.CharField(source='brand.name', read_only=True)
    platform_display = serializers.CharField(source='get_platform_display', read_only=True)
    
    class Meta:
        model = Review
        fields = ['id', 'brand', 'brand_name', 'platform', 'platform_display', 
                  'rating', 'review_count', 'date', 'created_at']
        read_only_fields = ['id', 'created_at']
