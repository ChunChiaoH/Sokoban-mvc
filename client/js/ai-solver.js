import { DIRECTIONS } from './config.js';
import { GameEngine } from './game-engine.js';

// AI Solver - BFS implementation
export class AISolver {
    constructor(gameEngine) {
        this.gameEngine = gameEngine;
    }
    
    getHint() {
        try {
            const solution = this.solveBFS();
            if (solution && solution.length > 0) {
                const firstMove = solution[0];
                const directionName = this.moveToDirection(firstMove);
                return {
                    success: true,
                    hint: directionName,
                    message: `💡 Hint: Try moving ${directionName.toLowerCase()}`
                };
            } else {
                return {
                    success: false,
                    message: 'No solution found or puzzle already solved!'
                };
            }
        } catch (error) {
            console.error('Solver error:', error);
            return {
                success: false,
                message: 'Error finding solution'
            };
        }
    }
    
    solveBFS() {
        const startState = this.gameEngine.state.clone();
        const queue = [startState];
        const visited = new Set();
        const parent = new Map();
        
        while (queue.length > 0) {
            const currentState = queue.shift();
            const currentHash = currentState.toHash();
            
            if (visited.has(currentHash)) continue;
            visited.add(currentHash);
            
            if (currentState.isWinState()) {
                return this.reconstructPath(parent, currentHash);
            }
            
            // Try all possible moves
            for (const [direction, move] of Object.entries(DIRECTIONS)) {
                const newState = this.simulateMove(currentState, move);
                if (newState) {
                    const newHash = newState.toHash();
                    if (!visited.has(newHash) && !parent.has(newHash)) {
                        queue.push(newState);
                        parent.set(newHash, { hash: currentHash, move: move });
                    }
                }
            }
        }
        
        return null; // No solution found
    }
    
    simulateMove(state, [dRow, dCol]) {
        const newState = state.clone();
        const [catRow, catCol] = newState.catPosition;
        const newRow = catRow + dRow;
        const newCol = catCol + dCol;
        
        // Use game engine logic for consistency
        const tempEngine = new GameEngine();
        tempEngine.state = newState;
        
        // Find direction name for the move
        const direction = Object.keys(DIRECTIONS).find(key => 
            DIRECTIONS[key][0] === dRow && DIRECTIONS[key][1] === dCol
        );
        
        const result = tempEngine.makeMove(direction);
        return result.success ? newState : null;
    }
    
    reconstructPath(parent, endHash) {
        const path = [];
        let current = endHash;
        
        while (parent.has(current)) {
            const parentInfo = parent.get(current);
            path.unshift(parentInfo.move);
            current = parentInfo.hash;
        }
        
        return path;
    }
    
    moveToDirection(move) {
        return Object.keys(DIRECTIONS).find(key => 
            DIRECTIONS[key][0] === move[0] && DIRECTIONS[key][1] === move[1]
        ) || 'UNKNOWN';
    }
}