from django.db import models
from brands.models import Brand


class Review(models.Model):
    """Track brand reviews across platforms."""
    
    PLATFORM_CHOICES = [
        ('google', 'Google Reviews'),
        ('yelp', 'Yelp'),
        ('trustpilot', 'Trustpilot'),
        ('g2', 'G2'),
        ('capterra', 'Capterra'),
        ('glassdoor', 'Glassdoor'),
    ]
    
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='reviews')
    platform = models.CharField(max_length=50, choices=PLATFORM_CHOICES)
    rating = models.DecimalField(max_digits=2, decimal_places=1, help_text='Rating out of 5')
    review_count = models.IntegerField(default=0)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date']
        unique_together = ['brand', 'platform', 'date']
    
    def __str__(self):
        return f'{self.brand.name} on {self.get_platform_display()}: {self.rating}/5'
