"""
Custom throttling classes for rate limiting.
"""
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle


class BurstRateThrottle(AnonRateThrottle):
    """Burst protection - prevents rapid-fire requests."""
    scope = 'burst'


class SustainedRateThrottle(UserRateThrottle):
    """Sustained rate limit for authenticated users."""
    scope = 'sustained'


class AnonSustainedRateThrottle(AnonRateThrottle):
    """Sustained rate limit for anonymous users."""
    scope = 'anon_sustained'
