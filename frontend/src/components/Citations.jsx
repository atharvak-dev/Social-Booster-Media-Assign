import { useState, useEffect } from 'react';
import { Pie, Bar, Line } from 'react-chartjs-2';
import { citationsAPI } from '../services/api';
import GlassSurface from './effects/GlassSurface';

function Citations() {
    const [citations, setCitations] = useState([]);
    const [breakdown, setBreakdown] = useState(null);
    const [summary, setSummary] = useState(null);
    const [timeline, setTimeline] = useState(null);
    const [loading, setLoading] = useState(true);
    const [filter, setFilter] = useState({ ai_model: '', mentioned: '' });
    const [timelineDays, setTimelineDays] = useState(14);
    const [timelineGroup, setTimelineGroup] = useState('ai_model');

    useEffect(() => {
        fetchData();
    }, [filter]);

    useEffect(() => {
        fetchTimeline();
    }, [timelineDays, timelineGroup]);

    const fetchData = async () => {
        try {
            setLoading(true);
            const [citationsRes, breakdownRes, summaryRes] = await Promise.all([
                citationsAPI.getAll(filter),
                citationsAPI.getBreakdown(),
                citationsAPI.getSummary(),
            ]);
            setCitations(citationsRes.data.results || citationsRes.data);
            setBreakdown(breakdownRes.data);
            setSummary(summaryRes.data);
        } catch (error) {
            console.error('Error fetching citations:', error);
        } finally {
            setLoading(false);
        }
    };

    const fetchTimeline = async () => {
        try {
            const res = await citationsAPI.getTimeline({ days: timelineDays, group_by: timelineGroup });
            setTimeline(res.data);
        } catch (error) {
            console.error('Error fetching timeline:', error);
        }
    };

    if (loading) {
        return <div className="loading"><div className="spinner"></div></div>;
    }

    return (
        <div>
            <div className="page-header">
                <div>
                    <h1 className="page-title">AI Citations</h1>
                    <p className="page-subtitle">Track brand mentions in AI-generated responses</p>
                </div>
                <div style={{ display: 'flex', gap: '12px' }}>
                    <select
                        className="form-select"
                        value={filter.ai_model}
                        onChange={(e) => setFilter({ ...filter, ai_model: e.target.value })}
                        style={{ width: '150px' }}
                    >
                        <option value="">All AI Models</option>
                        <option value="chatgpt">ChatGPT</option>
                        <option value="gemini">Gemini</option>
                        <option value="perplexity">Perplexity</option>
                        <option value="copilot">Copilot</option>
                        <option value="claude">Claude</option>
                    </select>
                    <select
                        className="form-select"
                        value={filter.mentioned}
                        onChange={(e) => setFilter({ ...filter, mentioned: e.target.value })}
                        style={{ width: '150px' }}
                    >
                        <option value="">All Status</option>
                        <option value="true">Mentioned</option>
                        <option value="false">Not Mentioned</option>
                    </select>
                </div>
            </div>

            {/* Summary Cards */}
            <div className="stats-grid">
                <div className="stat-card">
                    <div className="stat-icon">🤖</div>
                    <div className="stat-value">{summary?.total_citations || 0}</div>
                    <div className="stat-label">Total Checks</div>
                </div>
                <div className="stat-card success">
                    <div className="stat-icon" style={{ background: 'rgba(16, 185, 129, 0.15)' }}>✅</div>
                    <div className="stat-value">{summary?.total_mentioned || 0}</div>
                    <div className="stat-label">Times Mentioned</div>
                </div>
                <div className="stat-card">
                    <div className="stat-icon" style={{ background: 'rgba(139, 92, 246, 0.15)' }}>📈</div>
                    <div className="stat-value">{summary?.citation_rate || 0}%</div>
                    <div className="stat-label">Citation Rate</div>
                </div>
            </div>

            {/* Timeline Chart - Full Width */}
            <div className="card" style={{ marginBottom: '24px' }}>
                <div className="card-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <h3 className="chart-title" style={{ margin: 0 }}>📈 Citation Trends Over Time</h3>
                    <div style={{ display: 'flex', gap: '12px' }}>
                        <select
                            className="form-select"
                            value={timelineGroup}
                            onChange={(e) => setTimelineGroup(e.target.value)}
                            style={{ width: '140px' }}
                        >
                            <option value="ai_model">By AI Model</option>
                            <option value="brand">By Brand</option>
                        </select>
                        <select
                            className="form-select"
                            value={timelineDays}
                            onChange={(e) => setTimelineDays(Number(e.target.value))}
                            style={{ width: '120px' }}
                        >
                            <option value={7}>7 Days</option>
                            <option value={14}>14 Days</option>
                            <option value={30}>30 Days</option>
                        </select>
                    </div>
                </div>
                <div style={{ padding: '20px' }}>
                    <TimelineChart data={timeline} />
                </div>
            </div>

            {/* Charts */}
            <div className="charts-grid">
                <div className="chart-container">
                    <h3 className="chart-title">🤖 Citations by AI Model</h3>
                    <CitationPieChart data={breakdown?.breakdown || []} />
                </div>
                <div className="chart-container">
                    <h3 className="chart-title">📊 Citation Rate by Model</h3>
                    <CitationRateChart data={breakdown?.breakdown || []} />
                </div>
            </div>

            {/* Citations Table */}
            <div className="card">
                <div className="card-header">
                    <h3 className="card-title">Recent AI Citation Checks</h3>
                </div>
                <div className="table-container">
                    <table>
                        <thead>
                            <tr>
                                <th>Brand</th>
                                <th>AI Model</th>
                                <th>Query</th>
                                <th>Status</th>
                                <th>Date</th>
                            </tr>
                        </thead>
                        <tbody>
                            {citations.slice(0, 20).map(citation => (
                                <tr key={citation.id}>
                                    <td><strong>{citation.brand_name}</strong></td>
                                    <td><span className="badge badge-primary">{citation.ai_model_display}</span></td>
                                    <td style={{ maxWidth: '300px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                                        {citation.query}
                                    </td>
                                    <td>
                                        <span className={`badge ${citation.mentioned ? 'badge-success' : 'badge-danger'}`}>
                                            {citation.mentioned ? '✓ Mentioned' : '✗ Not Mentioned'}
                                        </span>
                                    </td>
                                    <td>{citation.date}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
}

function TimelineChart({ data }) {
    if (!data || !data.datasets || data.datasets.length === 0) {
        return <div className="empty-state"><div className="empty-icon">📈</div><p>No timeline data available</p></div>;
    }

    const chartData = {
        labels: data.labels.map(d => {
            const date = new Date(d);
            return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
        }),
        datasets: data.datasets.map(ds => ({
            ...ds,
            fill: false,
            pointRadius: 4,
            pointHoverRadius: 6,
        })),
    };

    const options = {
        responsive: true,
        maintainAspectRatio: false,
        interaction: {
            mode: 'index',
            intersect: false,
        },
        plugins: {
            legend: {
                position: 'top',
                labels: { color: '#94a3b8', usePointStyle: true, padding: 20 }
            },
            tooltip: {
                callbacks: {
                    label: (context) => `${context.dataset.label}: ${context.raw}%`
                }
            }
        },
        scales: {
            x: {
                grid: { color: 'rgba(99, 102, 241, 0.1)' },
                ticks: { color: '#94a3b8' }
            },
            y: {
                min: 0,
                max: 100,
                grid: { color: 'rgba(99, 102, 241, 0.1)' },
                ticks: {
                    color: '#94a3b8',
                    callback: (value) => `${value}%`
                }
            }
        }
    };

    return <div style={{ height: '350px' }}><Line data={chartData} options={options} /></div>;
}

function CitationPieChart({ data }) {
    if (!data || data.length === 0) {
        return <div className="empty-state"><div className="empty-icon">🤖</div><p>No data</p></div>;
    }

    const chartData = {
        labels: data.map(d => d.ai_model_display),
        datasets: [{
            data: data.map(d => d.mentioned),
            backgroundColor: ['#10A37F', '#4285F4', '#8B5CF6', '#00A4EF', '#D97757', '#EA4335'],
            borderColor: '#16213e',
            borderWidth: 2,
        }],
    };

    const options = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { position: 'right', labels: { color: '#94a3b8' } } },
    };

    return <div style={{ height: '280px' }}><Pie data={chartData} options={options} /></div>;
}

function CitationRateChart({ data }) {
    if (!data || data.length === 0) {
        return <div className="empty-state"><div className="empty-icon">📊</div><p>No data</p></div>;
    }

    const chartData = {
        labels: data.map(d => d.ai_model_display),
        datasets: [{
            label: 'Citation Rate %',
            data: data.map(d => d.citation_rate),
            backgroundColor: ['#10A37F', '#4285F4', '#8B5CF6', '#00A4EF', '#D97757', '#EA4335'],
            borderRadius: 8,
        }],
    };

    const options = {
        responsive: true,
        maintainAspectRatio: false,
        indexAxis: 'y',
        plugins: { legend: { display: false } },
        scales: {
            x: { max: 100, grid: { color: 'rgba(99, 102, 241, 0.1)' }, ticks: { color: '#94a3b8' } },
            y: { grid: { display: false }, ticks: { color: '#94a3b8' } },
        },
    };

    return <div style={{ height: '280px' }}><Bar data={chartData} options={options} /></div>;
}

export default Citations;
