import { useState, useEffect } from 'react';
import { Bar } from 'react-chartjs-2';
import { reviewsAPI } from '../services/api';

function Reviews() {
    const [reviews, setReviews] = useState([]);
    const [summary, setSummary] = useState(null);
    const [loading, setLoading] = useState(true);
    const [filter, setFilter] = useState({ platform: '' });

    useEffect(() => {
        fetchData();
    }, [filter]);

    const fetchData = async () => {
        try {
            setLoading(true);
            const [reviewsRes, summaryRes] = await Promise.all([
                reviewsAPI.getAll(filter),
                reviewsAPI.getSummary(),
            ]);
            setReviews(reviewsRes.data.results || reviewsRes.data);
            setSummary(summaryRes.data);
        } catch (error) {
            console.error('Error fetching reviews:', error);
        } finally {
            setLoading(false);
        }
    };

    if (loading) {
        return <div className="loading"><div className="spinner"></div></div>;
    }

    return (
        <div>
            <div className="page-header">
                <div>
                    <h1 className="page-title">Reviews</h1>
                    <p className="page-subtitle">Monitor brand ratings across review platforms</p>
                </div>
                <select
                    className="form-select"
                    value={filter.platform}
                    onChange={(e) => setFilter({ ...filter, platform: e.target.value })}
                    style={{ width: '180px' }}
                >
                    <option value="">All Platforms</option>
                    <option value="google">Google Reviews</option>
                    <option value="yelp">Yelp</option>
                    <option value="trustpilot">Trustpilot</option>
                    <option value="g2">G2</option>
                </select>
            </div>

            {/* Summary Cards */}
            <div className="stats-grid">
                <div className="stat-card">
                    <div className="stat-icon">⭐</div>
                    <div className="stat-value">{summary?.average_rating || 0}</div>
                    <div className="stat-label">Average Rating</div>
                </div>
                <div className="stat-card success">
                    <div className="stat-icon" style={{ background: 'rgba(16, 185, 129, 0.15)' }}>📝</div>
                    <div className="stat-value">{summary?.total_reviews?.toLocaleString() || 0}</div>
                    <div className="stat-label">Total Reviews</div>
                </div>
                <div className="stat-card">
                    <div className="stat-icon" style={{ background: 'rgba(139, 92, 246, 0.15)' }}>🏆</div>
                    <div className="stat-value">{summary?.by_platform?.length || 0}</div>
                    <div className="stat-label">Platforms Tracked</div>
                </div>
            </div>

            {/* Charts */}
            <div className="charts-grid">
                <div className="chart-container">
                    <h3 className="chart-title">⭐ Average Rating by Platform</h3>
                    <PlatformRatingChart data={summary?.by_platform || []} />
                </div>
                <div className="chart-container">
                    <h3 className="chart-title">📊 Review Count by Platform</h3>
                    <ReviewCountChart data={summary?.by_platform || []} />
                </div>
            </div>

            {/* Reviews Table */}
            <div className="card">
                <div className="card-header">
                    <h3 className="card-title">Recent Review Data</h3>
                </div>
                <div className="table-container">
                    <table>
                        <thead>
                            <tr>
                                <th>Brand</th>
                                <th>Platform</th>
                                <th>Rating</th>
                                <th>Reviews</th>
                                <th>Date</th>
                            </tr>
                        </thead>
                        <tbody>
                            {reviews.slice(0, 20).map(review => (
                                <tr key={review.id}>
                                    <td><strong>{review.brand_name}</strong></td>
                                    <td><span className="badge badge-primary">{review.platform_display}</span></td>
                                    <td>
                                        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                                            <StarRating rating={parseFloat(review.rating)} />
                                            <span>{review.rating}</span>
                                        </div>
                                    </td>
                                    <td>{review.review_count?.toLocaleString()}</td>
                                    <td>{review.date}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
}

function StarRating({ rating }) {
    const fullStars = Math.floor(rating);
    const hasHalf = rating % 1 >= 0.5;
    return (
        <span style={{ color: '#f59e0b' }}>
            {'★'.repeat(fullStars)}
            {hasHalf && '☆'}
            {'☆'.repeat(5 - fullStars - (hasHalf ? 1 : 0))}
        </span>
    );
}

function PlatformRatingChart({ data }) {
    if (!data || data.length === 0) {
        return <div className="empty-state"><div className="empty-icon">⭐</div><p>No data</p></div>;
    }

    const chartData = {
        labels: data.map(d => d.platform_display),
        datasets: [{
            label: 'Average Rating',
            data: data.map(d => d.avg_rating),
            backgroundColor: '#f59e0b',
            borderRadius: 8,
        }],
    };

    const options = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: {
            y: { max: 5, grid: { color: 'rgba(99, 102, 241, 0.1)' }, ticks: { color: '#94a3b8' } },
            x: { grid: { display: false }, ticks: { color: '#94a3b8' } },
        },
    };

    return <div style={{ height: '280px' }}><Bar data={chartData} options={options} /></div>;
}

function ReviewCountChart({ data }) {
    if (!data || data.length === 0) {
        return <div className="empty-state"><div className="empty-icon">📊</div><p>No data</p></div>;
    }

    const chartData = {
        labels: data.map(d => d.platform_display),
        datasets: [{
            label: 'Total Reviews',
            data: data.map(d => d.total_reviews),
            backgroundColor: '#10b981',
            borderRadius: 8,
        }],
    };

    const options = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: {
            y: { grid: { color: 'rgba(99, 102, 241, 0.1)' }, ticks: { color: '#94a3b8' } },
            x: { grid: { display: false }, ticks: { color: '#94a3b8' } },
        },
    };

    return <div style={{ height: '280px' }}><Bar data={chartData} options={options} /></div>;
}

export default Reviews;
