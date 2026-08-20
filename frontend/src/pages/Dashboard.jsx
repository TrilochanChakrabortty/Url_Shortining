import { useState, useEffect } from "react";
import {
  shortenUrlAuthenticated,
  getDashboardStats,
} from "../services/api";

function Dashboard({ onLogout }) {
  // ============================================================
  // DASHBOARD STATISTICS
  // ============================================================

  const [stats, setStats] = useState({
    total_urls: 0,
    total_clicks: 0,
    account_status: "Active",
  });

  const [statsLoading, setStatsLoading] = useState(true);

  // ============================================================
  // URL SHORTENER STATE
  // ============================================================

  const [url, setUrl] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  // ============================================================
  // LOAD DASHBOARD STATISTICS
  // ============================================================

  const loadDashboardStats = async () => {
    try {
      setStatsLoading(true);

      const token = localStorage.getItem("access_token");

      if (!token) {
        throw new Error("No access token found");
      }

      const data = await getDashboardStats(token);

      console.log("Dashboard stats:", data);

      setStats({
        total_urls: data.total_urls ?? 0,
        total_clicks: data.total_clicks ?? 0,
        account_status: data.account_status ?? "Active",
      });

    } catch (err) {
      console.error(
        "Failed to load dashboard statistics:",
        err
      );

    } finally {
      setStatsLoading(false);
    }
  };

  // ============================================================
  // FETCH STATS WHEN DASHBOARD LOADS
  // ============================================================

  useEffect(() => {
    loadDashboardStats();
  }, []);

  // ============================================================
  // CREATE SHORT URL
  // ============================================================

  const handleSubmit = async (e) => {
    e.preventDefault();

    setError("");
    setResult(null);
    setLoading(true);

    try {
      const data = await shortenUrlAuthenticated(url);

      // Show newly created short URL
      setResult(data);

      // Clear input
      setUrl("");

      // Refresh stats from database
      await loadDashboardStats();

    } catch (err) {
      setError(
        err.message || "Failed to create shortened URL"
      );

    } finally {
      setLoading(false);
    }
  };

  // ============================================================
  // COPY SHORT URL
  // ============================================================

  const handleCopy = async () => {
    if (!result?.short_url) return;

    try {
      await navigator.clipboard.writeText(
        result.short_url
      );
    } catch (err) {
      console.error("Failed to copy URL:", err);
    }
  };

  // ============================================================
  // LOGOUT
  // ============================================================

  const handleLogout = () => {
    localStorage.removeItem("access_token");

    onLogout();
  };

  // ============================================================
  // UI
  // ============================================================

  return (
    <div className="min-h-screen bg-slate-950 text-white">

      {/* Navbar */}
      <nav className="border-b border-slate-800 bg-slate-900">

        <div className="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">

          <div className="flex items-center gap-3">

            <span className="text-3xl">
              🔗
            </span>

            <div>
              <h1 className="font-bold text-lg">
                URL Shortener
              </h1>

              <p className="text-xs text-slate-400">
                Dashboard
              </p>
            </div>

          </div>

          <button
            onClick={handleLogout}
            className="bg-red-500/10 border border-red-500/30 text-red-400 hover:bg-red-500/20 px-4 py-2 rounded-lg text-sm font-medium transition"
          >
            Logout
          </button>

        </div>

      </nav>

      {/* Dashboard */}
      <main className="max-w-6xl mx-auto px-6 py-10">

        {/* Header */}
        <div className="mb-8">

          <h2 className="text-3xl font-bold">
            Dashboard
          </h2>

          <p className="text-slate-400 mt-2">
            Create and manage your shortened URLs.
          </p>

        </div>

        {/* Statistics */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-5 mb-8">

          {/* Total URLs */}
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6">

            <p className="text-slate-400 text-sm">
              Total URLs
            </p>

            <p className="text-3xl font-bold mt-2">
              {statsLoading
                ? "..."
                : stats.total_urls}
            </p>

          </div>

          {/* Total Clicks */}
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6">

            <p className="text-slate-400 text-sm">
              Total Clicks
            </p>

            <p className="text-3xl font-bold mt-2">
              {statsLoading
                ? "..."
                : stats.total_clicks}
            </p>

          </div>

          {/* Account Status */}
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6">

            <p className="text-slate-400 text-sm">
              Account Status
            </p>

            <p className="text-green-400 text-xl font-semibold mt-2">
              {stats.account_status}
            </p>

          </div>

        </div>

        {/* Create Short URL */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-8">

          <h3 className="text-xl font-semibold mb-2">
            Shorten a URL
          </h3>

          <p className="text-slate-400 mb-6">
            Enter a long URL to create a short link.
          </p>

          <form onSubmit={handleSubmit}>

            <input
              type="url"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              placeholder="https://example.com/your-long-url"
              required
              disabled={loading}
              className="w-full bg-slate-800 border border-slate-700 rounded-xl px-4 py-3 text-white placeholder-slate-500 outline-none focus:border-blue-500 transition"
            />

            <button
              type="submit"
              disabled={loading}
              className="w-full mt-4 bg-blue-600 hover:bg-blue-700 disabled:bg-blue-900 disabled:cursor-not-allowed text-white font-semibold py-3 rounded-xl transition"
            >
              {loading
                ? "Shortening..."
                : "Create Short URL"}
            </button>

          </form>

          {/* Error */}
          {error && (
            <div className="mt-5 bg-red-500/10 border border-red-500/30 text-red-400 rounded-xl p-4">
              {error}
            </div>
          )}

          {/* Result */}
          {result && (
            <div className="mt-6 bg-slate-800 border border-slate-700 rounded-xl p-5">

              <p className="text-sm text-slate-400 mb-2">
                Your shortened URL
              </p>

              <div className="flex items-center gap-3">

                <a
                  href={result.short_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-400 hover:text-blue-300 break-all flex-1"
                >
                  {result.short_url}
                </a>

                <button
                  type="button"
                  onClick={handleCopy}
                  className="bg-slate-700 hover:bg-slate-600 px-4 py-2 rounded-lg text-sm font-medium whitespace-nowrap"
                >
                  Copy
                </button>

              </div>

            </div>
          )}

        </div>

      </main>

    </div>
  );
}

export default Dashboard;