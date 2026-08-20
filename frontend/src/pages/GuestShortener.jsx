import {
  ArrowLeft,
  Link2,
  Copy,
  Check,
  User,
} from "lucide-react";

import { useState } from "react";

function GuestShortener({
  url,
  setUrl,
  result,
  error,
  loading,
  onSubmit,
  onBack,
  onRegister,
  onLogin,
}) {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    if (!result?.short_url) return;

    navigator.clipboard.writeText(result.short_url);

    setCopied(true);

    setTimeout(() => {
      setCopied(false);
    }, 2000);
  };

  return (
    <div className="min-h-screen bg-slate-950 text-white">

      {/* Navbar */}
      <nav className="border-b border-slate-800">
        <div className="max-w-5xl mx-auto px-6 py-5 flex items-center justify-between">

          <button
            onClick={onBack}
            className="flex items-center gap-2 text-slate-400 hover:text-white transition"
          >
            <ArrowLeft size={18} />

            Back
          </button>

          <div className="flex items-center gap-2 font-bold">
            <div className="w-9 h-9 rounded-lg bg-blue-600 flex items-center justify-center">
              <Link2 size={18} />
            </div>

            LinkShort
          </div>

          <button
            onClick={onLogin}
            className="text-sm text-blue-400 hover:text-blue-300"
          >
            Sign in
          </button>

        </div>
      </nav>

      {/* Main */}
      <main className="max-w-2xl mx-auto px-6 py-20">

        {/* Header */}
        <div className="text-center mb-10">

          <div className="inline-flex items-center gap-2 bg-blue-500/10 border border-blue-500/20 text-blue-300 px-4 py-2 rounded-full text-sm">
            <User size={16} />

            Guest mode
          </div>

          <h1 className="text-4xl font-bold mt-6">
            Shorten your link
          </h1>

          <p className="text-slate-400 mt-3">
            You can create up to 5 short links as a guest.
          </p>

        </div>

        {/* Shortener */}
        <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 md:p-8 shadow-2xl">

          <form onSubmit={onSubmit}>

            <label className="block text-sm font-medium text-slate-300 mb-3">
              Paste your long URL
            </label>

            <input
              type="url"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              placeholder="https://example.com/your-long-url"
              className="w-full bg-slate-950 border border-slate-700 rounded-xl px-4 py-4 text-white placeholder-slate-600 outline-none focus:border-blue-500 transition"
              required
            />

            <button
              type="submit"
              disabled={loading}
              className="w-full mt-4 bg-blue-600 hover:bg-blue-500 disabled:bg-blue-900 disabled:cursor-not-allowed py-4 rounded-xl font-semibold transition"
            >
              {loading
                ? "Creating your short link..."
                : "Shorten URL"}
            </button>

          </form>

          {/* Error */}
          {error && (
            <div className="mt-5 border border-red-500/30 bg-red-500/10 text-red-400 rounded-xl p-4 text-sm">
              {error}
            </div>
          )}

          {/* Result */}
          {result && (
            <div className="mt-6 border border-slate-700 bg-slate-950 rounded-2xl p-5">

              <p className="text-sm text-slate-400 mb-3">
                Your shortened URL
              </p>

              <div className="flex items-center gap-3">

                <a
                  href={result.short_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-400 hover:text-blue-300 break-all flex-1 font-medium"
                >
                  {result.short_url}
                </a>

                <button
                  onClick={handleCopy}
                  className="p-2.5 bg-slate-800 hover:bg-slate-700 rounded-lg transition"
                  title="Copy URL"
                >
                  {copied
                    ? <Check size={18} className="text-green-400" />
                    : <Copy size={18} />
                  }
                </button>

              </div>

            </div>
          )}

          {/* Upgrade */}
          <div className="border-t border-slate-800 mt-8 pt-6 text-center">

            <p className="text-slate-400 text-sm">
              Want to manage all your links in one place?
            </p>

            <button
              onClick={onRegister}
              className="mt-3 text-blue-400 hover:text-blue-300 font-medium text-sm"
            >
              Create a free account →
            </button>

          </div>

        </div>

      </main>

    </div>
  );
}

export default GuestShortener;