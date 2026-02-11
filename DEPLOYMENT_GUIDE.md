# OpenLiveCaption Deployment Guide

**Quick Start**: Get OpenLiveCaption running and share it with others in minutes!

## 🚀 Option 1: Run From Source (Fastest - Works Now!)

This is the easiest way to get started and share with technical users.

### For You (Setup Once)

```bash
# 1. Make sure you're in the project directory
cd C:\Users\acer\OpenLiveCaption

# 2. Install dependencies (if not already done)
pip install -r requirements.txt

# 3. Run the application
python Main.py
```

### For Others (Share These Instructions)

**Installation Instructions:**

1. **Install Python 3.10 or later**
   - Download from: https://www.python.org/downloads/
   - During installation, check "Add Python to PATH"

2. **Download OpenLiveCaption**
   - Download ZIP from: [Your GitHub/Google Drive link]
   - Extract to a folder (e.g., `C:\OpenLiveCaption`)

3. **Install Dependencies**
   ```bash
   cd C:\OpenLiveCaption
   pip install -r requirements.txt
   ```

4. **Run the Application**
   ```bash
   python Main.py
   ```

**That's it!** The application will launch with a control window and caption overlay.

---

## 🌐 Option 2: Share via GitHub (Recommended)

This is the best way to share open-source software.

### Step 1: Create GitHub Repository

1. Go to https://github.com and sign in (or create account)
2. Click the "+" icon → "New repository"
3. Name: `OpenLiveCaption`
4. Description: `Free, open-source live captions for everyone - 47 languages supported`
5. Make it Public
6. Click "Create repository"

### Step 2: Upload Your Code

**Option A: Using GitHub Desktop (Easiest)**

1. Download GitHub Desktop: https://desktop.github.com/
2. Install and sign in
3. File → Add Local Repository → Select your OpenLiveCaption folder
4. Click "Publish repository"
5. Done!

**Option B: Using Command Line**

```bash
cd C:\Users\acer\OpenLiveCaption

# Initialize git (if not already done)
git init
git add .
git commit -m "OpenLiveCaption v2.0.0 - Complete implementation with 47 languages"

# Connect to GitHub (replace Ruthhilary)
git remote add origin https://github.com/Ruthhilary/OpenLiveCaption.git
git branch -M main
git push -u origin main
```

### Step 3: Create a Release

1. Go to your repository on GitHub
2. Click "Releases" → "Create a new release"
3. Tag version: `v2.0.0`
4. Release title: `OpenLiveCaption v2.0.0 - 47 Languages`
5. Description: Copy from `RELEASE_NOTES.md`
6. Click "Publish release"

### Step 4: Share!

Your link: `https://github.com/Ruthhilary/OpenLiveCaption`

People can:
- Click "Code" → "Download ZIP"
- Follow installation instructions in README.md
- Star the repository
- Report issues
- Contribute improvements

---

## 📦 Option 3: Build Standalone Executable (Advanced)

This creates a single .exe file that doesn't require Python installation.

### Prerequisites

```bash
pip install pyinstaller
```

### Build Command

```bash
# Clean build
python build.py --clean

# This creates:
# - dist/OpenLiveCaption.exe (standalone executable)
```

**Note**: Building takes 10-20 minutes and creates a ~250MB file.

### Share the Executable

1. Upload `dist/OpenLiveCaption.exe` to:
   - Google Drive
   - Dropbox
   - Your website
   - GitHub Release

2. Share the download link

3. Users just download and run - no installation needed!

---

## 🌍 Option 4: Deploy Web Version

If you want a web-based version that runs in browsers.

### Local Testing

```bash
python server.py
```

Then visit: http://localhost:5000

### Deploy to Cloud (Free Options)

**Render.com (Recommended - Free tier)**

1. Go to https://render.com
2. Sign up with GitHub
3. New → Web Service
4. Connect your OpenLiveCaption repository
5. Settings:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python server.py`
6. Click "Create Web Service"
7. Your app will be live at: `https://your-app.onrender.com`

**Heroku (Free tier available)**

```bash
# Install Heroku CLI
# Then:
heroku login
heroku create openlivecaption
git push heroku main
```

Your app: `https://openlivecaption.herokuapp.com`

**Railway.app (Free tier)**

1. Go to https://railway.app
2. Sign in with GitHub
3. New Project → Deploy from GitHub
4. Select OpenLiveCaption repository
5. Done! Auto-deploys on every commit

---

## 📱 Option 5: Share Download Page

I've created a beautiful download page for you at `web/download.html`.

### View It Locally

```bash
# Open in browser
start web/download.html
```

### Host It Online

**Option A: GitHub Pages (Free)**

1. Push code to GitHub
2. Go to repository Settings → Pages
3. Source: Deploy from branch `main`
4. Folder: `/web`
5. Save
6. Your page: `https://Ruthhilary.github.io/OpenLiveCaption/download.html`

**Option B: Netlify (Free)**

1. Go to https://netlify.com
2. Drag and drop your `web` folder
3. Done! You get a URL like: `https://openlivecaption.netlify.app`

**Option C: Your Own Hosting**

1. Upload `web/download.html` to your web server
2. Update download links in the HTML
3. Share your URL

---

## 🎯 Recommended Path for You

Based on your setup, here's what I recommend:

### Phase 1: Immediate (Do This Now)

1. **Test the application**
   ```bash
   python Main.py
   ```

2. **Create GitHub repository**
   - Use GitHub Desktop (easiest)
   - Or use command line

3. **Share GitHub link**
   - People can download and run from source
   - Works on all platforms

### Phase 2: Next Week

1. **Build the executable**
   ```bash
   python build.py --clean
   ```

2. **Create GitHub Release**
   - Upload the .exe file
   - Add release notes

3. **Share release link**
   - Direct download for Windows users
   - No Python installation needed

### Phase 3: Future

1. **Deploy web version** (optional)
   - Use Render.com or Railway
   - Browser-based access

2. **Create download page** (optional)
   - Host on GitHub Pages or Netlify
   - Professional landing page

---

## 📋 Quick Reference

### Run Application
```bash
python Main.py
```

### Build Executable
```bash
python build.py --clean
```

### Run Web Server
```bash
python server.py
```

### Run Tests
```bash
python -m pytest -q
```

### View Download Page
```bash
start web/download.html
```

---

## 🆘 Troubleshooting

### "Python not found"
- Install Python from python.org
- Make sure "Add to PATH" was checked during installation

### "Module not found"
```bash
pip install -r requirements.txt
```

### Build takes too long
- This is normal (10-20 minutes)
- PyInstaller bundles everything into one file
- Be patient!

### Executable too large
- Normal size: 200-300MB
- Includes Python, Whisper, PyTorch, and all dependencies
- This is expected for AI applications

---

## 📞 Support

If you need help:
1. Check TROUBLESHOOTING.md
2. Check README.md
3. Open an issue on GitHub
4. Ask in GitHub Discussions

---

## 🎉 You're Ready!

You now have everything you need to:
- ✅ Run OpenLiveCaption locally
- ✅ Share it with others
- ✅ Deploy it online
- ✅ Build standalone executables

**Start with**: `python Main.py`

**Then share**: Create GitHub repository and share the link!

---

**Made with ❤️ for accessibility and inclusion**

