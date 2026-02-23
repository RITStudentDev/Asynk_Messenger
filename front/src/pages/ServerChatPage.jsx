import React, {useEffect, useState, useRef} from 'react';
import { useParams } from 'react-router-dom';

function ServerChatPage (){

        const { roomName} = useParams();
        const [messages, setMessages] = useState([]);
        const ws = useRef(null)

        useEffect(() => {
            ws.current = new WebSocket(`ws://localhost:8000/ws/chat/${roomName}/`)

            ws.current.onopen = () => {
                console.log("WebSocket connected")
            };

            ws.current.onmessage = (event) => {
                const data = JSON.parse(event.data);
                console.log('Recieved: ', data);
                setMessages(prev => [...prev, data.message]);
            };

            ws.onclose = () => {
                console.log('WebSocket disconnected')
            }

            ws.onerror = (err) => {
                console.error('WebSocket error: ', err);
            };

            return () => ws.current.close();
        }, [roomName]);
    return (
        <>
            <h1>Chat Server Index</h1>
            <h3>Connected: {roomName}</h3>
        </>
        
    )
}

export default ServerChatPage