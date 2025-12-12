import { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, NavLink } from 'react-router-dom';
import Dashboard from './components/Dashboard';
import BrandList from './components/BrandList';
import Rankings from './components/Rankings';
import Citations from './components/Citations';
import Reviews from './components/Reviews';

function App() {
    return (
        <Router>
            <div className="app-container">
                <Sidebar />
                <main className="main-content">
                    <Routes>
                        <Route path="/" element={<Dashboard />} />
                        <Route path="/brands" element={<BrandList />} />
                        <Route path="/rankings" element={<Rankings />} />
                        <Route path="/citations" element={<Citations />} />
                        <Route path="/reviews" element={<Reviews />} />
                    </Routes>
                </main>
            </div>
        </Router>
    );
}

function Sidebar() {
    return (
        <aside className="sidebar">
            <div className="logo">
                <div className="logo-icon">📊</div>
                <span className="logo-text">SocialBooster</span>
            </div>
            <nav className="nav-menu">
                <NavLink to="/" className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
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
        </aside>
    );
}

export default App;
