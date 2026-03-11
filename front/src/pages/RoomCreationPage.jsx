import { useState, useEffect } from "react"
import { useNavigate } from "react-router-dom"

function RoomCreationPage (){
    const [roomName, setRoomName] = useState('')
    const [bio, setBio] = useState('')
    const navigate = useNavigate()
    
    const createRoom = async () => {
        if (!roomName) return

        const response = await fetch('http://localhost:8000/rooms/', {
            method: 'POST',
            credentials: 'include',
            headers: { 'Content-Type': 'application/json'},
            body: JSON.stringify({roomName, bio})
        })
        const data = await response.json()
        if (response.ok){navigate(`/chat/${data.roomId}`)}
    }

    return(
        <>
            <input 
                className="room-name-input"
                placeholder="Enter a room name"
                value={roomName}
                onChange={(e) => setRoomName(e.target.value)}
            ></input>
            <input
                className="room-bio-input"
                placeholder="Write a description"
                value={bio}
                onChange={(e) => setBio(e.target.value)}
            ></input>
            <button onClick={createRoom}>Create</button>
        </>
    )
}
export default RoomCreationPage