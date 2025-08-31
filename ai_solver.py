from model import Model, Room
from constants import *
from collections import deque
from typing import Optional


class GameState:
    """Immutable representation of game state for AI search algorithms."""
    
    def __init__(self, cat_pos: tuple[int, int], glass_positions: frozenset[tuple[int, int]], room: Room):
        self.cat_pos = cat_pos
        self.glass_positions = glass_positions
        self.room = room
    
    def __hash__(self) -> int:
        return hash((self.cat_pos, self.glass_positions))
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, GameState):
            return False
        return self.cat_pos == other.cat_pos and self.glass_positions == other.glass_positions
    
    def is_solved(self) -> bool:
        """Check if all glasses are on destination tiles."""
        dest_positions = set()
        tiles = self.room.get_tiles()
        for i, row in enumerate(tiles):
            for j, tile in enumerate(row):
                if tile.get_text() == DEST:
                    dest_positions.add((i, j))
        
        return dest_positions == self.glass_positions
    
    def try_move(self, delta: tuple[int, int]) -> Optional['GameState']:
        """Try to move cat in given direction. Returns new GameState if valid, None if invalid."""
        cur_row, cur_col = self.cat_pos
        target_row, target_col = cur_row + delta[0], cur_col + delta[1]
        
        # Check boundary
        if not self._within_boundary(target_row, target_col):
            return None
            
        # Check if target tile is passable
        target_tile = self.room.get_tile(target_row, target_col)
        if not target_tile.is_passable():
            return None
        
        # Check if there's a glass at target position
        if (target_row, target_col) in self.glass_positions:
            # Try to push the glass
            glass_target_row = target_row + delta[0]
            glass_target_col = target_col + delta[1]
            
            # Check if glass can be pushed
            if (not self._within_boundary(glass_target_row, glass_target_col) or
                not self.room.get_tile(glass_target_row, glass_target_col).is_passable() or
                (glass_target_row, glass_target_col) in self.glass_positions):
                return None
            
            # Create new state with pushed glass
            new_glass_positions = (self.glass_positions - {(target_row, target_col)}) | {(glass_target_row, glass_target_col)}
            return GameState((target_row, target_col), new_glass_positions, self.room)
        else:
            # Just move cat
            return GameState((target_row, target_col), self.glass_positions, self.room)
    
    def _within_boundary(self, row: int, col: int) -> bool:
        """Check if position is within room boundaries."""
        max_row, max_col = self.room.get_dimension()
        return 0 <= row < max_row and 0 <= col < max_col
    
    @classmethod
    def from_model(cls, model: Model) -> 'GameState':
        """Create GameState from current Model state."""
        cat_pos = model.get_cat().get_pos()
        glass_positions = frozenset(model.get_room().get_glasses().keys())
        room = model.get_room()
        return cls(cat_pos, glass_positions, room)


class SokobanSolver:
    """AI solver for Sokoban puzzles using search algorithms."""
    
    def __init__(self, model: Model):
        self.model = model
    
    def solve_bfs(self) -> Optional[list[tuple[int, int]]]:
        """Solve using Breadth-First Search. Returns list of moves or None if no solution."""
        initial_state = GameState.from_model(self.model)
        
        if initial_state.is_solved():
            return []
        
        queue = deque([(initial_state, [])])
        visited = {initial_state}
        
        moves = [info['delta'] for info in MOVE_DIRECTIONS.values()]
        
        while queue:
            current_state, path = queue.popleft()
            
            for move in moves:
                next_state = current_state.try_move(move)
                
                if next_state is None or next_state in visited:
                    continue
                
                new_path = path + [move]
                
                if next_state.is_solved():
                    return new_path
                
                queue.append((next_state, new_path))
                visited.add(next_state)
        
        return None  # No solution found
    
    def solve_dfs(self, max_depth: int = 100) -> Optional[list[tuple[int, int]]]:
        """Solve using Depth-First Search with depth limit. Returns list of moves or None if no solution."""
        initial_state = GameState.from_model(self.model)
        visited = set()
        
        def dfs_recursive(state: GameState, path: list[tuple[int, int]], depth: int) -> Optional[list[tuple[int, int]]]:
            if depth > max_depth or state in visited:
                return None
            
            if state.is_solved():
                return path
            
            visited.add(state)
            moves = [info['delta'] for info in MOVE_DIRECTIONS.values()]
            
            for move in moves:
                next_state = state.try_move(move)
                if next_state is not None:
                    result = dfs_recursive(next_state, path + [move], depth + 1)
                    if result is not None:
                        return result
            
            visited.remove(state)  # Backtrack
            return None
        
        return dfs_recursive(initial_state, [], 0)