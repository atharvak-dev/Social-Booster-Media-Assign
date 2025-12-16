import { useState, useEffect } from 'react';
import { brandsAPI } from '../services/api';
import GlassSurface from './effects/GlassSurface';

function BrandList() {
    const [brands, setBrands] = useState([]);
    const [loading, setLoading] = useState(true);
    const [showModal, setShowModal] = useState(false);
    const [editingBrand, setEditingBrand] = useState(null);
    const [formData, setFormData] = useState({ name: '', category: 'software', website: '' });

    useEffect(() => {
        fetchBrands();
    }, []);

    const fetchBrands = async () => {
        try {
            setLoading(true);
            const response = await brandsAPI.getAll();
            setBrands(response.data.results || response.data);
        } catch (error) {
            console.error('Error fetching brands:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            if (editingBrand) {
                await brandsAPI.update(editingBrand.id, formData);
            } else {
                const response = await brandsAPI.create(formData);
                // Show notification about data fetching
                if (response.data?.auto_fetch_status) {
                    alert(`Brand "${formData.name}" created successfully!\n\n📊 Real data is being fetched from the internet in the background.\n\nPlease wait 10-15 seconds, then refresh the Dashboard to see the data.`);
                }
            }
            fetchBrands();
            closeModal();
        } catch (error) {
            console.error('Error saving brand:', error);
        }
    };

    const handleDelete = async (id) => {
        if (window.confirm('Are you sure you want to delete this brand?')) {
            try {
                await brandsAPI.delete(id);
                fetchBrands();
            } catch (error) {
                console.error('Error deleting brand:', error);
            }
        }
    };

    const openEditModal = (brand) => {
        setEditingBrand(brand);
        setFormData({ name: brand.name, category: brand.category, website: brand.website });
        setShowModal(true);
    };

    const openCreateModal = () => {
        setEditingBrand(null);
        setFormData({ name: '', category: 'software', website: '' });
        setShowModal(true);
    };

    const closeModal = () => {
        setShowModal(false);
        setEditingBrand(null);
        setFormData({ name: '', category: 'software', website: '' });
    };

    const categoryLabels = {
        software: 'Software & Technology',
        ecommerce: 'E-Commerce & Retail',
        finance: 'Finance & Accounting',
        health: 'Health & Wellness',
        food: 'Food & Beverage',
        services: 'Professional Services',
        other: 'Other',
    };

    if (loading) {
        return <div className="loading"><div className="spinner"></div></div>;
    }

    return (
        <div>
            <div className="page-header">
                <div>
                    <h1 className="page-title">Brands</h1>
                    <p className="page-subtitle">Manage your tracked brands</p>
                </div>
                <button className="btn btn-primary" onClick={openCreateModal}>
                    + Add Brand
                </button>
            </div>

            <div className="card">
                <div className="table-container">
                    <table>
                        <thead>
                            <tr>
                                <th>Brand Name</th>
                                <th>Category</th>
                                <th>Website</th>
                                <th>Created</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {brands.length === 0 ? (
                                <tr>
                                    <td colSpan="5" style={{ textAlign: 'center', padding: '40px' }}>
                                        <div className="empty-state">
                                            <div className="empty-icon">🏢</div>
                                            <p>No brands yet. Add your first brand!</p>
                                        </div>
                                    </td>
                                </tr>
                            ) : (
                                brands.map(brand => (
                                    <tr key={brand.id}>
                                        <td><strong>{brand.name}</strong></td>
                                        <td><span className="badge badge-primary">{categoryLabels[brand.category] || brand.category}</span></td>
                                        <td>
                                            {brand.website && (
                                                <a href={brand.website} target="_blank" rel="noopener noreferrer" style={{ color: 'var(--accent-tertiary)' }}>
                                                    {brand.website.replace(/^https?:\/\//, '').slice(0, 30)}...
                                                </a>
                                            )}
                                        </td>
                                        <td>{new Date(brand.created_at).toLocaleDateString()}</td>
                                        <td>
                                            <button className="btn btn-secondary" onClick={() => openEditModal(brand)} style={{ marginRight: '8px' }}>
                                                Edit
                                            </button>
                                            <button className="btn btn-danger" onClick={() => handleDelete(brand.id)}>
                                                Delete
                                            </button>
                                        </td>
                                    </tr>
                                ))
                            )}
                        </tbody>
                    </table>
                </div>
            </div>

            {/* Modal */}
            {showModal && (
                <div className="modal-overlay" onClick={closeModal}>
                    <div className="modal" onClick={e => e.stopPropagation()}>
                        <div className="modal-header">
                            <h2 className="modal-title">{editingBrand ? 'Edit Brand' : 'Add New Brand'}</h2>
                            <button className="modal-close" onClick={closeModal}>&times;</button>
                        </div>
                        <form onSubmit={handleSubmit}>
                            <div className="form-group">
                                <label className="form-label">Brand Name *</label>
                                <input
                                    type="text"
                                    className="form-input"
                                    value={formData.name}
                                    onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                                    required
                                    placeholder="Enter brand name"
                                />
                            </div>
                            <div className="form-group">
                                <label className="form-label">Category</label>
                                <select
                                    className="form-select"
                                    value={formData.category}
                                    onChange={(e) => setFormData({ ...formData, category: e.target.value })}
                                >
                                    {Object.entries(categoryLabels).map(([value, label]) => (
                                        <option key={value} value={value}>{label}</option>
                                    ))}
                                </select>
                            </div>
                            <div className="form-group">
                                <label className="form-label">Website URL</label>
                                <input
                                    type="url"
                                    className="form-input"
                                    value={formData.website}
                                    onChange={(e) => setFormData({ ...formData, website: e.target.value })}
                                    placeholder="https://example.com"
                                />
                            </div>
                            <div style={{ display: 'flex', gap: '12px', justifyContent: 'flex-end' }}>
                                <button type="button" className="btn btn-secondary" onClick={closeModal}>
                                    Cancel
                                </button>
                                <button type="submit" className="btn btn-primary">
                                    {editingBrand ? 'Update Brand' : 'Create Brand'}
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            )}
        </div>
    );
}

export default BrandList;
