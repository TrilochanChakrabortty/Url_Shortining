import { useState } from "react";
import { ArrowLeft, User, Lock, LogIn } from "lucide-react";
import { loginUser } from "../services/api";

function Login({ onBack, onLoginSuccess }) {
  // ----------------------------------
  // Form State
  // ----------------------------------
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  // ----------------------------------
  // UI State
  // ----------------------------------
  const [loading, setLoading] = useState(false);
  const [googleLoading, setGoogleLoading] = useState(false);
  const [error, setError] = useState("");

  // ----------------------------------
  // Username + Password Login
  // ----------------------------------
  const handleSubmit = async (e) => {
    e.preventDefault();

    setError("");
    setLoading(true);

    try {
      const data = await loginUser({
        username,
        password,
      });

      // Save JWT token
      if (data.access_token) {
        localStorage.setItem(
          "access_token",
          data.access_token
        );
      }

      // Move to dashboard
      onLoginSuccess(data);

    } catch (err) {
      setError(
        err.message || "Invalid username or password"
      );
    } finally {
      setLoading(false);
    }
  };

  // ----------------------------------
  // Google OAuth Login
  // ----------------------------------
  const handleGoogleLogin = () => {
    setGoogleLoading(true);

    // Redirect to FastAPI Google OAuth endpoint
    window.location.href =
      "http://127.0.0.1:8000/auth/google/login";
  };

  return (
    <div className="min-h-screen bg-slate-950 text-white flex items-center justify-center px-4">

      <div className="w-full max-w-md">

        {/* Back Button */}
        <button
          onClick={onBack}
          className="flex items-center gap-2 text-sm text-slate-400 hover:text-white transition mb-8"
        >
          <ArrowLeft size={18} />
          Back
        </button>

        {/* Login Card */}
        <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 md:p-8 shadow-2xl">

          {/* Header */}
          <div className="text-center mb-8">

            <div className="w-12 h-12 mx-auto mb-4 rounded-xl bg-blue-600 flex items-center justify-center">
              <LogIn size={22} />
            </div>

            <h1 className="text-2xl font-bold">
              Welcome back
            </h1>

            <p className="text-slate-400 text-sm mt-2">
              Sign in to manage your shortened links.
            </p>

          </div>

          {/* Error Message */}
          {error && (
            <div className="mb-5 border border-red-500/30 bg-red-500/10 text-red-400 rounded-xl p-3 text-sm">
              {error}
            </div>
          )}

          {/* Login Form */}
          <form onSubmit={handleSubmit}>

            {/* Username */}
            <div className="mb-4">

              <label className="block text-sm font-medium text-slate-300 mb-2">
                Username
              </label>

              <div className="relative">

                <User
                  size={18}
                  className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500"
                />

                <input
                  type="text"
                  value={username}
                  onChange={(e) =>
                    setUsername(e.target.value)
                  }
                  placeholder="Enter your username"
                  className="w-full bg-slate-950 border border-slate-700 rounded-xl pl-11 pr-4 py-3.5 text-white placeholder-slate-600 outline-none focus:border-blue-500 transition"
                  required
                />

              </div>

            </div>

            {/* Password */}
            <div className="mb-6">

              <label className="block text-sm font-medium text-slate-300 mb-2">
                Password
              </label>

              <div className="relative">

                <Lock
                  size={18}
                  className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500"
                />

                <input
                  type="password"
                  value={password}
                  onChange={(e) =>
                    setPassword(e.target.value)
                  }
                  placeholder="Enter your password"
                  className="w-full bg-slate-950 border border-slate-700 rounded-xl pl-11 pr-4 py-3.5 text-white placeholder-slate-600 outline-none focus:border-blue-500 transition"
                  required
                />

              </div>

            </div>

            {/* Login Button */}
            <button
              type="submit"
              disabled={loading || googleLoading}
              className="w-full bg-blue-600 hover:bg-blue-500 disabled:bg-blue-900 disabled:cursor-not-allowed py-3.5 rounded-xl font-semibold transition"
            >
              {loading
                ? "Signing in..."
                : "Sign in"}
            </button>

          </form>

          {/* Divider */}
          <div className="flex items-center gap-3 my-6">

            <div className="h-px bg-slate-800 flex-1" />

            <span className="text-xs text-slate-500">
              OR
            </span>

            <div className="h-px bg-slate-800 flex-1" />

          </div>

          {/* Google Login */}
          <button
            type="button"
            onClick={handleGoogleLogin}
            disabled={loading || googleLoading}
            className="w-full flex items-center justify-center gap-3 bg-white hover:bg-slate-200 disabled:bg-slate-300 text-slate-900 py-3.5 rounded-xl font-semibold transition"
          >
            {googleLoading ? (
              <>
                <div className="w-5 h-5 border-2 border-slate-400 border-t-slate-900 rounded-full animate-spin" />

                Redirecting to Google...
              </>
            ) : (
              <>
                <span className="font-bold text-lg">
                  G
                </span>

                Continue with Google
              </>
            )}
          </button>

          {/* Footer */}
          <div className="mt-7 text-center">

            <p className="text-sm text-slate-400">
              Don't have an account?
            </p>

            <button
              type="button"
              onClick={onBack}
              className="mt-2 text-sm text-blue-400 hover:text-blue-300 font-medium transition"
            >
              Create an account
            </button>

          </div>

        </div>

      </div>

    </div>
  );
}

export default Login;