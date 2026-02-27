/**
 * API utility — handles all backend communication.
 * In dev mode: connects to Flask at localhost:5000
 * In production (static export served by Flask): uses relative URLs
 */

const API_BASE = process.env.NODE_ENV === 'development'
    ? 'http://localhost:5000'
    : '';

export async function apiFetch(endpoint, options = {}) {
    const url = `${API_BASE}${endpoint}`;
    const res = await fetch(url, {
        headers: {
            'Content-Type': 'application/json',
            ...options.headers,
        },
        ...options,
    });

    if (!res.ok) {
        const error = await res.json().catch(() => ({ error: res.statusText }));
        throw new Error(error.error || `API Error: ${res.status}`);
    }

    return res.json();
}

export function apiStream(endpoint, body) {
    const url = `${API_BASE}${endpoint}`;
    return fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
    });
}

// Config
export const getConfig = () => apiFetch('/api/config');

// Settings
export const getSettings = () => apiFetch('/api/settings');
export const updateSettings = (data) => apiFetch('/api/settings', {
    method: 'PUT',
    body: JSON.stringify(data),
});

// Knowledge
export const listKnowledge = (category) => apiFetch(`/api/knowledge/${category}`);
export const getKnowledge = (category, name) => apiFetch(`/api/knowledge/${category}/${name}`);
export const updateKnowledge = (category, name, content) => apiFetch(`/api/knowledge/${category}/${name}`, {
    method: 'PUT',
    body: JSON.stringify({ content }),
});
export const createKnowledge = (category, name, content) => apiFetch(`/api/knowledge/${category}/${name}`, {
    method: 'POST',
    body: JSON.stringify({ content }),
});
export const deleteKnowledge = (category, name) => apiFetch(`/api/knowledge/${category}/${name}`, {
    method: 'DELETE',
});

// Reports
export const listReports = () => apiFetch('/api/reports');
export const getReport = (filename) => apiFetch(`/api/reports/${filename}`);
export const deleteReport = (filename) => apiFetch(`/api/reports/${filename}`, {
    method: 'DELETE',
});
