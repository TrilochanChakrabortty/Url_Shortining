import { useState } from "react";
import { registerUser } from "../services/api";

function Register({ onBackToHome, onRegisterSuccess }) {
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: "",
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const handleChange = (e) => {
    setFormData((prev) => ({
      ...prev,
      [e.target.name]: e.target.value,
    }));

    // Remove old messages when user starts typing again
    setError("");
    setSuccess("");
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    setError("");
    setSuccess("");
    setLoading(true);

    try {
      const data = await registerUser(formData);

      console.log("Registration successful:", data);

      // Show success message
      setSuccess(
        data?.message || "Account created successfully!"
      );

      // Clear form after successful registration
      setFormData({
        username: "",
        email: "",
        password: "",
      });

      // Move to login after successful registration
    setTimeout(() => {
    onRegisterSuccess();
    }, 1500);

    } catch (err) {
      console.error("Registration error:", err);

      setError(
        err.message || "Registration failed. Please try again."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-white flex items-center justify-center px-4">

      <div className="w-full max-w-md">

        {/* Header */}
        <div className="text-center mb-8">

          <div className="text-5xl mb-4">
            🔗
          </div>

          <h1 className="text-3xl font-bold">
            Create Account
          </h1>

          <p className="text-slate-400 mt-2">
            Create your account to manage your URLs
          </p>

        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 md:p-8 shadow-2xl">

          {/* SUCCESS MESSAGE */}
          {success && (
            <div className="mb-6 bg-green-500/10 border border-green-500/30 rounded-xl p-4">

              <div className="flex items-start gap-3">

                <div className="text-green-400 text-xl">
                  ✓
                </div>

                <div>
                  <p className="text-green-400 font-semibold">
                    Registration Successful
                  </p>

                  <p className="text-green-300/80 text-sm mt-1">
                    {success}
                  </p>
                </div>

              </div>

            </div>
          )}

          {/* ERROR MESSAGE */}
          {error && (
            <div className="mb-6 bg-red-500/10 border border-red-500/30 rounded-xl p-4">

              <div className="flex items-start gap-3">

                <div className="text-red-400 text-xl">
                  ✕
                </div>

                <div>
                  <p className="text-red-400 font-semibold">
                    Registration Failed
                  </p>

                  <p className="text-red-300/80 text-sm mt-1">
                    {error}
                  </p>
                </div>

              </div>

            </div>
          )}

          <form onSubmit={handleSubmit}>

            {/* Username */}
            <label className="block text-sm font-medium text-slate-300 mb-2">
              Username
            </label>

            <input
              type="text"
              name="username"
              value={formData.username}
              onChange={handleChange}
              placeholder="Enter username"
              required
              disabled={loading}
              className="w-full bg-slate-800 border border-slate-700 rounded-xl px-4 py-3 text-white placeholder-slate-500 outline-none focus:border-blue-500 transition"
            />

            {/* Email */}
            <label className="block text-sm font-medium text-slate-300 mb-2 mt-5">
              Email
            </label>

            <input
              type="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              placeholder="Enter email"
              required
              disabled={loading}
              className="w-full bg-slate-800 border border-slate-700 rounded-xl px-4 py-3 text-white placeholder-slate-500 outline-none focus:border-blue-500 transition"
            />

            {/* Password */}
            <label className="block text-sm font-medium text-slate-300 mb-2 mt-5">
              Password
            </label>

            <input
              type="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              placeholder="Enter password"
              required
              disabled={loading}
              className="w-full bg-slate-800 border border-slate-700 rounded-xl px-4 py-3 text-white placeholder-slate-500 outline-none focus:border-blue-500 transition"
            />

            {/* Submit */}
            <button
              type="submit"
              disabled={loading}
              className="w-full mt-6 bg-blue-600 hover:bg-blue-700 disabled:bg-blue-900 disabled:cursor-not-allowed text-white font-semibold py-3 rounded-xl transition"
            >
              {loading ? "Creating Account..." : "Create Account"}
            </button>

          </form>

          {/* Back */}
          <button
            type="button"
            onClick={onBackToHome}
            className="w-full mt-4 text-slate-400 hover:text-white text-sm transition"
          >
            Back to URL Shortener
          </button>

        </div>

      </div>

    </div>
  );
}

export default Register;