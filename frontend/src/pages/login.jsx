import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import client from '../api/client'

function Login() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    try {
      const params = new URLSearchParams()
      params.append('username', email)
      params.append('password', password)

      const res = await client.post('/auth/login', params)
      localStorage.setItem('token', res.data.access_token)
      navigate('/dashboard')
    } catch (err) {
      setError('Invalid email or password')
    }
  }

  return (
    <div className="max-w-sm mx-auto mt-20 p-6 border rounded-lg">
      <h1 className="text-2xl font-bold mb-4">Log In</h1>
      <form onSubmit={handleSubmit} className="flex flex-col gap-3">
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="border p-2 rounded"
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="border p-2 rounded"
        />
        {error && <p className="text-red-600 text-sm">{error}</p>}
        <button type="submit" className="bg-blue-600 text-white p-2 rounded">
          Log In
        </button>
      </form>
    </div>
  )
}

export default Login