import api from "./client";

export async function fetchProfile() {
  const res = await api.get("/users/me");
  return res.data;
}

export async function updateProfile(profile) {
  const res = await api.put("/users/me", profile);
  return res.data;
}
