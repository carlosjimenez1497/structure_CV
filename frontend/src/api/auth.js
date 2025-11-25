import api from "./client";

export async function login(email, password) {
  const res = await api.post("/auth/login", { email, password });
  return res.data; // expected: { access_token: "..." }
}

export async function register(email, password, full_name) {
  const res = await api.post("/auth/register", {
    email,
    password,
    full_name,
  });
  return res.data;
}
