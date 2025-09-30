import AdminPanel from "./AdminPanel";
import UserPanel from "./UserPanel";

function Dashboard() {
  const user = JSON.parse(localStorage.getItem("user"));
  if (!user) return <p>Please log in</p>;

  return (
    <div>
      <h1>Welcome, {user.username}!</h1>

      {user.role === "ADMIN" ? <AdminPanel /> : <UserPanel />}
    </div>
  );
}

export default Dashboard;