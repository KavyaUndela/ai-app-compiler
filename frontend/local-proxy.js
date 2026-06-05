const http = require('http')
const httpProxy = require('http-proxy')

const PORT = process.env.PORT || 8080
const BACKEND = 'http://localhost:8000'
const FRONTEND = 'http://localhost:3000'

const proxy = httpProxy.createProxyServer({
  xfwd: true,
  ws: true,
  secure: false,
})

const server = http.createServer((req, res) => {
  const url = req.url || '/'
  const target = url.startsWith('/api') || url.startsWith('/docs') || url.startsWith('/openapi.json')
    ? BACKEND
    : FRONTEND

  proxy.web(req, res, { target }, (err) => {
    console.error('Proxy error:', err)
    if (!res.headersSent) {
      res.writeHead(502, { 'Content-Type': 'text/plain' })
      res.end('Bad gateway')
    }
  })
})

server.on('upgrade', (req, socket, head) => {
  const url = req.url || '/'
  const target = url.startsWith('/api') || url.startsWith('/docs') || url.startsWith('/openapi.json')
    ? BACKEND
    : FRONTEND

  proxy.ws(req, socket, head, { target }, (err) => {
    console.error('WebSocket proxy error:', err)
    socket.destroy()
  })
})

server.listen(PORT, () => {
  console.log(`Local proxy running on http://localhost:${PORT}`)
  console.log(`  /api -> ${BACKEND}`)
  console.log(`  /docs -> ${BACKEND}/docs`)
  console.log(`  / -> ${FRONTEND}`)
})
