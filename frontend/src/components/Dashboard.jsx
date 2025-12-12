import { useState, useEffect } from 'react';
import { Line, Pie, Bar } from 'react-chartjs-2';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    BarElement,
    ArcElement,
    Title,
    Tooltip,
    Legend,
    Filler,
} from 'chart.js';
import { dashboardAPI, brandsAPI } from '../services/api';

// Register Chart.js components
ChartJS.register(
    CategoryScale, LinearScale, PointElement, LineElement, BarElement,
    ArcElement, Title, Tooltip, Legend, Filler
);

function Dashboard() {
    const [overview, setOverview] = useState(null);
    const [loading, setLoading] = useState(true);
    const [dateRange, setDateRange] = useState({ start: '', end: '' });

    useEffect(() => {
        fetchDashboardData();
    }, []);

    const fetchDashboardData = async () => {
        try {
            setLoading(true);
            const response = await dashboardAPI.getOverview(dateRange);
            setOverview(response.data);
        } catch (error) {
            console.error('Error fetching dashboard data:', error);
        } finally {
            setLoading(false);
        }
    };

    if (loading) {
        return (
            <div className="loading">
                <div className="spinner"></div>
            </div>
        );
    }

    const stats = overview?.overview || {};
    const charts = overview?.charts || {};

    return (
        <div className="dashboard">
            <div className="page-header">
                <div>
                    <h1 className="page-title">Dashboard</h1>
                    <p className="page-subtitle">Track your brand visibility across search and AI platforms</p>
                </div>
                <div className="date-filter">
                    <span>📅</span>
                    <input
                        type="date"
                        value={dateRange.start}
                        onChange={(e) => setDateRange({ ...dateRange, start: e.target.value })}
                    />
                    <span>to</span>
                    <input
                        type="date"
                        value={dateRange.end}
                        onChange={(e) => setDateRange({ ...dateRange, end: e.target.value })}
                    />
                    <button className="btn btn-primary" onClick={fetchDashboardData}>
                        Apply
                    </button>
                </div>
            </div>

            {/* Stats Cards */}
            <div className="stats-grid">
                <div className="stat-card">
                    <div className="stat-icon">🏢</div>
                    <div className="stat-value">{stats.total_brands || 0}</div>
                    <div className="stat-label">Brands Tracked</div>
                </div>
                <div className="stat-card success">
                    <div className="stat-icon" style={{ background: 'rgba(16, 185, 129, 0.15)' }}>🔍</div>
                    <div className="stat-value">{stats.average_search_position || 0}</div>
                    <div className="stat-label">Avg Search Position</div>
                    <div className="stat-change positive">↑ Improving</div>
                </div>
                <div className="stat-card">
                    <div className="stat-icon" style={{ background: 'rgba(139, 92, 246, 0.15)' }}>🤖</div>
                    <div className="stat-value">{stats.ai_citation_rate || 0}%</div>
                    <div className="stat-label">AI Citation Rate</div>
                    <div className="stat-change positive">↑ Growing</div>
                </div>
                <div className="stat-card warning">
                    <div className="stat-icon" style={{ background: 'rgba(245, 158, 11, 0.15)' }}>⭐</div>
                    <div className="stat-value">{stats.average_rating || 0}</div>
                    <div className="stat-label">Avg Rating</div>
                    <div className="stat-change positive">{stats.total_reviews || 0} reviews</div>
                </div>
            </div>

            {/* Charts */}
            <div className="charts-grid">
                <div className="chart-container">
                    <h3 className="chart-title">📈 Search Ranking Trends</h3>
                    <RankingTrendsChart data={charts.ranking_summary || []} />
                </div>
                <div className="chart-container">
                    <h3 className="chart-title">🤖 AI Citation Breakdown</h3>
                    <CitationPieChart data={charts.citation_breakdown || []} />
                </div>
                <div className="chart-container">
                    <h3 className="chart-title">📊 Brand Visibility Comparison</h3>
                    <BrandComparisonChart data={charts.brand_comparison || []} />
                </div>
                <div className="chart-container">
                    <h3 className="chart-title">⭐ Review Score Breakdown</h3>
                    <ReviewScoresChart data={charts.brand_comparison || []} />
                </div>
            </div>
        </div>
    );
}

// Ranking Trends Line Chart
function RankingTrendsChart({ data }) {
    if (!data || data.length === 0) {
        return <div className="empty-state"><div className="empty-icon">📈</div><p>No ranking data available</p></div>;
    }

    const colors = ['#6366f1', '#8b5cf6', '#06b6d4', '#10b981', '#f59e0b'];

    const chartData = {
        labels: data[0]?.data?.map(d => d.date.slice(5)) || [],
        datasets: data.map((brand, idx) => ({
            label: brand.brand_name,
            data: brand.data?.map(d => d.position) || [],
            borderColor: colors[idx % colors.length],
            backgroundColor: `${colors[idx % colors.length]}20`,
            fill: true,
            tension: 0.4,
        })),
    };

    const options = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'bottom',
                labels: { color: '#94a3b8', padding: 15 }
            },
        },
        scales: {
            y: {
                reverse: true,
                title: { display: true, text: 'Position', color: '#64748b' },
                grid: { color: 'rgba(99, 102, 241, 0.1)' },
                ticks: { color: '#94a3b8' }
            },
            x: {
                grid: { color: 'rgba(99, 102, 241, 0.1)' },
                ticks: { color: '#94a3b8' }
            },
        },
    };

    return <div style={{ height: '280px' }}><Line data={chartData} options={options} /></div>;
}

// Citation Pie Chart
function CitationPieChart({ data }) {
    if (!data || data.length === 0) {
        return <div className="empty-state"><div className="empty-icon">🤖</div><p>No citation data available</p></div>;
    }

    const chartData = {
        labels: data.map(d => d.name),
        datasets: [{
            data: data.map(d => d.value),
            backgroundColor: ['#6366f1', '#8b5cf6', '#06b6d4', '#10b981', '#f59e0b', '#ef4444'],
            borderColor: '#16213e',
            borderWidth: 2,
        }],
    };

    const options = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'right',
                labels: { color: '#94a3b8', padding: 15 }
            },
        },
    };

    return <div style={{ height: '280px' }}><Pie data={chartData} options={options} /></div>;
}

// Brand Comparison Bar Chart
function BrandComparisonChart({ data }) {
    if (!data || data.length === 0) {
        return <div className="empty-state"><div className="empty-icon">📊</div><p>No comparison data available</p></div>;
    }

    const chartData = {
        labels: data.map(d => d.brand_name),
        datasets: [
            {
                label: 'Visibility Score',
                data: data.map(d => d.visibility_score),
                backgroundColor: '#6366f1',
                borderRadius: 8,
            },
            {
                label: 'Search Score',
                data: data.map(d => d.search_score),
                backgroundColor: '#06b6d4',
                borderRadius: 8,
            },
            {
                label: 'AI Score',
                data: data.map(d => d.ai_score),
                backgroundColor: '#8b5cf6',
                borderRadius: 8,
            },
        ],
    };

    const options = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'bottom',
                labels: { color: '#94a3b8', padding: 15 }
            },
        },
        scales: {
            y: {
                grid: { color: 'rgba(99, 102, 241, 0.1)' },
                ticks: { color: '#94a3b8' }
            },
            x: {
                grid: { display: false },
                ticks: { color: '#94a3b8' }
            },
        },
    };

    return <div style={{ height: '280px' }}><Bar data={chartData} options={options} /></div>;
}

// Review Scores Chart
function ReviewScoresChart({ data }) {
    if (!data || data.length === 0) {
        return <div className="empty-state"><div className="empty-icon">⭐</div><p>No review data available</p></div>;
    }

    const chartData = {
        labels: data.map(d => d.brand_name),
        datasets: [{
            label: 'Review Score (0-100)',
            data: data.map(d => d.review_score),
            backgroundColor: '#f59e0b',
            borderRadius: 8,
        }],
    };

    const options = {
        responsive: true,
        maintainAspectRatio: false,
        indexAxis: 'y',
        plugins: {
            legend: { display: false },
        },
        scales: {
            x: {
                max: 100,
                grid: { color: 'rgba(99, 102, 241, 0.1)' },
                ticks: { color: '#94a3b8' }
            },
            y: {
                grid: { display: false },
                ticks: { color: '#94a3b8' }
            },
        },
    };

    return <div style={{ height: '280px' }}><Bar data={chartData} options={options} /></div>;
}

export default Dashboard;
