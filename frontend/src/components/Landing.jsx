import { useState, useEffect } from 'react';
import { authUtils } from '../services/api';

export default function Landing() {
    const navigate = useNavigate();
    const [email, setEmail] = useState('');
    const [activeFeature, setActiveFeature] = useState(0);
    const isAuthenticated = authUtils.isAuthenticated();

    const handleGetStarted = () => {
        if (isAuthenticated) {
            navigate('/dashboard');
        } else {
            navigate('/login');
        }
    };

    const handleSignIn = () => {
        if (isAuthenticated) {
            navigate('/dashboard');
        } else {
            navigate('/login');
        }
    };

    useEffect(() => {
        const interval = setInterval(() => {
            setActiveFeature((prev) => (prev + 1) % features.length);
        }, 3000);
        return () => clearInterval(interval);
    }, []);

    const features = [
        {
            icon: <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><circle cx="11" cy="11" r="8" /><path d="m21 21-4.35-4.35" /></svg>,
            title: 'Search Rankings',
            description: 'Track your brand\'s position across Google, Bing, and other search engines with real-time data.',
            color: '#6366f1'
        },
        {
            icon: <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M12 8V4H8" /><rect x="8" y="8" width="8" height="8" rx="1" /><path d="M16 16v4h4" /><path d="M4 4h4" /><path d="M20 20h-4" /></svg>,
            title: 'AI Citations',
            description: 'Monitor how AI assistants like ChatGPT, Claude, and Gemini mention your brand.',
            color: '#8b5cf6'
        },
        {
            icon: <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" /></svg>,
            title: 'Review Tracking',
            description: 'Aggregate reviews from Google, Yelp, and social platforms to understand sentiment.',
            color: '#ec4899'
        },
        {
            icon: <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M3 3v18h18" /><path d="M18 17V9" /><path d="M13 17V5" /><path d="M8 17v-3" /></svg>,
            title: 'Analytics Dashboard',
            description: 'Visualize all your brand metrics in one beautiful, real-time dashboard.',
            color: '#06b6d4'
        }
    ];

    const stats = [
        { value: '99.9%', label: 'Uptime' },
        { value: '50+', label: 'Data Sources' },
        { value: '10K+', label: 'Brands Tracked' },
        { value: '24/7', label: 'Monitoring' }
    ];

    const testimonials = [
        {
            quote: "SocialBooster transformed how we track our brand. The AI citations feature is a game-changer.",
            author: "Sarah Chen",
            role: "Marketing Director",
            company: "TechFlow Inc"
        },
        {
            quote: "Finally, one dashboard for all our brand analytics. Saves us hours every week.",
            author: "Michael Torres",
            role: "Brand Manager",
            company: "Elevate Studios"
        },
        {
            quote: "The real-time search ranking alerts have helped us stay ahead of competitors.",
            author: "Emily Watson",
            role: "SEO Lead",
            company: "Growth Labs"
        }
    ];

    return (
        <div className="landing-page">
            {/* Animated Background */}
            <div className="animated-bg">
                <div className="gradient-orb orb-1"></div>
                <div className="gradient-orb orb-2"></div>
                <div className="gradient-orb orb-3"></div>
            </div>

            {/* Navigation */}
            <GlassSurface className="landing-nav glass-static" pill={true} blur={16} opacity={0.4} brightness={40}>
                <div className="nav-container">
                    <div className="nav-brand">
                        <span className="nav-logo">
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                <path d="M3 3v18h18" />
                                <path d="M18 17V9" />
                                <path d="M13 17V5" />
                                <path d="M8 17v-3" />
                            </svg>
                        </span>
                        <span className="nav-name">SocialBooster</span>
                    </div>
                    <div className="nav-actions">
                        {isAuthenticated ? (
                            <button className="btn btn-primary" onClick={handleGetStarted}>Go to Dashboard</button>
                        ) : (
                            <>
                                <button className="btn btn-ghost" onClick={handleSignIn}>Sign In</button>
                                <button className="btn btn-primary" onClick={handleGetStarted}>Get Started</button>
                            </>
                        )}
                    </div>
                </div>
            </GlassSurface>

            {/* Hero Section */}
            <section className="hero-section">
                <div className="hero-background">
                    <LightPillar
                        topColor="#6366f1"
                        bottomColor="#ec4899"
                        intensity={1.3}
                        rotationSpeed={0.15}
                        glowAmount={0.008}
                        pillarWidth={5.0}
                        pillarHeight={0.25}
                        noiseIntensity={0.2}
                    />
                </div>

                <div className="hero-content">
                    <div className="hero-text">
                        <div className="hero-badge-wrapper">
                            <span className="hero-badge">
                                <span className="badge-dot"></span>
                                AI-Powered Brand Analytics
                            </span>
                        </div>

                        <h1 className="hero-title">
                            Track Your Brand's
                            <span className="gradient-text"> Digital Presence</span>
                            <span className="title-accent"> Everywhere</span>
                        </h1>

                        <p className="hero-subtitle">
                            Monitor search rankings, AI citations, and reviews across every platform.
                            Real-time insights powered by advanced analytics.
                        </p>

                        <div className="hero-cta">
                            <button className="btn btn-primary btn-xl" onClick={handleGetStarted}>
                                <span>Start Free Trial</span>
                                <span className="btn-arrow">→</span>
                            </button>
                            <button className="btn btn-glass btn-xl">
                                <span className="play-icon">▶</span>
                                Watch Demo
                            </button>
                        </div>

                        <div className="hero-trust">
                            <span className="trust-text">Trusted by innovative teams at</span>
                            <div className="trust-logos">
                                <span className="trust-logo">Stripe</span>
                                <span className="trust-logo">Notion</span>
                                <span className="trust-logo">Linear</span>
                                <span className="trust-logo">Vercel</span>
                            </div>
                        </div>
                    </div>

                    <div className="hero-visual">
                        <GlassSurface className="hero-card" blur={20} opacity={0.06} borderRadius={24}>
                            <div className="dashboard-preview">
                                <div className="preview-header">
                                    <div className="preview-dots">
                                        <span></span><span></span><span></span>
                                    </div>
                                    <span className="preview-title">Dashboard</span>
                                </div>
                                <div className="preview-stats">
                                    {stats.map((stat, idx) => (
                                        <div key={idx} className="preview-stat">
                                            <span className="preview-stat-icon">{stat.icon}</span>
                                            <span className="preview-stat-value">{stat.value}</span>
                                            <span className="preview-stat-label">{stat.label}</span>
                                        </div>
                                    ))}
                                </div>
                                <div className="preview-chart">
                                    <div className="chart-bars">
                                        {[65, 85, 45, 95, 70, 80, 60].map((h, i) => (
                                            <div key={i} className="chart-bar" style={{ height: `${h}%`, animationDelay: `${i * 0.1}s` }}></div>
                                        ))}
                                    </div>
                                </div>
                            </div>
                        </GlassSurface>
                    </div>
                </div>
            </section>

            {/* Features Section */}
            <section className="features-section">
                <div className="container">
                    <div className="section-header">
                        <span className="section-badge">Features</span>
                        <h2 className="section-title">
                            Everything You Need to
                            <span className="gradient-text"> Dominate</span>
                        </h2>
                        <p className="section-subtitle">
                            Powerful tools to track, analyze, and improve your brand's digital footprint
                        </p>
                    </div>

                    <div className="features-grid">
                        {features.map((feature, idx) => (
                            <div
                                key={idx}
                                className={`feature-card ${activeFeature === idx ? 'active' : ''}`}
                                onMouseEnter={() => setActiveFeature(idx)}
                            >
                                <div className="feature-glow" style={{ background: `radial-gradient(circle at center, ${feature.color}20 0%, transparent 70%)` }}></div>
                                <div className="feature-icon" style={{ background: `linear-gradient(135deg, ${feature.color} 0%, ${feature.color}80 100%)` }}>
                                    {feature.icon}
                                </div>
                                <h3 className="feature-title">{feature.title}</h3>
                                <p className="feature-description">{feature.description}</p>
                                <div className="feature-link">
                                    Learn more <span>→</span>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </section>

            {/* Stats Section */}
            <section className="stats-section">
                <div className="container">
                    <GlassSurface className="stats-glass" blur={16} opacity={0.05} borderRadius={32}>
                        <div className="stats-content">
                            {stats.map((stat, idx) => (
                                <div key={idx} className="stat-item">
                                    <span className="stat-value">{stat.value}</span>
                                    <span className="stat-label">{stat.label}</span>
                                </div>
                            ))}
                        </div>
                    </GlassSurface>
                </div>
            </section>

            {/* Testimonials Section */}
            <section className="testimonials-section">
                <div className="container">
                    <div className="section-header">
                        <span className="section-badge">Testimonials</span>
                        <h2 className="section-title">
                            Loved by
                            <span className="gradient-text"> Brands Worldwide</span>
                        </h2>
                    </div>

                    <div className="testimonials-grid">
                        {testimonials.map((t, idx) => (
                            <div key={idx} className="testimonial-card">
                                <div className="quote-icon">"</div>
                                <p className="testimonial-quote">{t.quote}</p>
                                <div className="testimonial-author">
                                    <div className="author-avatar">
                                        {t.author.split(' ').map(n => n[0]).join('')}
                                    </div>
                                    <div className="author-info">
                                        <span className="author-name">{t.author}</span>
                                        <span className="author-role">{t.role} at {t.company}</span>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </section>

            {/* CTA Section */}
            <section className="cta-section">
                <div className="container">
                    <GlassSurface className="cta-glass" blur={20} opacity={0.08} borderRadius={32}>
                        <div className="cta-content">
                            <h2 className="cta-title">Ready to Boost Your Brand?</h2>
                            <p className="cta-subtitle">
                                Join thousands of brands already using SocialBooster to dominate their digital presence.
                            </p>
                            <div className="cta-form">
                                <input
                                    type="email"
                                    placeholder="Enter your email"
                                    value={email}
                                    onChange={(e) => setEmail(e.target.value)}
                                    className="cta-input"
                                />
                                <button className="btn btn-primary btn-lg" onClick={handleGetStarted}>
                                    Start Free Trial
                                </button>
                            </div>
                            <p className="cta-note">No credit card required • 14-day free trial</p>
                        </div>
                    </GlassSurface>
                </div>
            </section>

            {/* Footer */}
            <footer className="landing-footer">
                <div className="container">
                    <div className="footer-content">
                        <div className="footer-brand">
                            <span className="footer-logo">
                                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                    <path d="M3 3v18h18" />
                                    <path d="M18 17V9" />
                                    <path d="M13 17V5" />
                                    <path d="M8 17v-3" />
                                </svg>
                            </span>
                            <span className="footer-name">SocialBooster</span>
                        </div>
                        <div className="footer-links">
                            <a href="#features">Features</a>
                            <a href="#pricing">Pricing</a>
                            <a href="#docs">Documentation</a>
                            <a href="#support">Support</a>
                        </div>
                        <p className="footer-copy">© 2024 SocialBooster. All rights reserved.</p>
                    </div>
                </div>
            </footer>
        </div>
    );
}
