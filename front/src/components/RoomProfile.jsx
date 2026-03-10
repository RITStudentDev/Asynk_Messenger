import '../styles/RoomProfile.css'
import icon from '../assets/defaultRoom.png'

function RoomProfile({roomName, bio}) {
    // change later with actaul values
    //const roomName = 'Room Name';
  return (
    <div className="room-profile-container">
        <div id='name-container'>
            <h1 className='room-name'>{roomName}</h1>
        </div>
        <img src={icon} alt='icon'/>
        <div className='bio-container'>
            <p>{bio}</p>
        </div>
    </div>
  );
}

export default RoomProfile;