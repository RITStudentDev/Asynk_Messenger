import "../styles/HubPage.css"

import HubSideBar from "../components/HubSideBar"
import RoomProfile from "../components/RoomProfile"

import { get_memberships } from "../mod/user"

function HubPage (){

    // change this to api fetch for looged user rooms
    const rooms = get_memberships()


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
                        <RoomProfile key={room.id} roomName={room.name}/>
                    ))}
                </div>
            </div>
        </div>
    )
}
export default HubPage