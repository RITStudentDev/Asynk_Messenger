import { getCookie } from "./user";

const BASE_URL = import.meta.env.VITE_API_URL;

// Adds specified user to current room
export async function add_to_room (contact) {
/*
Takes a user contact as an input ands the user with that contact to 
the current room defined by room ID in the URL
*/
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

export async function get_current_room () {
    const roomId = window.location.pathname.split("/")[2];
    try{
        const res = await fetch(`${BASE_URL}rooms/${roomId}`, {
            method: "GET",
            credentials: 'include'
        })
        const data = await res.json()
        return data.roomId
    } catch (err){
        throw err
    }
}

export async function get_room_channels (){
    const roomId = window.location.pathname.split("/")[2];
    if(!roomId) return null
    const roomData = await get_current_room()
    try {
        const channelRes = await fetch(`${BASE_URL}rooms/${roomId}/channels/`, {
            credentials: 'include'
        })

        const channelData = await channelRes.json()
        return channelData
    } catch (err) { throw err }
}