import { useLocation } from "react-router-dom";
import AdminPage from "./AdminPage";
import UserPage from "./UserPage";

function Dashboard() {
    const location = useLocation();
    const username = location.state?.username || "user";
    const role = location.state?.role || "user";
  
    return (
      <div>
        {role === "admin" ? (
          <AdminPage username={username} />
        ) : (
          <UserPage username={username} />
        )}
      </div>
    );
  }
  
  export default Dashboard;