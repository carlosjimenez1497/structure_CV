import { useEffect } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Welcome() {
  const { user, loading } = useAuth();
  const navigate = useNavigate();

  // If user is already logged in → go to dashboard
  useEffect(() => {
    if (!loading && user) {
      navigate("/dashboard", { replace: true });
    }
  }, [loading, user, navigate]);

  if (loading) {
    return (
      <div className="h-screen flex items-center justify-center">
        <p className="text-gray-500 text-lg">Loading...</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-100">
      <div className="bg-white p-10 rounded-xl shadow-lg max-w-md w-full text-center">
        <h1 className="text-3xl font-bold mb-4">Welcome</h1>
        <p className="text-gray-600 mb-8">
          Create targeted, personalized CVs in seconds.
        </p>

        <div className="flex flex-col gap-4">
          <Link
            to="/login"
            className="w-full bg-blue-600 hover:bg-blue-700 text-white py-2 rounded-lg font-semibold transition"
          >
            Login
          </Link>

          <Link
            to="/register"
            className="w-full border border-gray-400 text-gray-700 py-2 rounded-lg font-semibold hover:bg-gray-100 transition"
          >
            Register
          </Link>
        </div>
      </div>
    </div>
  );
}
