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

// Handle 401 errors - logout and redirect
const handle401Error = async () => {
    console.error('401 Unauthorized - Session expired or invalid token');

    // Clear session
    await supabase.auth.signOut();
    localStorage.clear();

    // Redirect to login
    window.location.href = '/login';
};

// Generic request handler with 401 handling
const makeRequest = async (endpoint: string, options: RequestInit = {}) => {
    const token = await getSessionToken();

    if (!token) {
        console.error("No auth token available - redirecting to login");
        await handle401Error();
        throw new Error('Authentication required');
    }

    const res = await fetch(`${BACKEND_URL}${endpoint}`, {
        ...options,
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
            ...options.headers,
        },
    });

    // Handle 401 Unauthorized
    if (res.status === 401) {
        console.error('401 Unauthorized response from backend');
        await handle401Error();
        throw new Error('Session expired or invalid token');
    }

    if (!res.ok) {
        let errorMessage = `Request failed with status ${res.status}`;
        try {
            const errorData = await res.json();
            errorMessage = errorData.detail || errorData.message || errorMessage;
        } catch {
            const errorText = await res.text();
            errorMessage = errorText || errorMessage;
        }
        throw new Error(errorMessage);
    }

    return res.json();
};

export const api = {
    get: async (endpoint: string) => {
        return makeRequest(endpoint, { method: 'GET' });
    },

    post: async (endpoint: string, body: any) => {
        return makeRequest(endpoint, {
            method: 'POST',
            body: JSON.stringify(body),
        });
    },

    put: async (endpoint: string, body: any) => {
        return makeRequest(endpoint, {
            method: 'PUT',
            body: JSON.stringify(body),
        });
    },

    patch: async (endpoint: string, body: any) => {
        return makeRequest(endpoint, {
            method: 'PATCH',
            body: JSON.stringify(body),
        });
    },

    delete: async (endpoint: string) => {
        return makeRequest(endpoint, { method: 'DELETE' });
    },

    // Logout function to clear session
    logout: async () => {
        await supabase.auth.signOut();
        localStorage.clear();
        window.location.href = '/login';
    }
};

