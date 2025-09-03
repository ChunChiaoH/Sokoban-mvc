# Sokoban Project Structure

## 📁 Directory Organization

```
Sokoban-mvc/
├── 📁 client/                    # Frontend JavaScript Application
│   └── index.html               # Main game (sokoban_refactored.html)
├── 📁 server/                   # Backend Python API  
│   ├── app.py                   # Flask web server (web_app.py)
│   ├── model.py                 # Game logic and entities
│   ├── ai_solver.py             # BFS/DFS solving algorithms  
│   ├── constants.py             # Game constants and configuration
│   └── utils.py                 # Utility functions
├── 📁 legacy/                   # Old versions (for reference)
│   ├── sokoban_js.html          # Original JavaScript draft
│   ├── templates/               # Old Flask templates
│   ├── text_game.py             # Command-line version
│   ├── graphical_game.py        # Desktop GUI version
│   ├── controller.py            # MVC controller (desktop)
│   └── view.py                  # MVC view (desktop)
├── 📁 games/                    # Room/level data files
│   └── default/                 # Default room pack
├── 📁 images/                   # Game assets and screenshots
├── 📁 __pycache__/              # Python cache (can be deleted)
├── 📁 .git/                     # Git repository data
├── 📄 README.md                 # Project documentation
├── 📄 DEVELOPMENT_LOG.md        # Development history
├── 📄 requirements.txt          # Python dependencies
└── 📄 test_model.py             # Unit tests
```

## 🎯 Current Active Files

### Client-Side (Pure JavaScript)
- **`client/index.html`** - Complete standalone game
  - Instant gameplay (no server required)
  - Built-in BFS solver for hints
  - Professional architecture with proper separation of concerns

### Server-Side (Python Flask)  
- **`server/app.py`** - Flask API server
  - Room generation endpoints (future)
  - Advanced AI features (future)
  - Analytics and player data (future)
- **`server/model.py`** - Core game logic
- **`server/ai_solver.py`** - Advanced solving algorithms

## 🚀 How to Run

### Client-Only Version (Recommended)
```bash
# Just open in browser - no server needed!
open client/index.html
```

### Full-Stack Version (Future)
```bash
# Start Python server
cd server
python app.py

# Then open client/index.html in browser
# Client will call server APIs for advanced features
```

## 📋 Development Status

✅ **Completed:**
- Pure JavaScript game engine  
- Professional code architecture
- BFS solver for basic hints
- Clean project organization

🔄 **Next Steps:**
- Server-side room generation
- Advanced AI algorithms in Python
- Integration between client and server

## 🗂️ File Purposes

| File | Purpose | Status |
|------|---------|---------|
| `client/index.html` | Main game application | ✅ Active |
| `server/app.py` | Flask API server | 🔄 Future enhancement |
| `server/model.py` | Game logic library | ✅ Ready |
| `server/ai_solver.py` | Advanced AI algorithms | ✅ Ready |
| `legacy/*` | Old versions | 📦 Archived |