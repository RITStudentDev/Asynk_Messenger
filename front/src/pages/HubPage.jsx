import "../styles/HubPage.css"

import HubSideBar from "../components/HubSideBar"
import RoomProfile from "../components/RoomProfile"

function HubPage (){

    return(
        <div className="page">
            <HubSideBar/>
            <div className="room-container">
                <RoomProfile/>
                <RoomProfile/>
                <RoomProfile/>
            </div>
        </div>
    )
}
export default HubPage