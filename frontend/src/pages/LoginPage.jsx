import { useNavigate } from "react-router-dom";
import React, { useState } from "react";
import './LoginPage.css';

function LoginPage() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    const res = await fetch("http://127.0.0.1:8000/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
      });

        try {
        const data = await res.json() 
        if (res.ok) {
            localStorage.setItem("token", data.access_token);
            navigate("/dashboard", { state: { username: data.username, role: data.role } });
        } else {
            setMessage(data.detail || "Login failed!");
        }
      } catch (e) {
        console.error("Failed to parse JSON:", e);
        setMessage("Response parsing error");
      }
      
  };

  return (
    <div className="login-container">
      <form onSubmit={handleSubmit}>
        {/* Message at the top */}
        {message && <p className="login-message">{message}</p>}
  
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button type="submit">Login</button>
      </form>
    </div>
  );
}

export default LoginPage;
