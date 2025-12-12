# SocialBooster - Brand Visibility Analytics Platform

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![Django](https://img.shields.io/badge/Django-4.2+-092E20?style=flat&logo=django&logoColor=white)](https://djangoproject.com)
[![React](https://img.shields.io/badge/React-18+-61DAFB?style=flat&logo=react&logoColor=black)](https://reactjs.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A comprehensive analytics platform for tracking brand visibility across search engines, AI platforms, and review sites. Monitor your brand's Google search rankings, AI citations, and customer reviews in one unified dashboard.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🏢 **Brand Management** | Full CRUD operations for tracking multiple client brands |
| 🔍 **Search Rankings** | Real-time Google search position tracking via SerpAPI |
| 🤖 **AI Citations** | Monitor brand mentions in ChatGPT, Gemini, Perplexity, Claude |
| ⭐ **Review Analytics** | Track ratings across Google, Trustpilot, G2, and more |
| 📊 **Interactive Dashboard** | Beautiful visualizations with Chart.js |
| 🔄 **Auto-Fetch** | Automatically fetch data when new brands are added |

---

## 🛠️ Technology Stack

### Backend
- **Framework**: Django 4.2+ with Django REST Framework
- **Database**: SQLite (development) / PostgreSQL (production)
- **Search API**: [SerpAPI](https://serpapi.com) for Google search results

### Frontend
- **Framework**: React 18 with Vite
- **Charts**: Chart.js with react-chartjs-2
- **HTTP Client**: Axios

---

## � Project Structure

```
SocialBooster/
├── backend/
│   ├── socialbooster/       # Django project settings
│   ├── brands/              # Brand management & auto-fetch
│   ├── rankings/            # Search ranking tracking
│   ├── citations/           # AI citation monitoring
│   ├── reviews/             # Review aggregation
│   ├── dashboard/           # Analytics & reporting
│   ├── integrations/        # SerpAPI integration
│   ├── .env                 # Environment variables
│   └── manage.py
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── services/        # API client
│   │   └── App.jsx
│   └── package.json
└── README.md
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- Node.js 18 or higher
- SerpAPI account ([Get free API key](https://serpapi.com))

### 1. Clone the Repository

```bash
git clone <repository-url>
cd SocialBooster
```

### 2. Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
# Create .env file with your SerpAPI key (see Configuration section)

# Run database migrations
python manage.py migrate

# (Optional) Seed demo data
python manage.py seed_data

# Start development server
python manage.py runserver
```

Backend API: `http://localhost:8000`

### 3. Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend App: `http://localhost:3000`

---

## ⚙️ Configuration

Create a `.env` file in the `backend/` directory:

```env
# SerpAPI (Required for Google Search)
SERPAPI_KEY=your_serpapi_key_here

# Django Settings
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# Supabase (Optional - for cloud database)
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-supabase-key

# PostgreSQL (Optional - for production)
# DATABASE_URL=postgresql://user:pass@host:port/dbname
```

---

## 📡 API Reference

### Brands

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/brands/` | List all brands |
| `POST` | `/api/brands/` | Create a brand (auto-fetches search data) |
| `GET` | `/api/brands/{id}/` | Get brand details |
| `PUT` | `/api/brands/{id}/` | Update brand |
| `DELETE` | `/api/brands/{id}/` | Delete brand |

### Search Rankings

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/rankings/` | List rankings (filterable) |
| `POST` | `/api/rankings/` | Create ranking entry |
| `GET` | `/api/rankings/trends/{brand_id}/` | Get ranking trends |
| `GET` | `/api/rankings/summary/` | Get summary statistics |

### AI Citations

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/citations/` | List citations (filterable) |
| `POST` | `/api/citations/` | Create citation entry |
| `GET` | `/api/citations/breakdown/` | Breakdown by AI model |
| `GET` | `/api/citations/summary/` | Summary statistics |

### Reviews

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/reviews/` | List reviews (filterable) |
| `POST` | `/api/reviews/` | Create review entry |
| `GET` | `/api/reviews/summary/` | Summary by platform |

### Dashboard

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/dashboard/overview/` | Dashboard statistics & charts |
| `GET` | `/api/dashboard/export/` | Export all data as JSON |

### Integrations (SerpAPI)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/integrations/search/` | Search brand position for keyword |
| `POST` | `/api/integrations/bulk-search/` | Bulk search multiple keywords |
| `GET` | `/api/integrations/usage/` | Check API usage/credits |

---

## � Usage Examples

### Create a Brand

```bash
curl -X POST http://localhost:8000/api/brands/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Acme Corp",
    "category": "software",
    "website": "https://acme.com"
  }'
```

> **Note:** Creating a brand automatically triggers a background search to fetch real Google rankings.

### Search Brand Position

```bash
curl -X POST http://localhost:8000/api/integrations/search/ \
  -H "Content-Type: application/json" \
  -d '{
    "brand_id": 1,
    "keyword": "project management software"
  }'
```

### Get Dashboard Overview

```bash
curl http://localhost:8000/api/dashboard/overview/
```

---

## 🎨 UI Features

- **Modern Dark Theme** with glassmorphism effects
- **Responsive Design** for all screen sizes
- **Interactive Charts** with hover effects
- **Real-time Updates** when data changes

---

## 📊 Supported Platforms

### Search Engines
- Google (via SerpAPI)

### AI Platforms
- ChatGPT
- Google Gemini
- Perplexity
- Microsoft Copilot
- Claude
- Google AI Overview

### Review Sites
- Google Reviews
- Trustpilot
- G2
- Capterra
- Yelp
- Glassdoor

---

## 🔒 Security

- Environment variables for sensitive data
- CORS protection enabled
- CSRF protection for forms
- No API keys exposed to frontend

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📞 Support

For support, please open an issue in the repository or contact the maintainers.

---

<p align="center">
  Made with ❤️ for brand visibility tracking
</p>
# Social-Booster-Media-Assign
