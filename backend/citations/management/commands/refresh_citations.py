"""
Management command to refresh AI citations using real Gemini API.
"""
import time
import random
from datetime import date, timedelta
from django.core.management.base import BaseCommand
from brands.models import Brand
from citations.models import AICitation
from integrations.gemini_service import GeminiService


class Command(BaseCommand):
    help = 'Refresh AI citations for all brands using real Gemini API'

    def add_arguments(self, parser):
        parser.add_argument(
            '--brand',
            type=str,
            help='Refresh citations for a specific brand name only',
        )
        parser.add_argument(
            '--generate-history',
            action='store_true',
            help='Generate simulated historical data for past 14 days',
        )
        parser.add_argument(
            '--days',
            type=int,
            default=14,
            help='Number of days of historical data to generate (default: 14)',
        )

    def handle(self, *args, **options):
        if options['generate_history']:
            return self._generate_historical_data(options)
        
        return self._refresh_with_gemini(options)
    
    def _generate_historical_data(self, options):
        """Generate realistic simulated historical citation data."""
        days = options['days']
        brands = Brand.objects.all()
        
        if options['brand']:
            brands = brands.filter(name__icontains=options['brand'])
        
        self.stdout.write(f'Generating {days} days of historical data for {brands.count()} brands...')
        
        # Clear existing data
        AICitation.objects.all().delete()
        
        ai_models = ['chatgpt', 'gemini', 'perplexity', 'copilot', 'claude']
        queries_per_day = 2
        
        # Brand popularity scores (affects mention probability)
        brand_popularity = {
            'Slack': 0.85,
            'Notion': 0.80,
            'Figma': 0.90,
            'Stripe': 0.88,
            'Shopify': 0.82,
            'HubSpot': 0.75,
            'Mailchimp': 0.70,
            'Zoom': 0.92,
        }
        
        total_created = 0
        
        for brand in brands:
            base_probability = brand_popularity.get(brand.name, 0.6)
            
            for day_offset in range(days):
                check_date = date.today() - timedelta(days=day_offset)
                
                for ai_model in ai_models:
                    # Each AI model has slightly different mention rates
                    model_modifier = {
                        'chatgpt': 0.05,
                        'gemini': 0.0,
                        'perplexity': 0.08,
                        'copilot': -0.05,
                        'claude': 0.03,
                    }.get(ai_model, 0)
                    
                    for _ in range(queries_per_day):
                        # Calculate if mentioned (with some daily variance)
                        daily_variance = random.uniform(-0.1, 0.1)
                        mention_prob = base_probability + model_modifier + daily_variance
                        mentioned = random.random() < mention_prob
                        
                        query = random.choice([
                            f"What is {brand.name}?",
                            f"Tell me about {brand.name}",
                            f"Is {brand.name} a good choice?",
                            f"Compare {brand.name} to alternatives",
                            f"Top features of {brand.name}",
                        ])
                        
                        context = f"{brand.name} is a popular tool..." if mentioned else "Brand not mentioned"
                        
                        AICitation.objects.create(
                            brand=brand,
                            ai_model=ai_model,
                            query=query,
                            mentioned=mentioned,
                            citation_context=context,
                            date=check_date
                        )
                        total_created += 1
        
        self.stdout.write(self.style.SUCCESS(
            f'✓ Created {total_created} historical citation records across {days} days'
        ))
    
    def _refresh_with_gemini(self, options):
        """Refresh citations using real Gemini API with semantic detection."""
        service = GeminiService()
        
        # Test API connection
        self.stdout.write('Testing Gemini API connection...')
        test_result = service.test_connection()
        
        if not test_result.get('success'):
            self.stdout.write(self.style.ERROR(
                f"Gemini API connection failed: {test_result.get('error')}"
            ))
            return
        
        self.stdout.write(self.style.SUCCESS('✓ Gemini API connection successful'))
        
        # Get brands to process
        if options['brand']:
            brands = Brand.objects.filter(name__icontains=options['brand'])
        else:
            brands = Brand.objects.all()
        
        if not brands.exists():
            self.stdout.write(self.style.WARNING('No brands found'))
            return
        
        self.stdout.write(f'\nRefreshing citations for {brands.count()} brands...\n')
        
        # Clear existing Gemini citations for today
        AICitation.objects.filter(ai_model='gemini', date=date.today()).delete()
        
        total_mentions = 0
        total_checks = 0
        
        for brand in brands:
            self.stdout.write(f'\n🔍 Checking: {brand.name}')
            
            queries = [
                f"What is {brand.name} and what does it do?",
                f"Tell me about {brand.name}'s main features",
            ]
            
            for query in queries:
                time.sleep(2)  # Rate limit delay
                
                result = service.check_brand_citation(brand.name, query)
                
                mentioned = result.get('mentioned', False)
                context = result.get('citation_context', 'Unable to check')
                is_semantic = result.get('semantic_match', False)
                
                AICitation.objects.create(
                    brand=brand,
                    ai_model='gemini',
                    query=query,
                    mentioned=mentioned,
                    citation_context=context[:500] if context else '',
                    date=date.today()
                )
                
                total_checks += 1
                if mentioned:
                    total_mentions += 1
                    match_type = "(semantic)" if is_semantic else "(direct)"
                    self.stdout.write(self.style.SUCCESS(
                        f'  ✓ Mentioned {match_type}: "{query[:35]}..."'
                    ))
                else:
                    self.stdout.write(self.style.WARNING(
                        f'  ✗ Not mentioned: "{query[:35]}..."'
                    ))
        
        rate = 100 * total_mentions // total_checks if total_checks else 0
        self.stdout.write(self.style.SUCCESS(
            f'\n\n✓ Completed! {total_mentions}/{total_checks} citations found ({rate}% rate)'
        ))
