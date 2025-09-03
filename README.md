# Sokoban Game - Full-Stack Web Application

> **🎮 Play Now:** Open `client/index.html` in your browser for instant gameplay!

A modern Sokoban puzzle game with **professional JavaScript architecture** and **Python AI backend**. Features instant client-side gameplay with optional server-side advanced AI capabilities.

![Game Demo](demo.gif)

## 🚀 Quick Start

### Option 1: Play Immediately (Client-Only)
```bash
# No setup required - just open in browser!
open client/index.html
```

### Option 2: Full-Stack with Python AI (Future)
```bash
# 1. Install Python dependencies
pip install -r requirements.txt

# 2. Start server (optional - for advanced AI features)
cd server
python app.py

# 3. Open client in browser
open client/index.html
```

## 🎮 Game Features

### Core Gameplay
- **Classic Sokoban mechanics**: Control a cat to push glass blocks onto destination spots
- **Multiple levels**: Progressive difficulty with win conditions
- **Smooth controls**: Arrow keys or WASD for movement
- **Instant response**: Zero network lag with client-side game engine

### 🤖 AI Features
- **Built-in BFS Solver**: Get hints instantly (client-side)
- **Advanced AI** (Future): Server-side complex algorithms
- **Room Generation** (Future): Procedural level creation with AI validation

## 📁 Project Structure

```
Sokoban-mvc/
├── client/           # JavaScript game (main application)  
│   └── index.html   # Complete standalone game
├── server/          # Python AI backend (future features)
│   ├── app.py       # Flask API server
│   ├── model.py     # Game logic
│   ├── ai_solver.py # Advanced algorithms
│   └── constants.py # Configuration  
├── legacy/          # Previous versions
├── games/           # Level data
└── images/          # Assets
```

## 🛠️ Architecture

### Client-Side (JavaScript)
- **Modern ES6+ Architecture** with proper separation of concerns
- **Modular Design**: GameEngine, AISolver, Renderer, UIController
- **Professional Patterns**: Namespace, error handling, configuration management
- **Performance Optimized**: Efficient canvas rendering and state management

### Server-Side (Python)
- **Flask API**: RESTful endpoints for advanced features
- **AI Algorithms**: BFS, DFS, and future ML-based solvers
- **Room Generation**: Procedural content creation with validation
- **Analytics Ready**: Player behavior tracking capabilities

## 🎯 Development Highlights

### Technical Achievements
- ✅ **Zero Network Lag**: Pure client-side game engine
- ✅ **Professional Code Quality**: SOLID principles, error handling
- ✅ **AI Integration**: Working BFS solver with hint system
- ✅ **Clean Architecture**: Modular, testable, maintainable
- ✅ **Cross-Platform**: Works in any modern browser

### AI & Algorithms
- **Breadth-First Search**: Optimal solution finding
- **State Space Analysis**: Efficient game state management  
- **Future ML Features**: Room difficulty analysis, personalized hints

## 🧪 Testing

The game includes comprehensive error handling and validation:
- Input validation and bounds checking
- Graceful failure handling for all operations
- Console logging for debugging
- Modular architecture enables easy unit testing

## 📚 Learning Outcomes

This project demonstrates:
- **Full-stack development** with JavaScript and Python
- **AI algorithm implementation** (BFS, state space search)
- **Professional code architecture** and design patterns
- **Client-server integration** planning and execution
- **Modern web development** best practices

## 🔮 Future Enhancements

- 🤖 **Advanced AI**: Machine learning based puzzle generation
- 🌐 **Multiplayer**: Real-time collaborative solving
- 📊 **Analytics**: Player performance tracking and insights
- 🎨 **Enhanced UI**: Animations, themes, and visual effects
- 📱 **Mobile Support**: Touch controls and responsive design

---

**Built with:** JavaScript (ES6+), Python 3, Flask, HTML5 Canvas  
**AI Algorithms:** BFS, DFS, State Space Search  
**Architecture:** MVC, Modular Design, RESTful APIs