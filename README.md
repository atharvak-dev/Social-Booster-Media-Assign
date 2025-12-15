# SocialBooster - Brand Visibility Analytics Platform

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![Django](https://img.shields.io/badge/Django-6.0+-092E20?style=flat&logo=django&logoColor=white)](https://djangoproject.com)
[![React](https://img.shields.io/badge/React-18+-61DAFB?style=flat&logo=react&logoColor=black)](https://reactjs.org)
[![NeonDB](https://img.shields.io/badge/NeonDB-PostgreSQL-00E699?style=flat)](https://neon.tech)

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

---

## 🛠️ Technology Stack

### Backend
- **Framework**: Django 6.0 with Django REST Framework
- **Database**: [NeonDB](https://neon.tech) (Serverless PostgreSQL)
- **Search API**: [SerpAPI](https://serpapi.com) for Google search results
- **Production Server**: Gunicorn with WhiteNoise for static files

### Frontend
- **Framework**: React 18 with Vite
- **Charts**: Chart.js with react-chartjs-2
- **HTTP Client**: Axios

### Deployment
- **Platform**: [Render.com](https://render.com)
- **Database**: NeonDB (Serverless PostgreSQL)
- **CI/CD**: Automated via Blueprint (`render.yaml`)

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- Node.js 18 or higher
- SerpAPI account ([Get free API key](https://serpapi.com))
- NeonDB account ([Get started](https://neon.tech))

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

# Configure environment variables (see Configuration section)

# Run database migrations
python manage.py migrate

# Seed demo data
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
# Database (NeonDB)
DATABASE_URL=postgresql://user:password@ep-xxx.pooler.neon.tech/dbname?sslmode=require

# SerpAPI (Required for Google Search)
SERPAPI_KEY=your_serpapi_key_here

# Gemini API (Required for AI Citations)
GEMINI_API_KEY=your_gemini_api_key_here

# Django Settings
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1
```

---

## 🚀 Deployment

### Production Setup (Render + NeonDB)

1. **Push to GitHub**
   ```bash
   git push origin main
   ```

2. **Deploy on Render**
   - Create a Blueprint from `render.yaml`
   - Add environment variables:
     - `DATABASE_URL` (NeonDB connection string)
     - `SERPAPI_KEY`
     - `SECRET_KEY` (auto-generated)
     - `DEBUG=False`

3. **Seed Production Data**
   ```bash
   python manage.py seed_data
   ```

For detailed deployment instructions, see [deployment_plan.md](./deployment_plan.md)

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

---

## 🔒 Security

- Environment variables for sensitive data
- CORS protection enabled
- CSRF protection for forms
- No API keys exposed to frontend
- SSL/TLS encryption for database connections

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
