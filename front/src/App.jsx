import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'
import './App.css'

import SignupPage from './pages/SignupPage'
import LoginPage from './pages/LoginPage'

function App() { return (
  <Router>
    <Routes>
      <Route path="/" element={<h1>rendering</h1>}/>
      <Route path="/signup" element={<SignupPage/>}/>
      <Route path="/login" element={<LoginPage/>}/>
    </Routes>
  </Router>
) } 

export default App