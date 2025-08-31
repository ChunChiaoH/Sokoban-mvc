# Step 1: Import Flask and your existing game code
from flask import Flask, jsonify, request
from model import Model
from ai_solver import SokobanSolver
from constants import *

# Step 2: Create Flask app instance  
app = Flask(__name__)

# Step 3: Global game state (simple approach for learning)
game_model = None
solver = None

# Step 4: Home page route
@app.route('/')
def home():
    """Serve the main game page."""
    return "<h1>Sokoban Web Game</h1><p>API Server Running!</p><p>Try: <a href='/api/init'>/api/init</a></p>"

# Step 5: Game initialization API
@app.route('/api/init')
def init_game():
    """Initialize game and return JSON state."""
    global game_model, solver
    
    try:
        # Use your existing Model class!
        print("Initializing game...")
        game_model = Model(DEFAULT_GAMES)
        solver = SokobanSolver(game_model)
        print("Game initialized successfully!")
        
        # Convert game state to JSON
        game_state = get_game_state()
        
        return jsonify({
            'success': True,
            'state': game_state,
            'room_number': game_model.get_cur_room_num() + 1,
            'total_rooms': game_model.get_num_rooms(),
            'message': 'Game initialized!'
        })
        
    except Exception as e:
        print(f"Error initializing game: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        })

def get_game_state():
    """Convert your Model to JSON format."""
    if not game_model:
        return None
    
    room = game_model.get_room()
    cat = game_model.get_cat()
    
    # Extract room data
    num_rows, num_cols = room.get_dimension()
    tiles = []
    for i in range(num_rows):
        row = []
        for j in range(num_cols):
            tile = room.get_tile(i, j)
            row.append(tile.get_text())
        tiles.append(row)
    
    # Extract entities
    cat_pos = cat.get_pos()
    glasses = room.get_glasses()
    glass_list = []
    for pos, glass in glasses.items():
        glass_list.append({
            'position': pos,
            'type': glass.get_text()
        })
    
    return {
        'dimensions': [num_rows, num_cols],
        'tiles': tiles,
        'cat_position': cat_pos,
        'glasses': glass_list
    }

# Step 4: Run the app (only when script is run directly)
if __name__ == '__main__':
    print("Starting Flask server...")
    print("Visit: http://localhost:5000")
    app.run(debug=True, port=5000)