import { Navigate } from "react-router-dom";

function ProtectedRoute({ children, requiredRole }) {
  const user = JSON.parse(localStorage.getItem("user"));

  if (!user) return <Navigate to="/login" />; // not logged in
  if (requiredRole && user.role !== requiredRole) return <p>Access Denied</p>;

  return children;
}

export default ProtectedRoute;