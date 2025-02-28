import { BrowserRouter as Router, Route, Routes, Navigate } from "react-router-dom";
import { useState, useEffect } from "react";
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import Dashboard from "./pages/Dashboard";
import Lesson from "./pages/Lesson";

function App() {
  const [token, setToken] = useState(localStorage.getItem("token")); // ✅ Get token from localStorage

  // ✅ Update state when token changes
  useEffect(() => {
    const storedToken = localStorage.getItem("token");
    setToken(storedToken);
  }, [localStorage.getItem("token")]);

  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login setToken={setToken} />} />
        <Route path="/signup" element={<Signup setToken={setToken} />} />
        <Route path="/dashboard" element={token ? <Dashboard /> : <Navigate to="/" />} />
        <Route path="/lesson-1" element={token ? <Lesson /> : <Navigate to="/" />} />
      </Routes>
    </Router>
  );
}

export default App;


