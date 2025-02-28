import { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

function Signup({ setToken }) {  // ✅ Accept setToken prop from App.jsx
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("student");
  const [error, setError] = useState("");

  const handleSignup = async (e) => {
    e.preventDefault();
    setError(""); // Reset error message

    try {
      const response = await axios.post("http://127.0.0.1:8000/signup", {
        username,
        email,
        password,
        role,
      });

      const token = response.data.access_token;
      localStorage.setItem("token", token);  // ✅ Store JWT
      setToken(token);  // ✅ Update state in App.jsx
      navigate("/dashboard");  // ✅ Redirect to Dashboard
    } catch (err) {
      setError(err.response?.data?.detail || "Sign-up failed. Try again.");  // ✅ Show real API error
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="p-8 bg-white shadow-lg rounded-lg w-96">
        <h2 className="text-2xl font-bold mb-4 text-center">Lira App - Sign Up</h2>
        {error && <p className="text-red-500 text-center">{error}</p>}
        
        <form onSubmit={handleSignup} className="space-y-4">
          <input
            type="text"
            className="p-2 border rounded w-full"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
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
          <label className="block text-sm font-medium">Role:</label>
          <select
            className="p-2 border rounded w-full"
            value={role}
            onChange={(e) => setRole(e.target.value)}
          >
            <option value="student">Student</option>
            <option value="teacher">Teacher</option>
          </select>
          <button type="submit" className="w-full bg-blue-500 text-white p-2 rounded hover:bg-blue-700">
            Sign Up
          </button>
        </form>

        <p className="mt-4 text-center">
          Already have an account?{" "}
          <button className="text-blue-500 underline" onClick={() => navigate("/")}>
            Login
          </button>
        </p>
      </div>
    </div>
  );
}

export default Signup;
