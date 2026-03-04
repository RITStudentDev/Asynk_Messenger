export async function login (username, password){

    //const BASE_URL = 'http://localhost:8000/'

    try {
        const response = await fetch( "http://localhost:8000/loging", {
            method: "POST",
            headers: {
                "Content-Type" : "application/json",
            },
            credentials: "include",
            body: JSON.stringify({
                username: username,
                password: password,
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