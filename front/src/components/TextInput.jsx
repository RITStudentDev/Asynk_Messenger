import '../styles/TextInput.css'
import { useState } from 'react'

function TextInput(props){
    const [focused, setFocused] = useState(false)
    const [filled, setFilled] = useState(false)

    const handleFocus = () => { setFocused(true) }
    const handleBlur = () => { setFocused(false) }
    const handleInput = (e) => {
        if (e.length > 0){
            setFilled(true)
        }
        else {setFilled(false)}
    }

    return(
        <div className="input-container">
            <div className={`focus-bar ${(focused || filled) ? "active" : ""}`}></div>

            <input
                placeholder={props.placeholder}
                type={props.type}
                onFocus={handleFocus}
                onBlur={handleBlur}
                onInput={handleInput}
            />
        </div>
    )
}
export default TextInput