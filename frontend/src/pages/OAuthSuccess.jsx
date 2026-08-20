import { useEffect } from "react";
import { useNavigate } from "react-router-dom";

function OAuthSuccess() {
  const navigate = useNavigate();

  useEffect(() => {
    const params = new URLSearchParams(
      window.location.search
    );

    const token = params.get("token");

    if (token) {
      localStorage.setItem(
        "access_token",
        token
      );
    }

    // Remove token from URL and return to app
    navigate("/", {
      replace: true,
    });
  }, [navigate]);

  return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center text-white">
      <div className="text-center">

        <div className="w-12 h-12 mx-auto border-4 border-slate-700 border-t-blue-500 rounded-full animate-spin" />

        <h2 className="text-xl font-semibold mt-6">
          Signing you in...
        </h2>

        <p className="text-slate-400 text-sm mt-2">
          Please wait while we complete your authentication.
        </p>

      </div>
    </div>
  );
}

export default OAuthSuccess;