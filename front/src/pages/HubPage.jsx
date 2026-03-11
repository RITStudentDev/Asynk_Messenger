import "../styles/HubPage.css"
import { useState, useEffect } from "react"
import HubSideBar from "../components/HubSideBar"
import RoomProfile from "../components/RoomProfile"

import { get_memberships } from "../mod/user"

function HubPage (){

    const [rooms, setRooms ] = useState([])

    // change this to api fetch for looged user rooms
    useEffect(() => {
        const fetchRooms = async () => {
            const rooms = await get_memberships()
            setRooms(rooms)
        }
        fetchRooms()
    }, [])


    return(
        <div className="page">
            <HubSideBar/>
            <div className="main-view">
                <div className="head-bar">
                    <button>+</button>
                    <button>F</button>
                    <input
                        placeholder="Search"
                    ></input>
                    <button>Me</button>
                </div>
                <div className="room-container">
                    {rooms.map((room) => (
                        <RoomProfile key={room.roomId} roomId={room.roomId} roomName={room.roomName} bio={room.bio}/>
                    ))}
                </div>
            </div>
        </div>
    )
}
export default HubPage