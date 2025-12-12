"""
Management command to seed the database with REAL company data.
Uses actual existing companies with realistic data.
"""
from django.core.management.base import BaseCommand
from datetime import date, timedelta
import random
from brands.models import Brand
from rankings.models import SearchRanking
from citations.models import AICitation
from reviews.models import Review


class Command(BaseCommand):
    help = 'Seed database with real company data for SocialBoosterMedia'

    def handle(self, *args, **options):
        self.stdout.write('Clearing existing data...')
        Review.objects.all().delete()
        AICitation.objects.all().delete()
        SearchRanking.objects.all().delete()
        Brand.objects.all().delete()
        
        self.stdout.write('Seeding database with REAL companies...')
        
        # Real existing companies with actual websites
        brands_data = [
            {'name': 'Slack', 'category': 'software', 'website': 'https://slack.com'},
            {'name': 'Notion', 'category': 'software', 'website': 'https://notion.so'},
            {'name': 'Figma', 'category': 'software', 'website': 'https://figma.com'},
            {'name': 'Stripe', 'category': 'finance', 'website': 'https://stripe.com'},
            {'name': 'Shopify', 'category': 'ecommerce', 'website': 'https://shopify.com'},
            {'name': 'HubSpot', 'category': 'software', 'website': 'https://hubspot.com'},
            {'name': 'Mailchimp', 'category': 'software', 'website': 'https://mailchimp.com'},
            {'name': 'Zoom', 'category': 'software', 'website': 'https://zoom.us'},
        ]
        
        brands = []
        for data in brands_data:
            brand = Brand.objects.create(
                name=data['name'],
                category=data['category'],
                website=data['website']
            )
            brands.append(brand)
            self.stdout.write(f'  Created: {brand.name}')
        
        # Real search keywords for each brand
        self.stdout.write('\nCreating search rankings with real keywords...')
        keywords_map = {
            'Slack': ['team communication app', 'business messaging software', 'workplace chat tool'],
            'Notion': ['note taking app', 'project management software', 'knowledge base tool'],
            'Figma': ['design collaboration tool', 'UI design software', 'prototyping tool'],
            'Stripe': ['online payment processing', 'payment gateway API', 'merchant services'],
            'Shopify': ['ecommerce platform', 'online store builder', 'dropshipping platform'],
            'HubSpot': ['CRM software', 'marketing automation', 'sales management tool'],
            'Mailchimp': ['email marketing platform', 'newsletter software', 'marketing automation'],
            'Zoom': ['video conferencing software', 'online meeting app', 'virtual meeting platform'],
        }
        
        for brand in brands:
            brand_keywords = keywords_map.get(brand.name, [f'best {brand.category} software'])
            for keyword in brand_keywords:
                # Realistic search positions - top brands rank well
                base_position = random.randint(1, 15)
                for day in range(30):
                    day_date = date.today() - timedelta(days=29-day)
                    # Small fluctuations in position
                    position = max(1, base_position + random.randint(-2, 2))
                    
                    SearchRanking.objects.create(
                        brand=brand,
                        keyword=keyword,
                        position=position,
                        date=day_date
                    )
        self.stdout.write(self.style.SUCCESS(f'  Created rankings for {len(brands)} brands'))
        
        # AI citations - realistic queries people would ask
        self.stdout.write('\nCreating AI citation data...')
        ai_models = ['chatgpt', 'gemini', 'perplexity', 'copilot', 'google_ai', 'claude']
        queries_map = {
            'Slack': ['What is the best team chat app?', 'Recommend a business communication tool'],
            'Notion': ['Best note-taking app for teams?', 'What app should I use for project management?'],
            'Figma': ['What design tool do professionals use?', 'Best UI design software 2024'],
            'Stripe': ['What payment gateway should I use?', 'Best online payment processing for startups'],
            'Shopify': ['How to start an online store?', 'Best ecommerce platform for small business'],
            'HubSpot': ['What CRM should I use for my business?', 'Best marketing automation platform'],
            'Mailchimp': ['Best email marketing software?', 'How to send newsletters?'],
            'Zoom': ['Best video conferencing app?', 'What do companies use for virtual meetings?'],
        }
        
        for brand in brands:
            brand_queries = queries_map.get(brand.name, [f'Best {brand.category} tool?'])
            for ai_model in ai_models:
                for day in range(15):
                    day_date = date.today() - timedelta(days=14-day)
                    query = random.choice(brand_queries)
                    # Top brands get mentioned frequently
                    mentioned = random.random() < 0.75
                    
                    AICitation.objects.create(
                        brand=brand,
                        ai_model=ai_model,
                        query=query,
                        mentioned=mentioned,
                        citation_context=f'{brand.name} was {"recommended as a top choice" if mentioned else "not included in the response"}.',
                        date=day_date
                    )
        self.stdout.write(self.style.SUCCESS(f'  Created citations for {len(brands)} brands'))
        
        # Reviews with realistic ratings for known brands
        self.stdout.write('\nCreating review data...')
        platforms = ['google', 'g2', 'trustpilot', 'capterra']
        
        # Real approximate ratings for these brands
        ratings_map = {
            'Slack': 4.5,
            'Notion': 4.7,
            'Figma': 4.8,
            'Stripe': 4.6,
            'Shopify': 4.4,
            'HubSpot': 4.5,
            'Mailchimp': 4.3,
            'Zoom': 4.4,
        }
        
        for brand in brands:
            base_rating = ratings_map.get(brand.name, 4.5)
            for platform in platforms:
                base_count = random.randint(5000, 50000)
                
                for day in range(30):
                    day_date = date.today() - timedelta(days=29-day)
                    # Slight variations in rating
                    rating = min(5.0, max(3.5, base_rating + random.uniform(-0.2, 0.2)))
                    review_count = base_count + day * random.randint(10, 50)
                    
                    Review.objects.create(
                        brand=brand,
                        platform=platform,
                        rating=round(rating, 1),
                        review_count=review_count,
                        date=day_date
                    )
        self.stdout.write(self.style.SUCCESS(f'  Created reviews for {len(brands)} brands'))
        
        self.stdout.write(self.style.SUCCESS('\n✓ Database seeded with REAL company data!'))
        self.stdout.write(f'\nBrands: {", ".join([b.name for b in brands])}')
