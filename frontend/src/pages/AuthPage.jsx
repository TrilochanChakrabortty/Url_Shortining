// function AuthPage({ onLogin, onRegister }) {
//   return (
//     <div className="min-h-screen bg-slate-950 text-white flex items-center justify-center px-4">

//       <div className="w-full max-w-md">

//         {/* Logo / Header */}
//         <div className="text-center mb-8">

//           <div className="text-6xl mb-5">
//             🔗
//           </div>

//           <h1 className="text-4xl font-bold mb-3">
//             URL Shortener
//           </h1>

//           <p className="text-slate-400 text-base">
//             Create and manage your shortened URLs
//           </p>

//         </div>

//         {/* Authentication Card */}
//         <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 md:p-8 shadow-2xl">

//           <div className="text-center mb-7">

//             <h2 className="text-2xl font-semibold">
//               Welcome
//             </h2>

//             <p className="text-slate-400 text-sm mt-2">
//               Login to your account or create a new one
//             </p>

//           </div>

//           {/* Login */}
//           <button
//             type="button"
//             onClick={onLogin}
//             className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 rounded-xl transition"
//           >
//             Login
//           </button>

//           {/* Register */}
//           <button
//             type="button"
//             onClick={onRegister}
//             className="w-full mt-4 bg-slate-800 hover:bg-slate-700 border border-slate-700 text-white font-semibold py-3 rounded-xl transition"
//           >
//             Create Account
//           </button>

//         </div>

//         <p className="text-center text-slate-500 text-xs mt-6">
//           Secure URL management made simple
//         </p>

//       </div>

//     </div>
//   );
// }

// export default AuthPage;

import {
  Link2,
  ArrowRight,
  User,
  LogIn,
  Sparkles,
  ShieldCheck,
  BarChart3,
} from "lucide-react";

function AuthPage({
  onGuest,
  onLogin,
  onRegister,
}) {
  return (
    <div className="min-h-screen bg-slate-950 text-white relative overflow-hidden">

      {/* Background */}
      <div className="absolute inset-0 bg-gradient-to-br from-blue-950/40 via-slate-950 to-slate-950" />

      {/* Navigation */}
      <nav className="relative z-10 flex items-center justify-between max-w-6xl mx-auto px-6 py-6">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-blue-600 flex items-center justify-center shadow-lg shadow-blue-500/20">
            <Link2 size={21} />
          </div>

          <span className="text-xl font-bold tracking-tight">
            LinkShort
          </span>
        </div>

        <button
          onClick={onLogin}
          className="text-sm font-medium text-slate-300 hover:text-white transition"
        >
          Sign in
        </button>
      </nav>

      {/* Main */}
      <main className="relative z-10 max-w-6xl mx-auto px-6 pt-12 pb-16">

        <div className="grid lg:grid-cols-2 gap-14 items-center min-h-[75vh]">

          {/* Left Content */}
          <div>

            <div className="inline-flex items-center gap-2 bg-blue-500/10 border border-blue-500/20 px-4 py-2 rounded-full text-sm text-blue-300 mb-6">
              <Sparkles size={16} />
              Simple. Fast. Reliable.
            </div>

            <h1 className="text-4xl md:text-6xl font-bold leading-tight tracking-tight">
              Short links.
              <br />

              <span className="text-blue-500">
                Bigger possibilities.
              </span>
            </h1>

            <p className="mt-6 text-lg text-slate-400 max-w-xl leading-relaxed">
              Create short, clean links in seconds. Continue as a guest
              or create an account to manage and track your URLs.
            </p>

            {/* Features */}
            <div className="mt-10 grid gap-5">

              <div className="flex items-center gap-4">
                <div className="w-10 h-10 rounded-xl bg-slate-900 border border-slate-800 flex items-center justify-center text-blue-400">
                  <Link2 size={19} />
                </div>

                <div>
                  <h3 className="font-medium">
                    Instant URL shortening
                  </h3>

                  <p className="text-sm text-slate-500">
                    Create clean short links instantly.
                  </p>
                </div>
              </div>

              <div className="flex items-center gap-4">
                <div className="w-10 h-10 rounded-xl bg-slate-900 border border-slate-800 flex items-center justify-center text-blue-400">
                  <BarChart3 size={19} />
                </div>

                <div>
                  <h3 className="font-medium">
                    Manage your links
                  </h3>

                  <p className="text-sm text-slate-500">
                    Registered users can manage their URLs.
                  </p>
                </div>
              </div>

              <div className="flex items-center gap-4">
                <div className="w-10 h-10 rounded-xl bg-slate-900 border border-slate-800 flex items-center justify-center text-blue-400">
                  <ShieldCheck size={19} />
                </div>

                <div>
                  <h3 className="font-medium">
                    Secure authentication
                  </h3>

                  <p className="text-sm text-slate-500">
                    Login securely using email or Google.
                  </p>
                </div>
              </div>

            </div>
          </div>

          {/* Right Card */}
          <div className="w-full max-w-md mx-auto">

            <div className="bg-slate-900/80 backdrop-blur-xl border border-slate-800 rounded-3xl p-7 md:p-8 shadow-2xl">

              <h2 className="text-2xl font-bold">
                Get started
              </h2>

              <p className="text-slate-400 text-sm mt-2 mb-7">
                Choose how you want to use LinkShort.
              </p>

              {/* Guest */}
              <button
                onClick={onGuest}
                className="w-full group flex items-center justify-between p-4 rounded-2xl bg-blue-600 hover:bg-blue-500 transition shadow-lg shadow-blue-900/30"
              >
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-xl bg-white/15 flex items-center justify-center">
                    <User size={19} />
                  </div>

                  <div className="text-left">
                    <p className="font-semibold">
                      Continue as Guest
                    </p>

                    <p className="text-xs text-blue-100">
                      Create up to 5 short links
                    </p>
                  </div>
                </div>

                <ArrowRight
                  size={19}
                  className="group-hover:translate-x-1 transition"
                />
              </button>

              {/* Divider */}
              <div className="flex items-center gap-3 my-6">
                <div className="h-px bg-slate-800 flex-1" />

                <span className="text-xs text-slate-500">
                  OR
                </span>

                <div className="h-px bg-slate-800 flex-1" />
              </div>

              {/* Register */}
              <button
                onClick={onRegister}
                className="w-full flex items-center justify-center gap-2 bg-slate-800 hover:bg-slate-700 border border-slate-700 py-3.5 rounded-xl font-medium transition"
              >
                Create free account

                <ArrowRight size={18} />
              </button>

              {/* Login */}
              <button
                onClick={onLogin}
                className="w-full flex items-center justify-center gap-2 text-slate-300 hover:text-white py-4 text-sm transition"
              >
                <LogIn size={17} />

                Already have an account? Sign in
              </button>

            </div>

          </div>

        </div>
      </main>

      {/* Footer */}
      <footer className="relative z-10 text-center text-sm text-slate-600 pb-8">
        © 2026 LinkShort. Fast and simple URL shortening.
      </footer>

    </div>
  );
}

export default AuthPage;