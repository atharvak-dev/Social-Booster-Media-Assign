from django.db import models
from brands.models import Brand


class AICitation(models.Model):
    """Track brand mentions in AI model responses."""
    
    AI_MODEL_CHOICES = [
        ('chatgpt', 'ChatGPT'),
        ('gemini', 'Gemini'),
        ('perplexity', 'Perplexity'),
        ('copilot', 'Microsoft Copilot'),
        ('google_ai', 'Google AI Overview'),
        ('claude', 'Claude'),
    ]
    
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='citations')
    ai_model = models.CharField(max_length=50, choices=AI_MODEL_CHOICES)
    query = models.TextField(help_text='The query/prompt used')
    mentioned = models.BooleanField(default=False, help_text='Was the brand mentioned?')
    citation_context = models.TextField(blank=True, help_text='Context around the mention')
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date']
        verbose_name = 'AI Citation'
        verbose_name_plural = 'AI Citations'
    
    def __str__(self):
        status = 'mentioned' if self.mentioned else 'not mentioned'
        return f'{self.brand.name} {status} in {self.get_ai_model_display()}'
