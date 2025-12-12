from django.db import models
from brands.models import Brand


class SearchRanking(models.Model):
    """Track Google search rankings for brand keywords."""
    
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='rankings')
    keyword = models.CharField(max_length=300)
    position = models.IntegerField(help_text='Search result position (1-100)')
    search_url = models.URLField(max_length=1000, blank=True)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date', 'position']
        unique_together = ['brand', 'keyword', 'date']
    
    def __str__(self):
        return f'{self.brand.name} - "{self.keyword}" at position {self.position}'
