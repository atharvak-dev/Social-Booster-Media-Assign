import { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, NavLink, useLocation } from 'react-router-dom';
import { authUtils, authAPI } from './services/api';
import Dashboard from './components/Dashboard';
import BrandList from './components/BrandList';
import Rankings from './components/Rankings';
import Citations from './components/Citations';
import Reviews from './components/Reviews';
import Login from './components/Login';
import Landing from './components/Landing';

function App() {
    return (
        <Router>
            <AppContent />
        </Router>
    );
}

function AppContent() {
    const [isAuthenticated, setIsAuthenticated] = useState(authUtils.isAuthenticated());
    const [user, setUser] = useState(null);
    const location = useLocation();

    useEffect(() => {
        if (isAuthenticated) {
            authAPI.getProfile()
                .then(res => setUser(res.data))
                .catch(() => {
                    authUtils.clearTokens();
                    setIsAuthenticated(false);
                });
        }
    }, [isAuthenticated]);

    const handleLoginSuccess = () => {
        setIsAuthenticated(true);
    };

    const handleLogout = () => {
        authAPI.logout();
        setIsAuthenticated(false);
        setUser(null);
    };

    // Show landing page for unauthenticated users on home route
    if (!isAuthenticated && location.pathname === '/') {
        return <Landing />;
    }

    // Show login page for unauthenticated users on login route
    if (!isAuthenticated && location.pathname === '/login') {
        return <Login onLoginSuccess={handleLoginSuccess} />;
    }

    // Redirect to landing for other routes when not authenticated
    if (!isAuthenticated) {
        return <Landing />;
    }

    return (
        <div className="app-container">
            <Sidebar user={user} onLogout={handleLogout} />
            <main className="main-content">
                <Routes>
                    <Route path="/" element={<Dashboard />} />
                    <Route path="/dashboard" element={<Dashboard />} />
                    <Route path="/brands" element={<BrandList />} />
                    <Route path="/rankings" element={<Rankings />} />
                    <Route path="/citations" element={<Citations />} />
                    <Route path="/reviews" element={<Reviews />} />
                </Routes>
            </main>
        </div>
    );
}

function Sidebar({ user, onLogout }) {
    return (
        <aside className="sidebar">
            <div className="logo">
                <div className="logo-icon">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                        <path d="M3 3v18h18" />
                        <path d="M18 17V9" />
                        <path d="M13 17V5" />
                        <path d="M8 17v-3" />
                    </svg>
                </div>
                <span className="logo-text">SocialBooster</span>
            </div>
            <nav className="nav-menu">
                <NavLink to="/dashboard" className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
                    <span className="nav-icon">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                            <rect x="3" y="3" width="7" height="7" />
                            <rect x="14" y="3" width="7" height="7" />
                            <rect x="14" y="14" width="7" height="7" />
                            <rect x="3" y="14" width="7" height="7" />
                        </svg>
                    </span>
                    <span className="nav-text">Dashboard</span>
                </NavLink>
                <NavLink to="/brands" className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
                    <span className="nav-icon">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                            <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z" />
                            <polyline points="9 22 9 12 15 12 15 22" />
                        </svg>
                    </span>
                    <span className="nav-text">Brands</span>
                </NavLink>
                <NavLink to="/rankings" className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
                    <span className="nav-icon">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                            <circle cx="11" cy="11" r="8" />
                            <path d="m21 21-4.35-4.35" />
                        </svg>
                    </span>
                    <span className="nav-text">Search Rankings</span>
                </NavLink>
                <NavLink to="/citations" className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
                    <span className="nav-icon">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                            <path d="M12 8V4H8" />
                            <rect x="8" y="8" width="8" height="8" rx="1" />
                            <path d="M16 16v4h4" />
                            <path d="M4 4h4" />
                            <path d="M20 20h-4" />
                        </svg>
                    </span>
                    <span className="nav-text">AI Citations</span>
                </NavLink>
                <NavLink to="/reviews" className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
                    <span className="nav-icon">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                            <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" />
                        </svg>
                    </span>
                    <span className="nav-text">Reviews</span>
                </NavLink>
            </nav>

            {user && (
                <div className="sidebar-footer">
                    <div className="user-info">
                        <span className="user-avatar">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
                                <circle cx="12" cy="7" r="4" />
                            </svg>
                        </span>
                        <span className="user-name">{user.username}</span>
                    </div>
                    <button onClick={onLogout} className="logout-btn">
                        Sign Out
                    </button>
                </div>
            )}
        </aside>
    );
}

export default App;
