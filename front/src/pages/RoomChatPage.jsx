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
            const data = JSON.parse(event.data)
            setMessages(prev => [...prev, { content: data.message }])
        };

        ws.current.onclose = () => {
            console.log('WebSocket disconnected')
        }

        ws.current.onerror = (err) => {
            console.error('WebSocket error: ', err);
        };

        return () => ws.current.close();
    }, [roomId]);

    useEffect(() => {
        const fetchMessages = async () => {
            const response = await fetch(`http://localhost:8000/rooms/${roomId}/messages/`, {
                credentials: 'include'
            })
            const data = await response.json()
            setMessages(data.messages)
        }
        fetchMessages()
    }, [roomId])
        
    return (
        <>
            <h3>Connected: {roomId}</h3>
            <div>
                <ul>
                    {messages.map((message, index) => (
                        <li key={index}>{message.content}</li>
                    ))}
                </ul>
            </div>
            <ChatInput ws={ws} roomId={roomId}/>
        </>
    )
}

export default ServerChatPage