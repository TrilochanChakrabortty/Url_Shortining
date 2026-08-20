import { Routes, Route } from "react-router-dom";

import App from "../App";
import Register from "../pages/Register";
import OAuthSuccess from "../pages/OAuthSuccess";

function AppRoutes() {
  return (
    <Routes>

      <Route
        path="/"
        element={<App />}
      />

      <Route
        path="/register"
        element={<Register />}
      />

      <Route
        path="/oauth-success"
        element={<OAuthSuccess />}
      />

    </Routes>
  );
}

export default AppRoutes;