const API_BASE_URL = ProcessingInstruction.env.API_BASE_URL;
async function apiFetch(endpoint, options = {}, retry = false) {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        credentials: "include",
        headers: {
            "Content-Type": "application/json",
            ...(options.headers || {}),
        },
        ...options,
    });

    if (response.status === 401 && !retry) {
        try {
            await refresh_token();
            return apiFetch(endpoint, options, true);
        } catch (refreshError) {
            window.location.href = "/login";
            throw refreshError;
        }
    }

    if (!response.ok) {
        throw new Error("Request failed");
    }

    return response.json();
}

export const get_user_data = async (username) => {
    return await apiFetch(`/user_data/${username}/`);
};

export const refresh_token = async () => {
    return await apiFetch("/token/refresh/", {
        method: "POST",
    });
};

export async function login_user(username, password) {
    return await apiFetch("/token/", {
        method: "POST",
        body: JSON.stringify({ username, password }),
    });
}
