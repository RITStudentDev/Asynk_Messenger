import { useState } from 'react'

function ImageUpload() {
    const [preview, setPreview] = useState(null)
    const [file, setFile] = useState(null)

    const handleChange = (e) => {
        const selected = e.target.files[0]
        if (!selected) return

        if (!selected.type.startsWith('image/')) {
            alert('Please select an image file')
            return
        }

        setFile(selected)
        setPreview(URL.createObjectURL(selected))
    }

    const handleUpload = async () => {
        if (!file) return

        const formData = new FormData()
        formData.append('image', file)

        const response = await fetch('http://localhost:8000/upload/', {
            method: 'POST',
            credentials: 'include',
            body: formData
        })
        const data = await response.json()
        console.log(data)
    }

    return (
        <div>
            <input
                type="file"
                accept="image/*"
                onChange={handleChange}
            />
            {preview && (
                <img src={preview} alt="preview" style={{ width: '100px', height: '100px', objectFit: 'cover' }} />
            )}
            <button onClick={handleUpload}>Upload</button>
        </div>
    )
}

export default ImageUpload