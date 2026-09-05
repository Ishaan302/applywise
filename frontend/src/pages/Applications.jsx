// page where the user can view, add, and update job applications.
import { useState, useEffect } from 'react'
import client from '../api/client'

const STATUSES = ["Saved", "Applied", "OA", "Interview", "Offer", "Rejected", "Withdrawn"]

function ApplicationForm({ onAdded }) {
  const [form, setForm] = useState({ company: '', role: '', location: '', source: '', job_url: '' })
  const [submitting, setSubmitting] = useState(false)

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setSubmitting(true)
    try {
      await client.post('/applications', form)
      setForm({ company: '', role: '', location: '', source: '', job_url: '' })
      onAdded()
    } catch (err) {
      console.error(err)
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="grid grid-cols-2 gap-3 bg-white border rounded-lg p-4 mb-6">
      <input name="company" placeholder="Company" value={form.company} onChange={handleChange} required className="border p-2 rounded" />
      <input name="role" placeholder="Role" value={form.role} onChange={handleChange} required className="border p-2 rounded" />
      <input name="location" placeholder="Location" value={form.location} onChange={handleChange} className="border p-2 rounded" />
      <input name="source" placeholder="Source (LinkedIn, Naukri...)" value={form.source} onChange={handleChange} className="border p-2 rounded" />
      <input name="job_url" placeholder="Job URL" value={form.job_url} onChange={handleChange} className="border p-2 rounded col-span-2" />
      <button type="submit" disabled={submitting} className="bg-blue-600 text-white p-2 rounded col-span-2">
        {submitting ? 'Adding...' : 'Add Application'}
      </button>
    </form>
  )
}

function ApplicationRow({ app, onStatusChange }) {
  return (
    <tr className="border-b">
      <td className="p-2">{app.company}</td>
      <td className="p-2">{app.role}</td>
      <td className="p-2">{app.source || '—'}</td>
      <td className="p-2">
        <select
          value={app.status}
          onChange={(e) => onStatusChange(app.id, e.target.value)}
          className="border rounded p-1 text-sm"
        >
          {STATUSES.map((s) => <option key={s} value={s}>{s}</option>)}
        </select>
      </td>
    </tr>
  )
}

function Applications() {
  const [apps, setApps] = useState([])
  const [loading, setLoading] = useState(true)

  const fetchApps = () => {
    setLoading(true)
    client.get('/applications')
      .then((res) => setApps(res.data))
      .catch((err) => console.error(err))
      .finally(() => setLoading(false))
  }

  useEffect(() => {
    fetchApps()
  }, [])

  const handleStatusChange = async (id, newStatus) => {
    const previous = apps
    setApps(apps.map((a) => (a.id === id ? { ...a, status: newStatus } : a)))
    try {
      await client.patch(`/applications/${id}`, { status: newStatus })
    } catch (err) {
      console.error(err)
      setApps(previous)
    }
  }

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">Applications</h1>
      <ApplicationForm onAdded={fetchApps} />

      {loading ? (
        <p>Loading...</p>
      ) : apps.length === 0 ? (
        <p className="text-gray-500">No applications yet — add your first one above.</p>
      ) : (
        <table className="w-full bg-white border rounded-lg">
          <thead>
            <tr className="border-b text-left text-sm text-gray-500">
              <th className="p-2">Company</th>
              <th className="p-2">Role</th>
              <th className="p-2">Source</th>
              <th className="p-2">Status</th>
            </tr>
          </thead>
          <tbody>
            {apps.map((app) => (
              <ApplicationRow key={app.id} app={app} onStatusChange={handleStatusChange} />
            ))}
          </tbody>
        </table>
      )}
    </div>
  )
}

export default Applications