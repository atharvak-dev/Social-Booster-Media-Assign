import { useState, useEffect } from 'react';
import { Pie, Bar } from 'react-chartjs-2';
import { citationsAPI } from '../services/api';

function Citations() {
    const [citations, setCitations] = useState([]);
    const [breakdown, setBreakdown] = useState(null);
    const [summary, setSummary] = useState(null);
    const [loading, setLoading] = useState(true);
    const [filter, setFilter] = useState({ ai_model: '', mentioned: '' });

    useEffect(() => {
        fetchData();
    }, [filter]);

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
                        <option value="google_ai">Google AI</option>
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

function CitationPieChart({ data }) {
    if (!data || data.length === 0) {
        return <div className="empty-state"><div className="empty-icon">🤖</div><p>No data</p></div>;
    }

    const chartData = {
        labels: data.map(d => d.ai_model_display),
        datasets: [{
            data: data.map(d => d.mentioned),
            backgroundColor: ['#6366f1', '#8b5cf6', '#06b6d4', '#10b981', '#f59e0b'],
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
            backgroundColor: '#8b5cf6',
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
