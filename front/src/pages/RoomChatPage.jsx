import React, {useEffect, useState, useRef} from 'react';
import { useParams } from 'react-router-dom';

import ChatInput from '../components/ChatInput';

function ServerChatPage (){

        const {roomId} = useParams();
        const [messages, setMessages] = useState([]);
        const ws = useRef(null)

        useEffect(() => {
            ws.current = new WebSocket(`ws://127.0.0.1:8000/ws/chat/${roomId}/`)

            ws.current.onopen = () => {
                console.log("WebSocket connected")
            };

            ws.current.onmessage = (event) => {
                const data = JSON.parse(event.data);
                console.log('Recieved: ', data);
                setMessages(prev => [...prev, data.message]);
            };

            ws.current.onclose = () => {
                console.log('WebSocket disconnected')
            }

            ws.current.onerror = (err) => {
                console.error('WebSocket error: ', err);
            };

            return () => ws.current.close();
        }, [roomId]);
    return (
        <>
            <h3>Connected: {roomId}</h3>
            <div>
                <ul>
                    {messages.map((message, index) => (
                        <li key={index}>{message}</li>
                    ))}
                </ul>
            </div>
            <ChatInput ws={ws} roomId={roomId}/>
        </>
    )
}

export default ServerChatPage