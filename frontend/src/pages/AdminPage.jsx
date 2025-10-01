import useLogout from "../components/Logout";

function AdminPage({ username }) {

    const logout = useLogout();
    return (
      <div>
        <h1>Admin Dashboard</h1>
        <p>Welcome, {username}!</p>
        <button onClick={logout}>Logout</button>
      </div>
    );
  }
  
  export default AdminPage;