import { useState, useEffect } from 'react';
import { Line } from 'react-chartjs-2';
import { rankingsAPI, brandsAPI } from '../services/api';
import GlassSurface from './effects/GlassSurface';

function Rankings() {
    const [rankings, setRankings] = useState([]);
    const [brands, setBrands] = useState([]);
    const [selectedBrand, setSelectedBrand] = useState('');
    const [trends, setTrends] = useState(null);
    const [loading, setLoading] = useState(true);
    const [summary, setSummary] = useState(null);

    useEffect(() => {
        fetchInitialData();
    }, []);

    useEffect(() => {
        if (selectedBrand) {
            fetchTrends(selectedBrand);
        }
    }, [selectedBrand]);

    const fetchInitialData = async () => {
        try {
            setLoading(true);
            const [rankingsRes, brandsRes, summaryRes] = await Promise.all([
                rankingsAPI.getAll(),
                brandsAPI.getAll(),
                rankingsAPI.getSummary(),
            ]);
            setRankings(rankingsRes.data.results || rankingsRes.data);
            setBrands(brandsRes.data.results || brandsRes.data);
            setSummary(summaryRes.data);

            // Auto-select first brand
            const brandList = brandsRes.data.results || brandsRes.data;
            if (brandList.length > 0) {
                setSelectedBrand(brandList[0].id);
            }
        } catch (error) {
            console.error('Error fetching data:', error);
        } finally {
            setLoading(false);
        }
    };

    const fetchTrends = async (brandId) => {
        try {
            const response = await rankingsAPI.getTrends(brandId);
            setTrends(response.data);
        } catch (error) {
            console.error('Error fetching trends:', error);
        }
    };

    if (loading) {
        return <div className="loading"><div className="spinner"></div></div>;
    }

    return (
        <div>
            <div className="page-header">
                <div>
                    <h1 className="page-title">Search Rankings</h1>
                    <p className="page-subtitle">Track Google search positions for your brands</p>
                </div>
                <div style={{ display: 'flex', gap: '12px', alignItems: 'center' }}>
                    <select
                        className="form-select"
                        value={selectedBrand}
                        onChange={(e) => setSelectedBrand(e.target.value)}
                        style={{ width: '200px' }}
                    >
                        {brands.map(brand => (
                            <option key={brand.id} value={brand.id}>{brand.name}</option>
                        ))}
                    </select>
                </div>
            </div>

            {/* Summary Cards */}
            <div className="stats-grid">
                <div className="stat-card">
                    <div className="stat-label">Total Rankings Tracked</div>
                    <div className="stat-value">{summary?.total_rankings || 0}</div>
                </div>
                <div className="stat-card success">
                    <div className="stat-label">Average Position</div>
                    <div className="stat-value">{summary?.average_position || 0}</div>
                </div>
                <div className="stat-card">
                    <div className="stat-label">Keywords Tracked</div>
                    <div className="stat-value">{summary?.unique_keywords || 0}</div>
                </div>
            </div>

            {/* Trends Chart */}
            <div className="charts-grid">
                <div className="chart-container" style={{ gridColumn: 'span 2' }}>
                    <h3 className="chart-title">Position Trends Over Time</h3>
                    {trends && <TrendsChart trends={trends.trends} />}
                </div>
            </div>

            {/* Rankings Table */}
            <div className="card">
                <div className="card-header">
                    <h3 className="card-title">Recent Rankings</h3>
                </div>
                <div className="table-container">
                    <table>
                        <thead>
                            <tr>
                                <th>Brand</th>
                                <th>Keyword</th>
                                <th>Position</th>
                                <th>Date</th>
                            </tr>
                        </thead>
                        <tbody>
                            {rankings.slice(0, 20).map(ranking => (
                                <tr key={ranking.id}>
                                    <td><strong>{ranking.brand_name}</strong></td>
                                    <td>{ranking.keyword}</td>
                                    <td>
                                        <span className={`badge ${ranking.position <= 10 ? 'badge-success' : ranking.position <= 30 ? 'badge-warning' : 'badge-danger'}`}>
                                            #{ranking.position}
                                        </span>
                                    </td>
                                    <td>{ranking.date}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
}

function TrendsChart({ trends }) {
    if (!trends || Object.keys(trends).length === 0) {
        return <div className="empty-state"><p>No trend data available</p></div>;
    }

    const colors = ['#6366f1', '#8b5cf6', '#06b6d4', '#10b981', '#f59e0b'];
    const keywords = Object.keys(trends);

    const chartData = {
        labels: trends[keywords[0]]?.map(d => d.date.slice(5)) || [],
        datasets: keywords.map((keyword, idx) => ({
            label: keyword,
            data: trends[keyword]?.map(d => d.position) || [],
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
            legend: { position: 'bottom', labels: { color: '#94a3b8' } },
        },
        scales: {
            y: {
                reverse: true,
                title: { display: true, text: 'Position', color: '#64748b' },
                grid: { color: 'rgba(99, 102, 241, 0.1)' },
                ticks: { color: '#94a3b8' }
            },
            x: { grid: { color: 'rgba(99, 102, 241, 0.1)' }, ticks: { color: '#94a3b8' } },
        },
    };

    return <div style={{ height: '300px' }}><Line data={chartData} options={options} /></div>;
}

export default Rankings;
