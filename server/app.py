# Step 1: Import Flask and your existing game code
from flask import Flask, jsonify, request, render_template
from model import Model
from ai_solver import SokobanSolver
from constants import *
from utils import delta_to_direction_name, direction_name_to_delta

# Step 2: Create Flask app instance  
app = Flask(__name__)

# Step 3: Global game state (simple approach for learning)
game_model = None
solver = None

# Step 4: Home page route - Now serves HTML5 Canvas game!
@app.route('/')
def home():
    """
    Serve the main game page with HTML5 Canvas.
    
    FLASK LEARNING POINTS:
    1. render_template() looks in templates/ folder automatically
    2. Separates HTML (presentation) from Python (logic)
    3. More maintainable than returning raw HTML strings
    4. Industry standard for web applications
    """
    return render_template('index.html')

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
            'message': WEB_GAME_INITIALIZED
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

# Step 6: Handle Player Moves (POST endpoint)
@app.route('/api/move', methods=['POST'])
def move():
    """
    Handle player moves via JSON.
    
    FLASK LEARNING POINTS:
    1. methods=['POST'] - Only accepts POST requests (for sending data)
    2. request.get_json() - Extracts JSON from request body
    3. Input validation - Always validate user input
    4. Consistent responses - Same JSON structure for success/error
    5. Using constants - Better than hardcoded strings
    """
    global game_model
    
    # Check if game is initialized
    if not game_model:
        return jsonify({
            'success': False,
            'error': WEB_GAME_NOT_INITIALIZED  # Using constant!
        })
    
    try:
        # Extract JSON data from POST request
        data = request.get_json()
        
        # Validate JSON structure
        if not data or 'direction' not in data:
            return jsonify({
                'success': False,
                'error': WEB_MISSING_DIRECTION  # Using constant!
            })
        
        direction = data['direction'].upper()
        
        # Validate direction using existing game constants
        if direction not in MOVE_DIRECTIONS:
            return jsonify({
                'success': False,
                'error': WEB_INVALID_DIRECTION.format(direction)  # Using constant!
            })
        
        # Execute move using existing game logic
        delta = MOVE_DIRECTIONS[direction]['delta']
        old_cat_pos = game_model.get_cat().get_pos()  # Store position before move
        game_model.move_cat(delta)
        new_cat_pos = game_model.get_cat().get_pos()  # Get position after move
        move_successful = old_cat_pos != new_cat_pos  # Check if cat actually moved
        is_completed = game_model.get_room().all_filled()
        
        # Get current game state BEFORE advancing level
        current_state = get_game_state()
        current_room_num = game_model.get_cur_room_num() + 1
        
        # Handle level progression (same logic as desktop version)
        advanced_level = False
        if is_completed:
            # Check if there are more rooms
            if game_model.get_cur_room_num() + 1 < game_model.get_num_rooms():
                game_model.level_up()  # Advance to next room
                advanced_level = True
                is_completed = False  # Reset for new room
        
        # Build response with game state from BEFORE level advance
        response = {
            'success': True,
            'move_successful': move_successful,
            'direction': direction,
            'state': current_state,  # Use state before advancing
            'room_completed': is_completed and not advanced_level,
            'room_number': current_room_num,  # Use room number before advancing
            'total_rooms': game_model.get_num_rooms(),
            'advanced_level': advanced_level
        }
        
        # Add appropriate message using constants
        if is_completed and not advanced_level:
            response['message'] = WEB_ROOM_COMPLETED
        elif not move_successful:
            response['message'] = WEB_MOVE_BLOCKED
        else:
            response['message'] = WEB_MOVED_SUCCESS.format(direction.lower())
            
        return jsonify(response)
        
    except Exception as e:
        print(f"Error processing move: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        })

# Step 7: AI Hint Endpoint (GET request)
@app.route('/api/hint')
def get_hint():
    """
    Get AI hint for next move.
    
    FLASK LEARNING POINTS:
    1. GET endpoint (no methods parameter = GET by default)
    2. No JSON input needed - just returns suggestion
    3. Uses existing AI solver from your game
    4. Each thread gets its own request object (as we discussed)
    """
    global game_model, solver
    
    # Check if game is initialized
    if not game_model or not solver:
        return jsonify({
            'success': False,
            'error': WEB_GAME_NOT_INITIALIZED
        })
    
    try:
        # Check if puzzle is already solved
        if game_model.get_room().all_filled():
            return jsonify({
                'success': True,
                'hint': None,
                'message': AI_ALREADY_SOLVED_MSG  # Reusing existing constant
            })
        
        # Get hint from AI solver
        # This uses your existing BFS solver from ai_solver.py
        solution = solver.solve_bfs()
        
        if not solution or len(solution) == 0:
            return jsonify({
                'success': True,
                'hint': None,
                'message': AI_NO_SOLUTION_MSG  # No solution found
            })
        
        # Get the first move from solution
        first_move_delta = solution[0]
        
        # Convert delta back to direction name using utility function
        hint_direction = delta_to_direction_name(first_move_delta)
        
        return jsonify({
            'success': True,
            'hint': hint_direction,
            'hint_delta': first_move_delta,
            'total_moves': len(solution),
            'message': AI_TRY_MOVING_MSG.format(hint_direction.lower())
        })
        
    except Exception as e:
        print(f"Error getting hint: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        })

# Step 4: Run the app (only when script is run directly)
if __name__ == '__main__':
    print("Starting Flask server...")
    print("Visit: http://localhost:5000")
    app.run(debug=True, port=5000)