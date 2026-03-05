import '../styles/RoomProfile.css'
import icon from '../assets/defaultRoom.png'

function RoomProfile() {
    // change later with actaul values
    const roomName = 'Room Name';
  return (
    <div className="room-profile-container">
        <div id='name-container'>
            <h1 className='room-name'>{roomName}</h1>
        </div>
        <img src={icon} alt='icon'/>
        <div className='bio-container'>
            <p>Lorem ipsum dolor sit amet consectetur, adipisicing elit. Explicabo exercitationem quas repellendus earum? Corrupti tempore maxime, ratione ea, ab, in aliquam aspernatur amet tenetur veritatis velit nostrum accusamus aperiam reiciendis.</p>
        </div>
    </div>
  );
}

export default RoomProfile;