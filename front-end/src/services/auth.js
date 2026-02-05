// const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:3000';

// const jsonHeaders = {
//   'Content-Type': 'application/json',
// };

// async function handleResponse(response) {
//   let data = null;
//   try {
//     data = await response.json();
//   } catch (e) {
//     // ignore parse error, maybe empty body
//   }

//   if (!response.ok) {
//     const message =
//       (data && (data.message || data.error)) ||
//       `Request failed with status ${response.status}`;
//     throw new Error(message);
//   }

//   return data;
// }

// /**
//  * Login user
//  * @param {{ email: string, password: string }} payload
//  * @returns {Promise<any>} user data / tokens from backend
//  */
// export async function login(payload) {
//   const res = await fetch(`${BASE_URL}/auth/login`, {
//     method: 'POST',
//     headers: jsonHeaders,
//     body: JSON.stringify(payload),
//     credentials: 'include', // send cookies if backend uses them
//   });

//   return handleResponse(res);
// }

// /**
//  * Register user
//  * @param {{ name?: string, email: string, password: string, [key: string]: any }} payload
//  * @returns {Promise<any>} created user / tokens from backend
//  */
// export async function register(payload) {
//   const res = await fetch(`${BASE_URL}/auth/register`, {
//     method: 'POST',
//     headers: jsonHeaders,
//     body: JSON.stringify(payload),
//     credentials: 'include',
//   });

//   return handleResponse(res);
// }


import api from "@/services/index";

export const login = (identifier, password) => {
  return api.post("/v1/auth/login/", { identifier, password });
};
