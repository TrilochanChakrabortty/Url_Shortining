const API_URL = "http://localhost:8000";

export async function shortenUrl(url) {
  const response = await fetch(`${API_URL}/shorten`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      url: url,
    }),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail?.[0]?.msg ||
      data.detail ||
      "Failed to shorten URL"
    );
  }

  return data;
}

export const registerUser = async (userData) => {
  const response = await fetch(`${API_URL}/auth/register`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(userData),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail || "Registration failed"
    );
  }

  return data;
};

export const loginUser = async (userData) => {
  const response = await fetch(`${API_URL}/auth/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(userData),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail || "Login failed"
    );
  }

  return data;
};

export const shortenUrlAuthenticated = async (url) => {
  const token = localStorage.getItem("access_token");

  if (!token) {
    throw new Error("You are not logged in.");
  }

  const response = await fetch(`${API_URL}/shorten`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${token}`,
    },
    body: JSON.stringify({
      url: url,
    }),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail?.[0]?.msg ||
      data.detail ||
      "Failed to shorten URL"
    );
  }

  return data;
};

export const getDashboardStats = async (token) => {
  const response = await fetch(
    "http://127.0.0.1:8000/dashboard/stats",
    {
      method: "GET",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );

  const data = await response.json();

  console.log("Dashboard API Response:", data);

  if (!response.ok) {
    throw new Error(
      data.detail || "Failed to fetch dashboard statistics"
    );
  }

  return data;
};