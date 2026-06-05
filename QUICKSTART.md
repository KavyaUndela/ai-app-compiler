# ⚡ QUICKSTART - Single Localhost

Get the entire AI Application Compiler running on **one localhost link** in **2 minutes**.

---

## 🎯 One Command Start

### Windows
```bash
run-single-localhost.bat
```

### macOS/Linux
```bash
chmod +x run-single-localhost.sh
./run-single-localhost.sh
```

### Any OS
```bash
docker compose up --build
```

---

## ✅ When Ready

Open your browser to:

### **🎉 http://localhost:8080**

That's it! Everything is there - no port confusion.

---

## 🎮 Try Sample Prompts

Click in the textarea and paste one:

### CRM System
```
Build a CRM with login, contacts management, dashboard with analytics, 
role-based access (Admin, Manager, User), and email notifications.
```

### Hospital Management
```
Create a hospital management system with patient records, doctor appointments, 
prescription management, billing, and patient portal.
```

### School ERP
```
Design a school ERP with student management, attendance tracking, class scheduling, 
grade management, and parent portal.
```

### E-commerce Store
```
Build an e-commerce platform with product catalog, shopping cart, checkout, 
payment integration, order tracking, and admin dashboard.
```

After pasting, click **"Generate Configuration"** and wait for results!

---

## 🔗 Single Localhost URLs

Everything accessible from **http://localhost:8080**:

| Component | URL |
|-----------|-----|
| **App UI** | http://localhost:8080 |
| **API Calls** | http://localhost:8080/api/* |
| **API Docs** | http://localhost:8080/docs |

---

## 📖 Explore After Generating

Click the navigation menu:

- **Pipeline** — See all 6 compilation stages
- **Validation** — Check for errors and warnings  
- **Repair** — View auto-fix suggestions
- **Runtime** — Preview generated code & forms
- **Recent** — Browse past compilations

---

## 🏗️ How It Works

Your requirement flows through 6 stages:

```
1. Intent Extraction     → Parse requirements
2. System Design        → Create architecture  
3. Schema Generation    → Build schemas
4. Validation Engine    → Check correctness
5. Repair Engine        → Fix issues
6. Runtime Simulator    → Generate preview
```

All results display instantly!

---

## 🛑 Stop Services

```bash
# Press Ctrl+C in the terminal
# Or run:
docker compose down
```

---

## 🐛 Troubleshooting

### Port 8080 Already in Use
```bash
# Find what's using it
lsof -i :8080                    # macOS/Linux
netstat -ano | findstr :8080    # Windows

# Kill it or edit docker-compose.yml to use different port
```

### Docker Not Installed
Download from: https://www.docker.com/products/docker-desktop

### Blank Page
- Press F12 (check browser console)
- Reload page (Ctrl+R)
- Check logs: `docker compose logs frontend`

### API Returns 404
```bash
# Test health:
curl http://localhost:8080/api/health

# Check logs:
docker compose logs backend
```

---

## 📚 More Documentation

| Document | Purpose |
|----------|---------|
| [SINGLE_LOCALHOST.md](SINGLE_LOCALHOST.md) | Complete single URL setup guide |
| [README_COMPLETE.md](README_COMPLETE.md) | Full feature overview |
| [API_REFERENCE.md](API_REFERENCE.md) | API endpoints reference |
| [DEPLOYMENT.md](DEPLOYMENT.md) | Production deployment |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Developer guide |
| [INDEX.md](INDEX.md) | All documentation index |

---

## Tech Stack

- **Frontend:** Next.js 15 + TypeScript + Tailwind CSS
- **Backend:** FastAPI + Python 3.12 + Pydantic v2
- **Proxy:** Nginx (single localhost router)
- **Infrastructure:** Docker + Docker Compose

---

## ✨ What You Get

✅ Complete 6-stage compiler pipeline  
✅ Natural language to architecture  
✅ Database schema generation  
✅ API endpoint design  
✅ Validation & error checking  
✅ Automated repair suggestions  
✅ Runtime preview with sample data  
✅ **All on one localhost link** 🎉
- **Deployment:** Docker Compose

---

## Getting Help

- Check application logs: `docker compose logs`
- Review [README_COMPLETE.md](README_COMPLETE.md)
- Read [API_REFERENCE.md](API_REFERENCE.md)
- See [CONTRIBUTING.md](CONTRIBUTING.md) for extending the system

---

**Ready to build? Run `docker compose up --build` or `start-local.bat`**

🎉 That's it! You're all set.
