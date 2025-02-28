import { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

function Login({ setToken }) {  // ✅ Accept setToken prop from App.jsx
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleLogin = async (e) => {
    e.preventDefault();
    setError(""); // Reset error message

    try {
      const response = await axios.post("http://127.0.0.1:8000/login", {
        email,
        password,
      });

      const token = response.data.access_token;
      localStorage.setItem("token", token);  // ✅ Store JWT in localStorage
      setToken(token);  // ✅ Update state in App.jsx
      navigate("/dashboard"); // ✅ Redirect to Dashboard
    } catch (err) {
      setError(err.response?.data?.detail || "Invalid email or password.");  // ✅ Display backend error
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="p-8 bg-white shadow-lg rounded-lg w-96">
        <h2 className="text-2xl font-bold mb-4 text-center">Lira App - Login</h2>
        {error && <p className="text-red-500 text-center">{error}</p>}
        
        <form onSubmit={handleLogin} className="space-y-4">
          <input
            type="email"
            className="p-2 border rounded w-full"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
          <input
            type="password"
            className="p-2 border rounded w-full"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          <button type="submit" className="w-full bg-blue-500 text-white p-2 rounded hover:bg-blue-700">
            Login
          </button>
        </form>

        <p className="mt-4 text-center">
          Don't have an account?{" "}
          <button className="text-blue-500 underline" onClick={() => navigate("/signup")}>
            Sign Up
          </button>
        </p>
      </div>
    </div>
  );
}

export default Login;
