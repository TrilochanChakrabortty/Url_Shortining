// import { useState } from "react";
// import { shortenUrl } from "./services/api";
// import AuthPage from "./pages/AuthPage";
// import Register from "./pages/Register";
// import Login from "./pages/Login";
// import Dashboard from "./pages/Dashboard";

// function App() {
//   const [page, setPage] = useState("auth");

//   const [url, setUrl] = useState("");
//   const [result, setResult] = useState(null);
//   const [error, setError] = useState("");
//   const [loading, setLoading] = useState(false);

//   const handleSubmit = async (e) => {
//     e.preventDefault();

//     setError("");
//     setResult(null);
//     setLoading(true);

//     try {
//       const data = await shortenUrl(url);

//       setResult(data);
//     } catch (err) {
//       setError(err.message);
//     } finally {
//       setLoading(false);
//     }
//   };

//  if (page === "auth") {
//   return (
//     <AuthPage
//       onLogin={() => {
//         setPage("login");
//       }}
//       onRegister={() => {
//         setPage("register");
//       }}
//     />
//   );
// }

// if (page === "register") {
//   return (
//     <Register
//       onBackToHome={() => setPage("auth")}
//       onRegisterSuccess={() => setPage("login")}
//     />
//   );
// }

// if (page === "login") {
//   return (
//     <Login
//       onBack={() => setPage("auth")}
//       onLoginSuccess={(data) => {
//         console.log("Logged in user:", data.user);
//         console.log("Access token:", data.access_token);

//         setPage("dashboard")

//         // Dashboard will be connected in the next step.
//       }}
//     />
//   );
// }

//       if (page === "dashboard") {
//       return (
//       <Dashboard
//       onLogout={() => {
//         localStorage.removeItem("access_token");
//         setPage("auth");
//       }}
//     />
//   );
// }

//   // Show URL Shortener page
//   return (
//     <div className="min-h-screen bg-slate-950 text-white flex items-center justify-center px-4">
//       <div className="w-full max-w-2xl">

//         {/* Header */}
//         <div className="text-center mb-10">

//           <div className="text-5xl mb-4">
//             🔗
//           </div>

//           <h1 className="text-4xl md:text-5xl font-bold mb-4">
//             URL Shortener
//           </h1>

//           <p className="text-slate-400 text-lg">
//             Shorten your long URLs instantly
//           </p>

//           {/* Register Button */}
//           <button
//             onClick={() => setPage("register")}
//             className="mt-4 text-blue-400 hover:text-blue-300 font-medium transition"
//           >
//             Create an account
//           </button>

//         </div>

//         {/* URL Shortener Card */}
//         <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 md:p-8 shadow-2xl">

//           <form onSubmit={handleSubmit}>

//             <label className="block text-sm font-medium text-slate-300 mb-2">
//               Enter your URL
//             </label>

//             <input
//               type="url"
//               value={url}
//               onChange={(e) => setUrl(e.target.value)}
//               placeholder="https://example.com/your-very-long-url"
//               className="w-full bg-slate-800 border border-slate-700 rounded-xl px-4 py-3 text-white placeholder-slate-500 outline-none focus:border-blue-500 transition"
//               required
//             />

//             <button
//               type="submit"
//               disabled={loading}
//               className="w-full mt-4 bg-blue-600 hover:bg-blue-700 disabled:bg-blue-900 disabled:cursor-not-allowed text-white font-semibold py-3 rounded-xl transition"
//             >
//               {loading ? "Shortening..." : "Shorten URL"}
//             </button>

//           </form>

//           {/* Error */}
//           {error && (
//             <div className="mt-5 bg-red-500/10 border border-red-500/30 text-red-400 rounded-xl p-4">
//               {error}
//             </div>
//           )}

//           {/* Result */}
//           {result && (
//             <div className="mt-6 bg-slate-800 border border-slate-700 rounded-xl p-5">

//               <p className="text-sm text-slate-400 mb-2">
//                 Your shortened URL
//               </p>

//               <div className="flex items-center gap-3">

//                 <a
//                   href={result.short_url}
//                   target="_blank"
//                   rel="noopener noreferrer"
//                   className="text-blue-400 hover:text-blue-300 break-all flex-1"
//                 >
//                   {result.short_url}
//                 </a>

//                 <button
//                   onClick={() =>
//                     navigator.clipboard.writeText(result.short_url)
//                   }
//                   className="bg-slate-700 hover:bg-slate-600 px-4 py-2 rounded-lg text-sm font-medium whitespace-nowrap"
//                 >
//                   Copy
//                 </button>

//               </div>

//             </div>
//           )}

//         </div>

//       </div>
//     </div>
//   );
// }

// export default App;

import { useState } from "react";
import { shortenUrl } from "./services/api";

import AuthPage from "./pages/AuthPage";
import Register from "./pages/Register";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import GuestShortener from "./pages/GuestShortener";

function App() {
  // If a token already exists, directly open dashboard
  const [page, setPage] = useState(() => {
    const token = localStorage.getItem("access_token");

    return token ? "dashboard" : "auth";
  });

  const [url, setUrl] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();

    setError("");
    setResult(null);
    setLoading(true);

    try {
      const data = await shortenUrl(url);

      setResult(data);
    } catch (err) {
      setError(err.message || "Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  // -----------------------------
  // AUTH LANDING PAGE
  // -----------------------------
  if (page === "auth") {
    return (
      <AuthPage
        onGuest={() => setPage("guest")}
        onLogin={() => setPage("login")}
        onRegister={() => setPage("register")}
      />
    );
  }

  // -----------------------------
  // GUEST URL SHORTENER
  // -----------------------------
  if (page === "guest") {
    return (
      <GuestShortener
        url={url}
        setUrl={setUrl}
        result={result}
        error={error}
        loading={loading}
        onSubmit={handleSubmit}
        onBack={() => {
          setResult(null);
          setError("");
          setPage("auth");
        }}
        onRegister={() => setPage("register")}
        onLogin={() => setPage("login")}
      />
    );
  }

  // -----------------------------
  // REGISTER
  // -----------------------------
  if (page === "register") {
    return (
      <Register
        onBackToHome={() => setPage("auth")}
        onRegisterSuccess={() => setPage("login")}
      />
    );
  }

  // -----------------------------
  // LOGIN
  // -----------------------------
  if (page === "login") {
    return (
      <Login
        onBack={() => setPage("auth")}
        onLoginSuccess={(data) => {
          console.log("Logged in user:", data.user);

          // In case Login.jsx does not already store it
          if (data.access_token) {
            localStorage.setItem(
              "access_token",
              data.access_token
            );
          }

          setPage("dashboard");
        }}
      />
    );
  }

  // -----------------------------
  // DASHBOARD
  // -----------------------------
  if (page === "dashboard") {
    return (
      <Dashboard
        onLogout={() => {
          localStorage.removeItem("access_token");

          setPage("auth");
        }}
      />
    );
  }

  return null;
}

export default App;