# 🐳 Install Docker Desktop

## ✅ Automatic Installation

Run this file:
```
install-docker.bat
```

It will download and start the installer.

---

## 📝 Manual Installation

### Step 1: Download
Go to: https://www.docker.com/products/docker-desktop

Click **"Download for Windows"**

### Step 2: Install
1. Run the downloaded file: `Docker Desktop Installer.exe`
2. Check both options:
   - ✅ "Install required Windows components"
   - ✅ "Add Docker Desktop to the PATH"
3. Click **Install**
4. Wait for completion (~5 minutes)

### Step 3: Restart
Restart your computer

### Step 4: Verify
Open PowerShell and run:
```bash
docker --version
```

You should see: `Docker version 24.0.x` (or similar)

---

## ✅ After Installation

In your project folder, run:
```bash
cd "C:\Users\anush\OneDrive\Desktop\AI Enginner"
docker compose up --build
```

Then open: **http://localhost:8080**

---

## ⚠️ If Installation Fails

### Check Windows Version
```bash
winver
```
Must be Windows 10/11 Pro, Enterprise, or Education (not Home)

### Enable Hyper-V
If you get a "Hyper-V" error:
1. Press `Win + R`
2. Type: `optionalfeatures.exe`
3. Check: ✅ Hyper-V
4. Click OK
5. Restart computer

### System Requirements
- **Windows:** 10/11 Pro/Enterprise/Education
- **RAM:** 4GB minimum (8GB recommended)
- **Disk Space:** 5GB free
- **CPU:** Must support virtualization

---

## 🆘 Still Not Working?

Try the **Local Setup** instead (no Docker needed):

```bash
cd "C:\Users\anush\OneDrive\Desktop\AI Enginner\backend"
python -m venv .venv
.venv\Scripts\Activate.bat
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Then in another terminal:
```bash
cd "C:\Users\anush\OneDrive\Desktop\AI Enginner\frontend"
npm install
npm run dev
```

Access via:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000/api
- API Docs: http://localhost:8000/docs

---

## 📞 Need Help?

Check: [QUICKSTART.md](QUICKSTART.md) or [STARTUP.md](STARTUP.md)
