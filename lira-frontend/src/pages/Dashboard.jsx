import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

function Dashboard() {
  const navigate = useNavigate();
  const [username, setUsername] = useState("");

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      navigate("/"); // Redirect to login if not authenticated
      return;
    }

    axios.get("http://127.0.0.1:8000/protected", {
      headers: { Authorization: `Bearer ${token}` }
    })
    .then((response) => {
      setUsername(response.data.email);
    })
    .catch(() => {
      localStorage.removeItem("token");
      navigate("/"); // Redirect to login if token is invalid
    });
  }, [navigate]);

  return (
    <div style={{ textAlign: "center", padding: "50px" }}>
      <h1>Welcome, {username}!</h1>
      <button onClick={() => alert("Starting from the beginning...")}>Start from the Beginning</button>
      <button onClick={() => navigate("/lesson-1")}>Access Lesson 1</button>
      <button onClick={() => alert("Viewing progress...")}>View Progress</button>
    </div>
  );
}

export default Dashboard;

