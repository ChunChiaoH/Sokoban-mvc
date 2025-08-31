# Sokoban Game with AI Solver

A classic Sokoban puzzle game implemented in Python with **Model-View-Controller architecture** and **AI solving capabilities**. Built collaboratively with AI assistance to demonstrate modern development practices.

![Game Demo](demo.gif)

## 🎮 Features

### Core Gameplay
- **Classic Sokoban mechanics**: Control a cat to push glass blocks onto destination spots
- **Multiple levels**: Progressively challenging puzzles
- **Dual interfaces**: Both graphical (Tkinter) and text-based versions
- **Smooth controls**: WASD keys or arrow keys for movement

### 🤖 AI Solver (NEW!)
- **BFS Algorithm**: Finds optimal solutions with minimal moves
- **DFS Algorithm**: Faster solving for simpler puzzles  
- **Interactive AI**: Press 'X' to watch AI solve automatically, 'H' for hints
- **Step-by-step visualization**: AI moves are animated with 1-second delays

### 🏗️ Architecture
- **MVC Pattern**: Clean separation of game logic, rendering, and input handling
- **Unified movement system**: Single source of truth for all movement controls
- **Extensible design**: Easy to add new features, levels, and AI algorithms
- **Comprehensive constants**: Centralized configuration and messaging

## 🚀 Getting Started

### Prerequisites
```bash
pip install tkinter pillow
```

### Running the Game
```bash
# Graphical version (recommended)
python graphical_game.py

# Text-based version  
python text_game.py
```

### Controls
- **WASD** or **Arrow Keys**: Move the cat
- **X**: Solve puzzle with AI (graphical version only)
- **H**: Get AI hint for next move (graphical version only)

## 🧠 AI Solver Technical Details

The AI solver uses **game state representation** and **search algorithms**:

### GameState Class
- **Immutable snapshots** of game state (cat position + glass positions)
- **Hashable states** for efficient visited-state tracking in search
- **Move simulation** without affecting actual game state

### Search Algorithms
- **Breadth-First Search (BFS)**: Guarantees optimal solution (shortest moves)
- **Depth-First Search (DFS)**: Faster for simple puzzles, depth-limited to prevent infinite loops
- **State space exploration**: Systematically tries all possible move sequences

### Integration
- **Real-time solving**: AI runs in background without blocking gameplay
- **Visual feedback**: Progress messages and step-by-step move execution
- **Fallback handling**: Graceful handling when no solution exists

## 📁 Project Structure

```
├── model.py          # Game logic and entities (Cat, Glass, Room)
├── view.py           # Rendering (Tkinter GUI + text display)  
├── controller.py     # Input handling and game flow
├── ai_solver.py      # AI algorithms and game state representation
├── constants.py      # Game configuration and unified movement system
├── graphical_game.py # GUI entry point
├── text_game.py      # Console entry point
├── test_model.py     # Unit tests
└── games/default/    # Level definitions
```

## 🔬 Technical Highlights

- **Clean Architecture**: Demonstrates MVC pattern implementation
- **Modern Python**: Type annotations, error handling, and best practices
- **AI Integration**: Practical application of search algorithms
- **Code Quality**: Comprehensive constants, unified systems, and maintainable code
- **Testing**: Unit tests for core game logic

## 🚧 Future Enhancements

- **Web Version**: Flask + HTML5 Canvas for browser gameplay
- **A* Search**: More efficient pathfinding algorithm
- **Level Generator**: AI-powered puzzle creation
- **Advanced AI**: Machine learning approaches for puzzle analysis

## 🎯 Development Notes

This project showcases:
- **Problem-solving skills**: Implementing classic algorithms (BFS/DFS)
- **Software architecture**: Clean MVC pattern with extensible design
- **Modern development**: Collaborative AI-assisted development workflow
- **User experience**: Intuitive controls and visual feedback

---

*Developed collaboratively with AI assistance to demonstrate modern software development practices and algorithm implementation.*
