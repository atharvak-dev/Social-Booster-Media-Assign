import { Navigate, useLocation } from 'react-router-dom';
import { authUtils } from '../services/api';

export default function RequireAuth({ children }) {
    const isAuthenticated = authUtils.isAuthenticated();
    const location = useLocation();

    if (!isAuthenticated) {
        // Redirect to login page, but save the current location they were trying to go to
        return <Navigate to="/login" state={{ from: location }} replace />;
    }

    return children;
}
