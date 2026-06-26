'use client'

import { useState, useRef, useEffect } from 'react'

const API = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export default function Home() {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [dragOver, setDragOver] = useState(false)
  const [uploadStatus, setUploadStatus] = useState(null)
  const bottomRef = useRef(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  function showStatus(msg) {
    setUploadStatus(msg)
    // clear after 4s so it doesn't sit there forever
    setTimeout(() => setUploadStatus(null), 4000)
  }

  async function uploadFile(file) {
    const ext = file.name.split('.').pop().toLowerCase()
    if (!['txt', 'md'].includes(ext)) {
      showStatus(`error: only .txt and .md files supported`)
      return
    }

    showStatus(`uploading ${file.name}...`)
    const form = new FormData()
    form.append('file', file)

    try {
      const res = await fetch(`${API}/upload`, { method: 'POST', body: form })
      const data = await res.json()
      if (!res.ok) showStatus(`error: ${data.detail}`)
      else showStatus(`${file.name} uploaded -- ${data.chunks_stored} chunks stored`)
    } catch {
      showStatus('error: could not reach backend')
    }
  }

  function handleDrop(e) {
    e.preventDefault()
    setDragOver(false)
    const file = e.dataTransfer.files[0]
    if (file) uploadFile(file)
  }

  async function handleSend(e) {
    e.preventDefault()
    const q = input.trim()
    if (!q || loading) return

    setInput('')
    setMessages(prev => [...prev, { role: 'user', text: q }])
    setLoading(true)

    try {
      const res = await fetch(`${API}/ask`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: q }),
      })
      const data = await res.json()
      if (!res.ok) {
        setMessages(prev => [...prev, { role: 'error', text: data.detail || 'something went wrong' }])
      } else {
        setMessages(prev => [...prev, { role: 'bot', text: data.answer, sources: data.sources }])
      }
    } catch {
      setMessages(prev => [...prev, { role: 'error', text: 'could not reach backend' }])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div
      style={styles.page}
      onDragOver={e => { e.preventDefault(); setDragOver(true) }}
      onDragLeave={() => setDragOver(false)}
      onDrop={handleDrop}
    >
      {/* drag overlay */}
      {dragOver && (
        <div style={styles.dropOverlay}>
          <span style={styles.dropOverlayText}>drop file to upload</span>
        </div>
      )}

      {/* header */}
      <div style={styles.header}>
        <span style={styles.headerTitle}>rag-chatbot<span style={styles.cursor}>_</span></span>
        <span style={styles.headerHint}>drag a .txt or .md file anywhere to upload</span>
      </div>

      {/* upload status */}
      {uploadStatus && (
        <div style={styles.uploadStatus}>{uploadStatus}</div>
      )}

      {/* chat area */}
      <div style={styles.chatArea}>
        {messages.length === 0 && (
          <p style={styles.placeholder}>
            {'> drop a doc, then ask a question'}
          </p>
        )}
        {messages.map((m, i) => (
          <div key={i} style={styles.messageRow}>
            <span style={{
              ...styles.prompt,
              color: m.role === 'user' ? '#f0a0b8' : m.role === 'error' ? '#e07070' : '#aaa'
            }}>
              {m.role === 'user' ? '>' : m.role === 'error' ? '!' : '$'}
            </span>
            <div style={styles.messageContent}>
              <p style={styles.text}>{m.text}</p>
              {m.sources && m.sources.length > 0 && (
                <p style={styles.sources}>
                  <span style={styles.sourcesLabel}>sources: </span>
                  {m.sources.join(', ')}
                </p>
              )}
            </div>
          </div>
        ))}
        {loading && (
          <div style={styles.messageRow}>
            <span style={{ ...styles.prompt, color: '#aaa' }}>$</span>
            <p style={{ ...styles.text, color: '#666' }}>thinking...</p>
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      {/* input */}
      <form onSubmit={handleSend} style={styles.form}>
        <span style={styles.inputPrompt}>{'>'}</span>
        <input
          style={styles.input}
          value={input}
          onChange={e => setInput(e.target.value)}
          placeholder="ask something..."
          disabled={loading}
          autoFocus
        />
        <button type="submit" style={{
          ...styles.sendBtn,
          opacity: loading || !input.trim() ? 0.4 : 1,
          cursor: loading || !input.trim() ? 'default' : 'pointer',
        }} disabled={loading || !input.trim()}>
          send
        </button>
      </form>
    </div>
  )
}

const styles = {
  page: {
    display: 'flex',
    flexDirection: 'column',
    height: '100vh',
    maxWidth: '800px',
    margin: '0 auto',
    padding: '0 24px',
    boxSizing: 'border-box',
    position: 'relative',
  },
  dropOverlay: {
    position: 'fixed',
    inset: 0,
    background: 'rgba(26, 26, 26, 0.92)',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    zIndex: 100,
    border: '2px dashed #f0a0b8',
  },
  dropOverlayText: {
    color: '#f0a0b8',
    fontSize: '18px',
    letterSpacing: '0.05em',
  },
  header: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    padding: '20px 0 14px',
    borderBottom: '1px solid #2e2e2e',
  },
  headerTitle: {
    fontSize: '15px',
    color: '#e0e0e0',
    letterSpacing: '0.03em',
  },
  cursor: {
    color: '#f0a0b8',
    animation: 'blink 1.2s step-end infinite',
  },
  headerHint: {
    fontSize: '11px',
    color: '#444',
  },
  uploadStatus: {
    fontSize: '11px',
    color: '#f0a0b8',
    padding: '6px 0',
    borderBottom: '1px solid #2e2e2e',
  },
  chatArea: {
    flex: 1,
    overflowY: 'auto',
    padding: '20px 0',
    display: 'flex',
    flexDirection: 'column',
    gap: '10px',
  },
  placeholder: {
    color: '#3a3a3a',
    fontSize: '13px',
    margin: '40px 0 0',
  },
  messageRow: {
    display: 'flex',
    gap: '12px',
    alignItems: 'flex-start',
  },
  prompt: {
    fontSize: '14px',
    lineHeight: 1.6,
    userSelect: 'none',
    flexShrink: 0,
  },
  messageContent: {
    flex: 1,
  },
  text: {
    margin: 0,
    fontSize: '14px',
    lineHeight: 1.6,
    whiteSpace: 'pre-wrap',
    color: '#d0d0d0',
  },
  sources: {
    margin: '6px 0 0',
    fontSize: '11px',
    color: '#555',
  },
  sourcesLabel: {
    color: '#f0a0b8',
  },
  form: {
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
    padding: '12px 0 24px',
    borderTop: '1px solid #2e2e2e',
  },
  inputPrompt: {
    color: '#f0a0b8',
    fontSize: '14px',
    userSelect: 'none',
  },
  input: {
    flex: 1,
    background: 'transparent',
    color: '#e0e0e0',
    border: 'none',
    outline: 'none',
    fontSize: '14px',
    caretColor: '#f0a0b8',
  },
  sendBtn: {
    background: 'transparent',
    color: '#f0a0b8',
    border: '1px solid #f0a0b8',
    borderRadius: '3px',
    padding: '6px 14px',
    fontSize: '12px',
    letterSpacing: '0.05em',
  },
}
