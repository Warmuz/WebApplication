import useLogout from "../components/Logout";
function UserPage({ username }) {
  const logout = useLogout();
    return (
      <div>
        <h1>User Dashboard</h1>
        <p>Welcome, {username}!</p>
        <button onClick={logout}>Logout</button>
      </div>
    );
  }
  
  export default UserPage;
  