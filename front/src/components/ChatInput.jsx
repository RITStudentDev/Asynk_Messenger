import { useState, useEffect } from 'react'

function ChatInput({ws, roomId}) {
    const [content, setContent] = useState('')
    const [currentUser, setCurrentUser] = useState(null)

    useEffect(() => {
        const fetchUser = async () => {
            const response = await fetch('http://localhost:8000/users/me/', {
                credentials: 'include'
            })
            const data = await response.json()
            setCurrentUser(data)
        }
        fetchUser()
    }, [])

    const sendMessage = async () => {
        if (!content) return

        ws.current.send(JSON.stringify({
            message: content,
            sender_username: currentUser?.username,
            timestamp: new Date().toISOString()
        }))

        await fetch('http://localhost:8000/messages/', {
            method: 'POST',
            credentials: 'include',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                room: roomId,
                content: content
            })
        })

        setContent('')
    }

    return (
        <div>
            <input
                type="text"
                value={content}
                onChange={(e) => setContent(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
                placeholder="Type a message..."
            />
            <button onClick={sendMessage}>Send</button>
        </div>
    )
}

export default ChatInput