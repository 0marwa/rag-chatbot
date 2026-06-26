export const metadata = {
  title: 'rag-chatbot',
}

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <head>
        <style>{`@keyframes blink { 0%, 100% { opacity: 1 } 50% { opacity: 0 } }`}</style>
      </head>
      <body style={{ margin: 0, fontFamily: 'monospace', background: '#1a1a1a', color: '#d0d0d0' }}>
        {children}
      </body>
    </html>
  )
}
