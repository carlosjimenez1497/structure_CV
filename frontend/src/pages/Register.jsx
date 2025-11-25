import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { register, login } from "../api/auth";
import { useAuth } from "../context/AuthContext";
import { fetchProfile } from "../api/profile";

export default function Register() {
  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [errorMsg, setErrorMsg] = useState("");

  const navigate = useNavigate();
  const { setUser } = useAuth();

  async function handleSubmit(e) {
    e.preventDefault();
    setErrorMsg("");

    try {
      // Create user
      await register(email, password, fullName);

      // Auto-login
      const res = await login(email, password);
      localStorage.setItem("access_token", res.access_token);

      // Load profile
      const profile = await fetchProfile();
      setUser(profile);

      // Go to dashboard
      navigate("/dashboard");
    } catch (err) {
      console.error(err);
      setErrorMsg("Error registering user.");
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-100 px-4">
      <div className="bg-white p-10 rounded-xl shadow-lg max-w-md w-full">
        <h1 className="text-3xl font-bold mb-6 text-center">Register</h1>

        {errorMsg && (
          <div className="mb-4 p-3 rounded bg-red-100 text-red-700 text-sm">
            {errorMsg}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <input
            className="w-full border border-gray-300 p-3 rounded-lg"
            placeholder="Full name"
            value={fullName}
            onChange={(e) => setFullName(e.target.value)}
            required
          />

          <input
            type="email"
            className="w-full border border-gray-300 p-3 rounded-lg"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />

          <input
            type="password"
            className="w-full border border-gray-300 p-3 rounded-lg"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />

          <button
            className="w-full bg-blue-600 hover:bg-blue-700 text-white py-2 rounded-lg text-lg font-semibold"
            type="submit"
          >
            Register
          </button>
        </form>

        <p className="mt-4 text-center text-sm text-gray-600">
          Already have an account?{" "}
          <Link to="/login" className="text-blue-600 font-semibold">
            Login
          </Link>
        </p>
      </div>
    </div>
  );
}
