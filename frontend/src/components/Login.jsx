import { useState } from 'react';
import { authAPI, authUtils } from '../services/api';
import './Login.css';

export default function Login({ onLoginSuccess }) {
    const [isRegister, setIsRegister] = useState(false);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [formData, setFormData] = useState({
        username: '',
        email: '',
        password: '',
        password2: '',
    });

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
        setError('');
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');

        try {
            if (isRegister) {
                await authAPI.register(formData);
                // Auto-login after register
                await authAPI.login(formData.username, formData.password);
            } else {
                await authAPI.login(formData.username, formData.password);
            }
            onLoginSuccess();
        } catch (err) {
            // Handle validation errors from backend
            const errorData = err.response?.data;
            let message = 'Authentication failed';

            if (errorData) {
                // Check for field-specific errors
                if (typeof errorData === 'object') {
                    const errorMessages = [];
                    for (const [field, errors] of Object.entries(errorData)) {
                        if (Array.isArray(errors)) {
                            errorMessages.push(...errors);
                        } else if (typeof errors === 'string') {
                            errorMessages.push(errors);
                        }
                    }
                    if (errorMessages.length > 0) {
                        message = errorMessages.join(' ');
                    }
                } else if (typeof errorData === 'string') {
                    message = errorData;
                }
            }

            setError(message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="login-container">
            {/* Animated Background */}
            <div className="login-bg">
                <div className="login-orb orb-1"></div>
                <div className="login-orb orb-2"></div>
            </div>
            <div className="login-card">
                <div className="login-header">
                    <div className="login-logo">
                        <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                            <path d="M3 3v18h18" />
                            <path d="M18 17V9" />
                            <path d="M13 17V5" />
                            <path d="M8 17v-3" />
                        </svg>
                    </div>
                    <h1>SocialBooster</h1>
                    <p>{isRegister ? 'Create your account' : 'Sign in to your account'}</p>
                </div>

                {error && <div className="login-error">{error}</div>}

                <form onSubmit={handleSubmit} className="login-form">
                    <div className="form-group">
                        <label className="form-label">Username</label>
                        <input
                            type="text"
                            name="username"
                            className="form-input"
                            value={formData.username}
                            onChange={handleChange}
                            required
                            autoFocus
                        />
                    </div>

                    {isRegister && (
                        <div className="form-group">
                            <label className="form-label">Email</label>
                            <input
                                type="email"
                                name="email"
                                className="form-input"
                                value={formData.email}
                                onChange={handleChange}
                                required
                            />
                        </div>
                    )}

                    <div className="form-group">
                        <label className="form-label">Password</label>
                        <input
                            type="password"
                            name="password"
                            className="form-input"
                            value={formData.password}
                            onChange={handleChange}
                            required
                        />
                    </div>

                    {isRegister && (
                        <div className="form-group">
                            <label className="form-label">Confirm Password</label>
                            <input
                                type="password"
                                name="password2"
                                className="form-input"
                                value={formData.password2}
                                onChange={handleChange}
                                required
                            />
                        </div>
                    )}

                    <button type="submit" className="btn btn-primary login-btn" disabled={loading}>
                        {loading ? 'Please wait...' : (isRegister ? 'Create Account' : 'Sign In')}
                    </button>
                </form>

                <div className="login-toggle">
                    {isRegister ? (
                        <p>Already have an account? <button onClick={() => setIsRegister(false)}>Sign In</button></p>
                    ) : (
                        <p>Don't have an account? <button onClick={() => setIsRegister(true)}>Create one</button></p>
                    )}
                </div>
            </div>
        </div>
    );
}
