import React, { useState } from 'react'
import '../styles/Signup.css'
import TextInput from './TextInput.jsx'

function Login (){
    
    return(
        <div className="signup-box">
            <form onSubmit={handleSubmit}>
                <h2>Login</h2>
                <TextInput placeholder="Username" type="username"/>
                <br/>
                <TextInput placeholder="Password" type="password"/>
                <a href="#" className="login">Don't have an account</a>
                <button type='submit'>Login</button>
                {error && <p>{error}</p>}
                {error && <p>{message}</p>}
            </form>
        </div>
    )
}
export default Login