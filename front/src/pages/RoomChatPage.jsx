import React, {useEffect, useState, useRef} from 'react';
import { useParams } from 'react-router-dom';

import '../styles/RoomChatPage.css'

import ChatInput from '../components/ChatInput';
import HubSideBar from '../components/HubSideBar'
import Message from '../components/Message';

function ServerChatPage (){

    const {roomId} = useParams();
    const [messages, setMessages] = useState([]);
    const [roomName, setRoomName] = useState("");
    const presentRef = useRef(null);
    const isInitialLoad = useRef(true);
    const ws = useRef(null);

    useEffect(() => {
        ws.current = new WebSocket(`ws://127.0.0.1:8000/ws/chat/${roomId}/`)

        ws.current.onopen = () => {
            console.log("WebSocket connected")
        };

        ws.current.onmessage = (event) => {
            const data = JSON.parse(event.data)
            setMessages(prev => [...prev, {
                content: data.content,
                sender_username: data.sender_username,
                timestamp: data.timestamp

            }])
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
            isInitialLoad.current = true;
        }
        fetchMessages()
    }, [roomId])
    
    useEffect(() => {
        if (isInitialLoad.current){
            presentRef.current?.scrollIntoView({behavior: 'instant'})
            isInitialLoad.current = false;
        } else {
            presentRef.current?.scrollIntoView({behavior: 'smooth'})
        }
    }, [messages])

    useEffect(() => {
        const fetchRoom = async () => {
            const response = await fetch(`http://localhost:8000/rooms/${roomId}/`, {
                credentials: 'include'
            })
            const data = await response.json()
            setRoomName(data.roomName)
        }
        fetchRoom()
    }, [roomId])

    return (
        <div className='chat-page'>
            <HubSideBar/>
            <div className='chat-view'>
                <h3>{roomName}</h3>
                <div className='chat-list'>
                    <ul>
                        {messages.map((message, index) => (
                            <Message
                                key={index}
                                username={message.sender_username}
                                content={message.content}
                                timestamp={message.timestamp}
                            />
                        ))}
                    </ul>
                    <div ref={presentRef}/>
                </div>
                <ChatInput ws={ws} roomId={roomId}/>
            </div>
        </div>
    )
}

export default ServerChatPage
