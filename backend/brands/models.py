from django.db import models


class Brand(models.Model):
    """Brand model for tracking client brands."""
    
    CATEGORY_CHOICES = [
        ('software', 'Software & Technology'),
        ('ecommerce', 'E-Commerce & Retail'),
        ('finance', 'Finance & Accounting'),
        ('health', 'Health & Wellness'),
        ('food', 'Food & Beverage'),
        ('services', 'Professional Services'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')
    website = models.URLField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
