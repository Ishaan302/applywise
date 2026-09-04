import { useState, useEffect } from 'react'
import client from '../api/client'

function StatCard({ label, value }) {
  return (
    <div className="bg-white border rounded-lg p-4 shadow-sm">
      <p className="text-sm text-gray-500">{label}</p>
      <p className="text-2xl font-bold">{value}</p>
    </div>
  )
}

function Dashboard() {
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    client.get('/analytics/stats')
      .then((res) => setStats(res.data))
      .catch((err) => console.error(err))
      .finally(() => setLoading(false))
  }, [])

  const handleLogout = () => {
    localStorage.removeItem('token')
    window.location.href = '/login'
  }

  if (loading) return <p className="p-6">Loading...</p>
  if (!stats) return <p className="p-6">Couldn't load stats.</p>

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">Dashboard</h1>
        <button onClick={handleLogout} className="text-sm text-red-600">
          Log out
        </button>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <StatCard label="Total Applications" value={stats.total_applications} />
        <StatCard label="Response Rate" value={`${stats.response_rate}%`} />
        <StatCard label="Interview Rate" value={`${stats.interview_conversion_rate}%`} />
        <StatCard label="Offer Rate" value={`${stats.offer_rate}%`} />
      </div>
    </div>
  )
}


export default Dashboard