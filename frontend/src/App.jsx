// It controls navigation between frontend pages and decides which pages require login.

import { BrowserRouter, Routes, Route, Navigate, Link } from 'react-router-dom'
import Login from './pages/Login'
import Dashboard from './pages/Dashboard'
import Applications from './pages/Applications'
import PrivateRoute from './components/PrivateRoute'

function Nav() {
  return (
    <nav className="bg-white border-b p-4 flex gap-4">
      <Link to="/dashboard" className="font-semibold">Dashboard</Link>
      <Link to="/applications" className="font-semibold">Applications</Link>
    </nav>
  )
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/dashboard" element={<PrivateRoute><Nav /><Dashboard /></PrivateRoute>} />
        <Route path="/applications" element={<PrivateRoute><Nav /><Applications /></PrivateRoute>} />
        <Route path="*" element={<Navigate to="/login" />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App