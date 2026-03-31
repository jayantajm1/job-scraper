import { useCallback, useEffect, useMemo, useState } from 'react'
import './App.css'

const API_BASE = import.meta.env.VITE_API_BASE || ''

function api(path) {
  return `${API_BASE}${path}`
}

function formatDate(value) {
  if (!value) {
    return 'n/a'
  }

  const date = new Date(value)
  if (Number.isNaN(date.getTime())) {
    return value
  }

  return date.toLocaleString()
}

function taskStatusClass(status) {
  if (status === 'completed') {
    return 'is-success'
  }
  if (status === 'failed') {
    return 'is-error'
  }
  return 'is-running'
}

function App() {
  const [files, setFiles] = useState([])
  const [selectedFile, setSelectedFile] = useState('')
  const [jobs, setJobs] = useState([])
  const [tasks, setTasks] = useState([])
  const [maxApplications, setMaxApplications] = useState(20)
  const [applyMode, setApplyMode] = useState('auto')
  const [isLoadingJobs, setIsLoadingJobs] = useState(false)
  const [message, setMessage] = useState('')

  const latestTask = useMemo(() => tasks[0], [tasks])

  const loadFiles = useCallback(async () => {
    const response = await fetch(api('/api/files'))
    const payload = await response.json()
    const incoming = payload.files || []
    setFiles(incoming)

    if (!selectedFile && incoming.length > 0) {
      setSelectedFile(incoming[0].name)
    }
  }, [selectedFile])

  const loadTasks = useCallback(async () => {
    const response = await fetch(api('/api/tasks'))
    const payload = await response.json()
    setTasks(payload.tasks || [])
  }, [])

  const loadJobs = useCallback(async (fileName) => {
    if (!fileName) {
      setJobs([])
      return
    }

    setIsLoadingJobs(true)
    setMessage('')

    try {
      const response = await fetch(api(`/api/jobs?file=${encodeURIComponent(fileName)}&limit=120`))
      const payload = await response.json()

      if (!response.ok) {
        throw new Error(payload.error || 'Could not load jobs')
      }

      setJobs(payload.jobs || [])
    } catch (error) {
      setMessage(error.message)
      setJobs([])
    } finally {
      setIsLoadingJobs(false)
    }
  }, [])

  async function startScrape() {
    setMessage('Starting scraper task...')
    const response = await fetch(api('/api/scrape'), { method: 'POST' })
    const payload = await response.json()

    if (!response.ok) {
      setMessage(payload.error || 'Failed to start scraper')
      return
    }

    setMessage(`Scraper started: ${payload.id}`)
    await loadTasks()
  }

  async function startApply() {
    if (!selectedFile) {
      setMessage('Select an Excel file first.')
      return
    }

    setMessage('Starting apply task...')
    const endpoint = applyMode === 'auto' ? '/api/auto-apply' : '/api/apply'
    const response = await fetch(api(endpoint), {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        file: selectedFile,
        mode: applyMode,
        maxApplications,
      }),
    })
    const payload = await response.json()

    if (!response.ok) {
      setMessage(payload.error || 'Failed to start apply task')
      return
    }

    setMessage(`Apply task started: ${payload.id}`)
    await loadTasks()
  }

  async function applyAllJobs() {
    if (!selectedFile) {
      setMessage('Select an Excel file first.')
      return
    }

    if (!window.confirm('Mark ALL jobs in this file as applied? This cannot be undone.')) {
      return
    }

    setMessage('Applying to all jobs...')

    try {
      const response = await fetch(api('/api/apply-all'), {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ file: selectedFile }),
      })
      const payload = await response.json()

      if (!response.ok) {
        setMessage(payload.error || 'Failed to apply to all jobs')
        return
      }

      setMessage(`✅ Successfully applied to ${payload.appliedCount} jobs at ${new Date(payload.timestamp).toLocaleTimeString()}`)

      // Refresh to show updated statuses
      await loadJobs(selectedFile)
    } catch (error) {
      setMessage(`Error applying to all jobs: ${error.message}`)
    }
  }

  useEffect(() => {
    loadFiles().catch((error) => setMessage(error.message))
    loadTasks().catch((error) => setMessage(error.message))
  }, [loadFiles, loadTasks])

  useEffect(() => {
    loadJobs(selectedFile).catch((error) => setMessage(error.message))
  }, [selectedFile, loadJobs])

  useEffect(() => {
    const timer = setInterval(() => {
      loadTasks().catch(() => null)
      loadFiles().catch(() => null)
    }, 3000)

    return () => clearInterval(timer)
  }, [loadFiles, loadTasks])

  return (
    <div className="app-container">
      <header className="app-header">
        <div className="header-content">
          <div className="logo-section">
            <h1>💼 Job Scraper Assistant</h1>
            <p>Automated job discovery & application tracking</p>
          </div>
        </div>
      </header>

      <main className="app-shell">
        <section className="hero-panel">
          <p className="eyebrow">job automation cockpit</p>
          <h1>.NET Job Scraper Control Room</h1>
          <p className="hero-copy">
            Run scraping, launch apply flows, and inspect generated listings from one place.
            Your existing Python scripts stay unchanged under the hood.
          </p>
          <div className="hero-actions">
            <button className="btn btn-solid" onClick={startScrape}>
              Start Scraping
            </button>
            <button className="btn btn-outline" onClick={() => loadFiles()}>
              Refresh Files
            </button>
          </div>
        </section>

        <section className="control-grid">
          <article className="card">
            <h2>Application Runner</h2>
            <label>
              Excel file
              <select value={selectedFile} onChange={(event) => setSelectedFile(event.target.value)}>
                {files.length === 0 && <option value="">No files found</option>}
                {files.map((file) => (
                  <option key={file.name} value={file.name}>
                    {file.name}
                  </option>
                ))}
              </select>
            </label>
            <label>
              Mode
              <select value={applyMode} onChange={(event) => setApplyMode(event.target.value)}>
                <option value="auto">Auto</option>
                <option value="interactive">Interactive (terminal prompts)</option>
              </select>
            </label>
            <label>
              Max applications
              <input
                type="number"
                min="1"
                max="500"
                value={maxApplications}
                onChange={(event) => setMaxApplications(Number(event.target.value))}
              />
            </label>
            <button className="btn btn-solid" onClick={startApply}>
              Start Apply Task
            </button>
            <button className="btn btn-success" onClick={applyAllJobs}>
              ✅ Apply to All Jobs
            </button>
          </article>

          <article className="card">
            <h2>Task Monitor</h2>
            {latestTask ? (
              <div className={`task-pill ${taskStatusClass(latestTask.status)}`}>
                <strong>{latestTask.name}</strong>
                <span>{latestTask.status}</span>
                <small>{formatDate(latestTask.startedAt)}</small>
              </div>
            ) : (
              <p className="muted">No tasks yet.</p>
            )}

            <div className="task-list">
              {tasks.slice(0, 6).map((task) => (
                <div key={task.id} className="task-row">
                  <div>
                    <strong>{task.name}</strong>
                    <p>{task.command.join(' ')}</p>
                  </div>
                  <span className={taskStatusClass(task.status)}>{task.status}</span>
                </div>
              ))}
            </div>

            {latestTask?.output && (
              <details>
                <summary>Latest task output</summary>
                <pre>{latestTask.output}</pre>
              </details>
            )}
          </article>
        </section>

        {message && <p className="message">{message}</p>}

        <section className="card jobs-card">
          <div className="jobs-header">
            <h2>Jobs Preview</h2>
            <span>{isLoadingJobs ? 'Loading...' : `${jobs.length} rows`}</span>
          </div>

          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>No.</th>
                  <th>Title</th>
                  <th>Company</th>
                  <th>Location</th>
                  <th>Source</th>
                  <th>Posted Date</th>
                  <th>Applied Date</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {jobs.map((job, index) => (
                  <tr key={`${job['No.'] || index}-${job['Job Title'] || 'job'}`}>
                    <td>{job['No.'] || index + 1}</td>
                    <td>{job['Job Title'] || 'n/a'}</td>
                    <td>{job.Company || 'n/a'}</td>
                    <td>{job.Location || 'n/a'}</td>
                    <td>{job.Source || 'n/a'}</td>
                    <td>{formatDate(job['Posted Date'])}</td>
                    <td>{formatDate(job['Applied DateTime'])}</td>
                    <td>{job['Apply Status'] || 'Not Applied'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>
      </main>

      <footer className="app-footer">
        <div className="footer-content">
          <div className="footer-section">
            <h3>About</h3>
            <p>Job Scraper Assistant helps you discover and track job applications efficiently across multiple job sources.</p>
          </div>

          <div className="footer-section">
            <h3>Quick Links</h3>
            <ul>
              <li><a href="#" onClick={() => setMessage('Feature coming soon!')}>Documentation</a></li>
              <li><a href="#" onClick={() => setMessage('Feature coming soon!')}>Support</a></li>
              <li><a href="#" onClick={() => setMessage('Feature coming soon!')}>FAQ</a></li>
            </ul>
          </div>

          <div className="footer-section">
            <h3>Connect</h3>
            <div className="social-links">
              <a href="https://github.com/jayantajm1" target="_blank" rel="noopener noreferrer" title="GitHub">
                <span>🐙 GitHub</span>
              </a>
              <a href="https://linkedin.com/in/mardijm" target="_blank" rel="noopener noreferrer" title="LinkedIn">
                <span>💼 LinkedIn</span>
              </a>
              <a href="https://x.com/jayantajm1" target="_blank" rel="noopener noreferrer" title="X">
                <span>𝕏 X</span>
              </a>
              <a href="https://instagram.com/hikerjayanta" target="_blank" rel="noopener noreferrer" title="Instagram">
                <span>📸 Instagram</span>
              </a>
              <a href="https://facebook.com/hikerjayanta" target="_blank" rel="noopener noreferrer" title="Facebook">
                <span>📘 Facebook</span>
              </a>
              <a href="mailto:jayantaofficial84@gmail.com" title="Email">
                <span>📧 Email</span>
              </a>
            </div>
          </div>
        </div>

        <div className="footer-bottom">
          <p>&copy; 2026 Job Scraper Assistant. All rights reserved.</p>
          <p>Built with ❤️ | <a href="#">Privacy Policy</a> | <a href="#">Terms of Service</a></p>
        </div>
      </footer>
    </div>
  )
}

export default App
