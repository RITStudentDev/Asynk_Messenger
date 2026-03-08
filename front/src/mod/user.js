export async function login (username, password){

    const BASE_URL = "http://localhost:8000/" 
    // CXf25nXw

    try {
        const response = await fetch( `${BASE_URL}users/login/`, {
            method: "POST",
            headers: {
                "Content-Type" : "application/json",
            },
            credentials: "include",
            body: JSON.stringify({
                username: username,
                password: password
            }),
        });

        const data = await response.json()

        if (!response.ok){
            throw new Error(data.detail || "Login failed");
        }

        return data;

    } catch (error){
        throw error
    }
}

export async function get_logged_user(){
    try {
        const response = await fetch( `${BASE_URL}users/me`, {
            credentials: "include",
            headers: {
                Authorization : `Bearer ${accessToken}`
            }
        });

        if (!response.ok){
            throw new Error("Failed to fetch user");
        }

        const data = await response.json();
        return data;

    } catch (err) {
        console.log(err);
        return null
    }
}