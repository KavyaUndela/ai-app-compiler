# Single Localhost Setup

Run the entire AI Application Compiler on a **single localhost link** using Nginx reverse proxy.

## 🚀 Quick Start (One Command)

```bash
docker compose up --build
```

Then open your browser to:

### 🎯 **http://localhost:8080**

That's it! Everything is accessible from one link:
- **Frontend:** http://localhost:8080
- **API Calls:** http://localhost:8080/api/*
- **API Docs:** http://localhost:8080/docs

---

## 📊 What's Running

| Component | URL | Port |
|-----------|-----|------|
| **Full App** | http://localhost:8080 | 8080 |
| Frontend | Proxied via 8080 | - |
| Backend API | Proxied via 8080/api | - |
| Swagger Docs | http://localhost:8080/docs | 8080 |

---

## 🔄 How It Works

```
Client Request
    ↓
http://localhost:8080
    ↓
Nginx Reverse Proxy
    ↓
├─→ /api/* → Backend (port 8000)
├─→ /docs → Backend API Docs
└─→ /* → Frontend (port 3000)
```

---

## ✨ Benefits

✅ Single URL for everything  
✅ No port confusion  
✅ Production-like setup  
✅ Proper API routing  
✅ Full documentation access  

---

## 💻 Usage

### 1. Start Services
```bash
docker compose up --build
```

### 2. Open Browser
```
http://localhost:8080
```

### 3. Try a Prompt
- Click "Build a CRM" sample
- Click "Generate Configuration"
- Wait for results

### 4. Explore Pages
All pages accessible from the navigation menu:
- Home (Prompt input)
- Pipeline (6-stage view)
- Validation (Error report)
- Repair (Fix suggestions)
- Runtime (Preview)
- Recent (Compilations)

### 5. View API Docs
```
http://localhost:8080/docs
```

---

## 🔧 Configuration

### Key Files

**nginx.conf** - Reverse proxy routing
- Routes `/api` requests to backend
- Routes all other requests to frontend
- Enables WebSocket support

**docker-compose.yml** - Container orchestration
- Starts backend on internal port 8000
- Starts frontend on internal port 3000
- Runs Nginx on external port 8080

---

## 🎮 Testing

### In Browser

```
http://localhost:8080

Sample Prompts:
✓ "Build a CRM with login, contacts, dashboard"
✓ "Hospital management system"
✓ "School ERP system"
✓ "E-commerce platform"
```

### Via API (cURL)

```bash
# Generate compilation
curl -X POST http://localhost:8080/api/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Build a simple todo app"}'

# List compilations
curl http://localhost:8080/api/compilations

# Health check
curl http://localhost:8080/api/health
```

### Via JavaScript (from frontend)

```javascript
// The frontend automatically uses http://localhost:8080/api
// No configuration needed!
```

---

## 🛑 Stopping

```bash
# Stop all services
docker compose down

# Stop and remove volumes
docker compose down -v

# View logs
docker compose logs -f

# View specific service logs
docker compose logs -f backend
docker compose logs -f frontend
docker compose logs -f nginx
```

---

## 🐛 Troubleshooting

### Port 8080 Already in Use

```bash
# Find process using port
lsof -i :8080  # macOS/Linux
netstat -ano | findstr :8080  # Windows

# Kill process
kill -9 PID  # macOS/Linux
taskkill /PID PID /F  # Windows

# Or use different port - edit docker-compose.yml:
# ports:
#   - "8000:80"  # Use 8000 instead
```

### API Calls Return 404

```bash
# Check backend is running
curl http://localhost:8080/api/health

# Check Nginx routing
curl -v http://localhost:8080/api/generate

# View Nginx logs
docker compose logs nginx
```

### Frontend Shows Blank Page

```bash
# Check frontend is running
curl http://localhost:8080

# Check browser console for errors
# Open: http://localhost:8080
# Press: F12 (Developer Tools)
# Go to: Console tab

# View frontend logs
docker compose logs frontend
```

### Rebuild Needed

```bash
# Full rebuild
docker compose down -v
docker compose up --build

# Clear cache
docker system prune -a
docker compose up --build
```

---

## 📈 Performance

- **Page Load:** ~1-2 seconds
- **API Response:** ~300-500ms
- **Total Pipeline:** ~6 stages in parallel

---

## 🔐 Security Notes

For local development only. For production:
- Add HTTPS/SSL
- Implement authentication
- Configure CORS properly
- Use environment variables for secrets

---

## 📚 Next Steps

### Learn More
- [Full Documentation](README_COMPLETE.md)
- [API Reference](API_REFERENCE.md)
- [Architecture Guide](README_COMPLETE.md#-architecture)

### Extend Features
- Add database integration
- Implement authentication
- Deploy to production
- See [CONTRIBUTING.md](CONTRIBUTING.md)

### Production Deployment
- See [DEPLOYMENT.md](DEPLOYMENT.md)
- AWS, Google Cloud, Heroku supported
- Kubernetes ready

---

## ✅ What to Try

1. Open **http://localhost:8080**
2. Click a sample prompt (e.g., "Build a CRM")
3. Click "Generate Configuration"
4. Explore all 6 pages:
   - View the pipeline
   - Check validation results
   - See repair suggestions
   - Preview the runtime
   - Browse recent compilations

5. Try the API (optional):
   ```bash
   curl http://localhost:8080/docs
   ```

---

## 📞 Support

- **Quick Help:** Check [README_COMPLETE.md](README_COMPLETE.md#-troubleshooting)
- **API Issues:** See [API_REFERENCE.md](API_REFERENCE.md)
- **Setup Issues:** Review [STARTUP.md](STARTUP.md)
- **Development:** See [CONTRIBUTING.md](CONTRIBUTING.md)

---

**🎉 You're all set! Visit http://localhost:8080 now!**
