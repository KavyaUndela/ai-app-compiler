import axios from 'axios'

const BASE = process.env.NEXT_PUBLIC_API_URL || ''

const client = axios.create({ baseURL: BASE, timeout: 30000 })

export async function generate(payload: { prompt: string }) {
  const r = await client.post('/generate', payload)
  return r.data
}

export async function validate(payload: { prompt: string }) {
  const r = await client.post('/validate', payload)
  return r.data
}

export async function repair(payload: { prompt: string }) {
  const r = await client.post('/repair', payload)
  return r.data
}

export async function runtimePreview(payload: { prompt: string }) {
  const r = await client.post('/runtime-preview', payload)
  return r.data
}

export async function getMetrics() {
  const r = await client.get('/metrics')
  return r.data
}

export async function getHealth() {
  const r = await client.get('/health')
  return r.data
}
