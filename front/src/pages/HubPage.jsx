import "../styles/HubPage.css"

import HubSideBar from "../components/HubSideBar"
import RoomProfile from "../components/RoomProfile"

function HubPage (){

    // change this to api fetch for looged user rooms
    const rooms = [
        {id: 1, name: "Group 1"},
        {id: 2, name: "Group 2"},
        {id: 3, name: "Group 3"},
        {id: 4, name: "Group 4"},
        {id: 5, name: "Group 5"},
        {id: 6, name: "Group 6"},
    ]


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