import "../styles/HubPage.css"

import HubSideBar from "../components/HubSideBar"
import RoomProfile from "../components/RoomProfile"

function HubPage (){

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
                    <RoomProfile/>
                    <RoomProfile/>
                    <RoomProfile/>
                    <RoomProfile/>
                    <RoomProfile/>
                    <RoomProfile/>
                </div>
            </div>
        </div>
    )
}
export default HubPage