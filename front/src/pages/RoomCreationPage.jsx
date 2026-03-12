import { useState, useEffect } from "react"
import { useNavigate } from "react-router-dom"
import HubSideBar from '../components/HubSideBar.jsx'
import '../styles/RoomCreationPage.css'

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
        <div className="rcp">
            <HubSideBar/>
            <div className="creation-container">
                <input 
                    className="room-name-input"
                    placeholder="Enter a room name"
                    value={roomName}
                    onChange={(e) => setRoomName(e.target.value)}
                ></input>
                <textarea
                    className="room-bio-input"
                    placeholder="Write a description"
                    value={bio}
                    onChange={(e) => setBio(e.target.value)}
                ></textarea>
                <button className="create-button"onClick={createRoom}>Create</button>
            </div>
        </div>
    )
}
export default RoomCreationPage