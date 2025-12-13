# SocialBooster - 5 Minute Pitch

## Project Overview

**SocialBooster** is a comprehensive **Brand Visibility Analytics Platform** that tracks and analyzes brand presence across three critical digital channels:

1. **Google Search Rankings** - Where does your brand appear in search results?
2. **AI Citations** - Is your brand being mentioned by ChatGPT, Gemini, Perplexity?
3. **Customer Reviews** - What's your reputation on Google, Yelp, Trustpilot?

---

## The Problem We Solve

In 2025, brand visibility is fragmented across traditional search, AI assistants, and review platforms. Marketing teams struggle to:

- Track rankings across multiple keywords
- Monitor if AI chatbots recommend their brand
- Aggregate reviews from 6+ platforms

**SocialBooster unifies this data into a single dashboard** with actionable insights.

---

## Tech Stack Decisions

| Layer | Technology | Why I Chose It |
|-------|-----------|----------------|
| **Backend** | Django 6.0 + DRF | Mature, robust ORM, excellent for REST APIs |
| **Frontend** | React 18 + Vite | Fast dev experience, modern component architecture |
| **Database** | NeonDB (PostgreSQL) | Serverless, auto-scaling, great free tier |
| **Hosting** | Render.com | Easy monorepo deployment, auto-SSL, Blueprint support |
| **Static Files** | WhiteNoise | Zero-config static serving from Django |

### Why Django over Node.js?
- **ORM**: Django's ORM handles complex aggregations (Avg, Count, Sum) elegantly
- **Admin Panel**: Free CRUD interface for data management
- **Security**: Built-in CSRF, XSS, SQL injection protection

### Why NeonDB over Supabase?
- **IPv4 Compatibility**: Works seamlessly with Render (no IPv6 issues)
- **Connection Pooling**: PgBouncer built-in
- **Branching**: Database branching for dev/prod separation

---

## Architecture Decisions

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   React     │────▶│   Django    │────▶│   NeonDB    │
│  (Vite)     │ API │   (DRF)     │ SQL │ (PostgreSQL)│
└─────────────┘     └─────────────┘     └─────────────┘
       │                   │
       └───── Both served by Render.com ─────┘
```

### Key Design Patterns:

1. **ViewSets + Routers**: DRF ViewSets reduce boilerplate by 70%
2. **Select Related**: Eager loading foreign keys prevents N+1 queries
3. **Database Aggregation**: Push calculations to PostgreSQL, not Python
4. **SPA Routing**: Django serves React's `index.html` for all non-API routes

---

## Features Implemented

### Dashboard
- **Overview Cards**: Brands, Avg Position, Citation Rate, Avg Rating
- **Ranking Trends Chart**: Line chart showing position changes over time
- **Citation Breakdown**: Pie chart by AI model (ChatGPT, Gemini, etc.)
- **Brand Comparison**: Bar chart comparing visibility scores

### Brand Management
- CRUD operations with auto-fetch capability
- Background data fetching via threading

### Search Rankings
- Filter by brand, keyword, date range
- Trend analysis per keyword
- Summary statistics

### AI Citations
- Track mentions across 6 AI platforms
- Breakdown by model with citation rates
- Filter by mentioned/not mentioned

### Reviews
- Aggregate from 6 platforms (Google, Yelp, Trustpilot, G2, Capterra, Glassdoor)
- Platform-wise breakdown
- Rating trends

---

## Challenges & Solutions

### Challenge 1: Database Connection Issues
**Problem**: Supabase IPv6 incompatibility with Render  
**Solution**: Migrated to NeonDB with IPv4 pooler endpoint

### Challenge 2: Static File Serving
**Problem**: React assets returning 404 or wrong MIME type  
**Solution**: Configured Vite `base: '/static/'` + WhiteNoise middleware

### Challenge 3: SPA Routing in Django
**Problem**: React Router URLs returning Django 404  
**Solution**: Created catch-all view serving `index.html` for non-API routes

### Challenge 4: Query Performance
**Problem**: N+1 queries in dashboard (4 queries × N brands)  
**Solution**: Used `select_related()` and database-level aggregation

---

## Code Quality Practices

1. **Type Safety**: Clear model definitions with choices and help_text
2. **Error Handling**: Try-catch with meaningful error responses
3. **Documentation**: Docstrings on all ViewSets and actions
4. **DRY Principle**: Reusable `get_queryset()` filters
5. **Security**: Environment variables for secrets, CORS configuration

---

## Deployment Architecture

```yaml
# render.yaml - Infrastructure as Code
services:
  - type: web
    name: socialbooster
    env: python
    buildCommand: "pip install ... && npm build && collectstatic"
    startCommand: "gunicorn socialbooster.wsgi"
    envVars:
      - DATABASE_URL: (from NeonDB)
      - SECRET_KEY: (auto-generated)
```

**Single command deployment**: Push to GitHub → Render auto-deploys

---

## Future Improvements

1. **Real-time Data**: WebSockets for live ranking updates
2. **API Integrations**: SerpAPI for live Google rankings, OpenAI for AI citation checking
3. **Caching**: Redis for expensive aggregations
4. **Background Jobs**: Celery for scheduled data fetching
5. **Multi-tenancy**: User accounts with isolated brand data

---

## Demo

**Live URL**: https://social-booster-media-assign-1.onrender.com

**Key Flows**:
1. Dashboard loads with aggregated stats and charts
2. Navigate to Brands → View 8 seeded companies
3. Search Rankings → Filter by keyword or date
4. AI Citations → See breakdown by AI model
5. Reviews → Platform-wise rating analysis

---

## Conclusion

SocialBooster demonstrates:

- ✅ Full-stack development (Django + React)
- ✅ RESTful API design with DRF
- ✅ Database optimization (select_related, aggregation)
- ✅ Cloud deployment (Render + NeonDB)
- ✅ Modern frontend build (Vite)
- ✅ Professional code organization

**Thank you for reviewing my project!**

---

*Built by: [Your Name]*  
*GitHub: https://github.com/atharvak-dev/Social-Booster-Media-Assign*
