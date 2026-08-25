// ============================================================
// API CONFIGURATION
// ============================================================

const API_URL = "http://127.0.0.1:8000";


// ============================================================
// GET AUTH TOKEN
// ============================================================

const getAccessToken = () => {
  return localStorage.getItem("access_token");
};


// ============================================================
// HANDLE API RESPONSE
// ============================================================

const parseResponse = async (response) => {
  let data;

  try {
    data = await response.json();
  } catch {
    data = {};
  }

  if (!response.ok) {
    throw new Error(
      data.detail?.[0]?.msg ||
      data.detail ||
      `Request failed with status ${response.status}`
    );
  }

  return data;
};


// ============================================================
// REGISTER USER
// ============================================================

export const registerUser = async (userData) => {
  const response = await fetch(
    `${API_URL}/auth/register`,
    {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },

      body: JSON.stringify(userData),
    }
  );

  return await parseResponse(response);
};


// ============================================================
// LOGIN USER
// ============================================================

export const loginUser = async (userData) => {
  const response = await fetch(
    `${API_URL}/auth/login`,
    {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },

      body: JSON.stringify(userData),
    }
  );

  const data = await parseResponse(response);

  // ----------------------------------------------------------
  // IMPORTANT:
  // Save the newly generated JWT immediately.
  // ----------------------------------------------------------

  if (data.access_token) {
    localStorage.setItem(
      "access_token",
      data.access_token
    );
  }

  console.log(
    "LOGIN SUCCESS - TOKEN STORED"
  );

  console.log(
    "TOKEN LENGTH:",
    data.access_token?.length
  );

  return data;
};


// ============================================================
// LOGOUT USER
// ============================================================

export const logoutUser = () => {
  localStorage.removeItem("access_token");
};


// ============================================================
// CREATE SHORT URL - GUEST
// ============================================================

export const shortenUrl = async (url) => {
  const response = await fetch(
    `${API_URL}/shorten`,
    {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },

      body: JSON.stringify({
        url: url,
      }),
    }
  );

  return await parseResponse(response);
};


// ============================================================
// CREATE SHORT URL - AUTHENTICATED
// ============================================================

export const shortenUrlAuthenticated = async (url) => {
  const token = getAccessToken();

  console.log(
    "========== SHORTEN REQUEST =========="
  );

  console.log(
    "TOKEN EXISTS:",
    !!token
  );

  console.log(
    "TOKEN LENGTH:",
    token?.length
  );

  if (!token) {
    throw new Error(
      "You are not logged in."
    );
  }

  const response = await fetch(
    `${API_URL}/shorten`,
    {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",

        Authorization:
          `Bearer ${token}`,
      },

      body: JSON.stringify({
        url: url,
      }),
    }
  );

  const data = await parseResponse(response);

  console.log(
    "SHORTEN STATUS:",
    response.status
  );

  console.log(
    "SHORTEN RESPONSE:",
    data
  );

  return data;
};


// ============================================================
// GET DASHBOARD STATISTICS
// ============================================================

export const getDashboardStats = async () => {
  const token = getAccessToken();

  console.log(
    "========== DASHBOARD REQUEST =========="
  );

  console.log(
    "API URL:",
    `${API_URL}/dashboard/stats`
  );

  console.log(
    "TOKEN EXISTS:",
    !!token
  );

  console.log(
    "TOKEN LENGTH:",
    token?.length
  );

  console.log(
    "TOKEN PREVIEW:",
    token
      ? `${token.substring(0, 40)}...`
      : null
  );

  console.log(
    "======================================="
  );

  if (!token) {
    throw new Error(
      "No access token found. Please login again."
    );
  }

  const response = await fetch(
    `${API_URL}/dashboard/stats`,
    {
      method: "GET",

      headers: {
        Accept: "application/json",

        Authorization:
          `Bearer ${token}`,
      },
    }
  );

  const data = await response.json();

  console.log(
    "========== DASHBOARD RESPONSE =========="
  );

  console.log(
    "STATUS:",
    response.status
  );

  console.log(
    "DATA:",
    data
  );

  console.log(
    "========================================"
  );

  // ----------------------------------------------------------
  // JWT rejected
  // ----------------------------------------------------------

  if (response.status === 401) {

    console.error(
      "JWT rejected by backend."
    );

    // Remove invalid/stale token.

    localStorage.removeItem(
      "access_token"
    );

    throw new Error(
      "Session expired or invalid. Please login again."
    );
  }

  if (!response.ok) {
    throw new Error(
      data.detail ||
      "Failed to fetch dashboard statistics"
    );
  }

  return data;
};