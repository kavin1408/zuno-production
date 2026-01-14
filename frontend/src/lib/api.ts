const BACKEND_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

import { supabase } from './supabase';

// Get the real Supabase session token
const getSessionToken = async () => {
    const { data: { session }, error } = await supabase.auth.getSession();
    if (error) {
        console.error("Supabase session error:", error);
        return null;
    }
    return session?.access_token || null;
};

export const api = {
    get: async (endpoint: string) => {
        const token = await getSessionToken();
        if (!token) {
            console.warn("No auth token available for GET", endpoint);
        }

        const res = await fetch(`${BACKEND_URL}${endpoint}`, {
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json',
            },
        });

        if (!res.ok) {
            const errorText = await res.text();
            throw new Error(errorText || `Request failed with status ${res.status}`);
        }
        return res.json();
    },

    post: async (endpoint: string, body: any) => {
        const token = await getSessionToken();
        if (!token) {
            console.warn("No auth token available for POST", endpoint);
        }

        const res = await fetch(`${BACKEND_URL}${endpoint}`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(body),
        });

        if (!res.ok) {
            const errorText = await res.text();
            throw new Error(errorText || `Request failed with status ${res.status}`);
        }
        return res.json();
    },

    put: async (endpoint: string, body: any) => {
        const token = await getSessionToken();
        if (!token) {
            console.warn("No auth token available for PUT", endpoint);
        }

        const res = await fetch(`${BACKEND_URL}${endpoint}`, {
            method: 'PUT',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(body),
        });

        if (!res.ok) {
            const errorText = await res.text();
            throw new Error(errorText || `Request failed with status ${res.status}`);
        }
        return res.json();
    },

    // Logout function to clear session
    logout: async () => {
        await supabase.auth.signOut();
        localStorage.clear();
    }
};
