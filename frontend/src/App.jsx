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
                <div className="logo-icon">📊</div>
                <span className="logo-text">SocialBooster</span>
            </div>
            <nav className="nav-menu">
                <NavLink to="/dashboard" className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
                    <span className="nav-icon">🏠</span>
                    <span className="nav-text">Dashboard</span>
                </NavLink>
                <NavLink to="/brands" className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
                    <span className="nav-icon">🏢</span>
                    <span className="nav-text">Brands</span>
                </NavLink>
                <NavLink to="/rankings" className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
                    <span className="nav-icon">🔍</span>
                    <span className="nav-text">Search Rankings</span>
                </NavLink>
                <NavLink to="/citations" className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
                    <span className="nav-icon">🤖</span>
                    <span className="nav-text">AI Citations</span>
                </NavLink>
                <NavLink to="/reviews" className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
                    <span className="nav-icon">⭐</span>
                    <span className="nav-text">Reviews</span>
                </NavLink>
            </nav>

            {user && (
                <div className="sidebar-footer">
                    <div className="user-info">
                        <span className="user-avatar">👤</span>
                        <span className="user-name">{user.username}</span>
                    </div>
                    <button onClick={onLogout} className="logout-btn">
                        Logout
                    </button>
                </div>
            )}
        </aside>
    );
}

export default App;
