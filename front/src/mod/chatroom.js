import { getCookie } from "./user";

const BASE_URL = "http://localhost:8000/" ;

export async function add_to_room (contact) {
    const access_token = getCookie("access_token")
    const roomId = window.location.pathname.split("/")[2];

    const response = await fetch(`${BASE_URL}rooms/${roomId}/join/`, {
        method: "POST",
        credentials: "include",
        headers: {
            Authorization: `Bearer ${access_token}`,
            "Content-Type": "application/json"
        },
        body: JSON.stringify({"contact":contact})
    })

    if (!response.ok) throw new Error("Failed to add user to room")
    return await response.json();
}