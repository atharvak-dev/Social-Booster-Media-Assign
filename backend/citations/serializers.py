from rest_framework import serializers
from .models import AICitation


class AICitationSerializer(serializers.ModelSerializer):
    """Serializer for AICitation model."""
    brand_name = serializers.CharField(source='brand.name', read_only=True)
    ai_model_display = serializers.CharField(source='get_ai_model_display', read_only=True)
    
    class Meta:
        model = AICitation
        fields = ['id', 'brand', 'brand_name', 'ai_model', 'ai_model_display', 
                  'query', 'mentioned', 'citation_context', 'date', 'created_at']
        read_only_fields = ['id', 'created_at']
