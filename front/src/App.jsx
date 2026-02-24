import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'
import './App.css'

import SignupPage from './pages/SignupPage'
import LoginPage from './pages/LoginPage'
import ServerChatPage from './pages/ServerChatPage'
import HubPage from './pages/HubPage'

function App() { return (
  <Router>
    <Routes>
      <Route path="/" element={<h1>rendering</h1>}/>
      <Route path="/signup" element={<SignupPage/>}/>
      <Route path="/login" element={<LoginPage/>}/>
      <Route path="/hub" element={<HubPage/>}/>
      <Route path="/chat/:roomName" element={<ServerChatPage/>}/>
    </Routes>
  </Router>
) } 

export default App