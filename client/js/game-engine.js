import { SYMBOLS, DIRECTIONS, SAMPLE_ROOMS } from './config.js';

// Game State Management
export class GameState {
    constructor() {
        this.reset();
    }
    
    reset() {
        this.currentRoom = 0;
        this.rooms = [...SAMPLE_ROOMS];
        this.catPosition = [0, 0];
        this.tiles = [];
        this.glasses = [];
        this.dimensions = [0, 0];
    }
    
    // Deep copy for solver
    clone() {
        const cloned = new GameState();
        cloned.currentRoom = this.currentRoom;
        cloned.rooms = this.rooms; // Rooms don't change, can share reference
        cloned.catPosition = [...this.catPosition];
        cloned.tiles = this.tiles.map(row => [...row]);
        cloned.glasses = this.glasses.map(glass => ({
            position: [...glass.position],
            type: glass.type
        }));
        cloned.dimensions = [...this.dimensions];
        return cloned;
    }
    
    toHash() {
        return JSON.stringify({
            cat: this.catPosition,
            glasses: this.glasses.map(g => ({ pos: g.position, type: g.type }))
        });
    }
    
    isWinState() {
        return this.glasses.every(glass => glass.type === SYMBOLS.GLASS_ON_DEST);
    }
}

// Game Engine - Pure logic, no rendering
export class GameEngine {
    constructor() {
        this.state = new GameState();
    }
    
    loadRoom(roomIndex) {
        if (roomIndex >= this.state.rooms.length) {
            return { success: false, message: '🎉 All rooms completed!' };
        }
        
        this.state.currentRoom = roomIndex;
        const room = this.state.rooms[roomIndex];
        
        try {
            this.parseRoom(room.layout);
            return { 
                success: true, 
                message: `Room ${roomIndex + 1}: ${room.description}` 
            };
        } catch (error) {
            console.error('Failed to load room:', error);
            return { success: false, message: 'Failed to load room' };
        }
    }
    
    parseRoom(layout) {
        if (!layout || !Array.isArray(layout)) {
            throw new Error('Invalid room layout');
        }
        
        const rows = layout.length;
        const cols = layout[0]?.length || 0;
        
        this.state.dimensions = [rows, cols];
        this.state.tiles = [];
        this.state.glasses = [];
        
        for (let i = 0; i < rows; i++) {
            this.state.tiles[i] = [];
            const row = layout[i] || '';
            
            for (let j = 0; j < cols; j++) {
                const char = row[j] || SYMBOLS.EMPTY;
                
                switch (char) {
                    case 'C':
                        this.state.catPosition = [i, j];
                        this.state.tiles[i][j] = SYMBOLS.EMPTY;
                        break;
                    case 'G':
                        this.state.glasses.push({
                            position: [i, j],
                            type: SYMBOLS.GLASS
                        });
                        this.state.tiles[i][j] = SYMBOLS.EMPTY;
                        break;
                    case 'H':
                        this.state.glasses.push({
                            position: [i, j],
                            type: SYMBOLS.GLASS_ON_DEST
                        });
                        this.state.tiles[i][j] = SYMBOLS.DEST;
                        break;
                    default:
                        this.state.tiles[i][j] = char;
                }
            }
        }
    }
    
    makeMove(direction) {
        if (!DIRECTIONS[direction]) {
            return { success: false, message: 'Invalid direction' };
        }
        
        const [dRow, dCol] = DIRECTIONS[direction];
        const [catRow, catCol] = this.state.catPosition;
        const newRow = catRow + dRow;
        const newCol = catCol + dCol;
        
        // Bounds check
        if (!this.isValidPosition(newRow, newCol)) {
            return { success: false, message: 'Out of bounds' };
        }
        
        // Wall check
        if (this.state.tiles[newRow][newCol] === SYMBOLS.WALL) {
            return { success: false, message: 'Wall collision' };
        }
        
        // Glass handling
        const glassAtTarget = this.findGlassAt(newRow, newCol);
        if (glassAtTarget) {
            const pushResult = this.tryPushGlass(glassAtTarget, dRow, dCol);
            if (!pushResult.success) {
                return pushResult;
            }
        }
        
        // Move cat
        this.state.catPosition = [newRow, newCol];
        
        const isWin = this.state.isWinState();
        return { 
            success: true, 
            message: isWin ? '🎉 Room completed!' : 'Move successful',
            isWin: isWin
        };
    }
    
    tryPushGlass(glass, dRow, dCol) {
        const [glassRow, glassCol] = glass.position;
        const newGlassRow = glassRow + dRow;
        const newGlassCol = glassCol + dCol;
        
        if (!this.isValidPosition(newGlassRow, newGlassCol)) {
            return { success: false, message: 'Cannot push glass out of bounds' };
        }
        
        if (this.state.tiles[newGlassRow][newGlassCol] === SYMBOLS.WALL) {
            return { success: false, message: 'Cannot push glass into wall' };
        }
        
        if (this.findGlassAt(newGlassRow, newGlassCol)) {
            return { success: false, message: 'Cannot push glass into another glass' };
        }
        
        // Move the glass
        glass.position = [newGlassRow, newGlassCol];
        glass.type = (this.state.tiles[newGlassRow][newGlassCol] === SYMBOLS.DEST) ? 
            SYMBOLS.GLASS_ON_DEST : SYMBOLS.GLASS;
        
        return { success: true };
    }
    
    isValidPosition(row, col) {
        const [maxRow, maxCol] = this.state.dimensions;
        return row >= 0 && row < maxRow && col >= 0 && col < maxCol;
    }
    
    findGlassAt(row, col) {
        return this.state.glasses.find(glass => 
            glass.position[0] === row && glass.position[1] === col
        );
    }
    
    reset() {
        this.loadRoom(this.state.currentRoom);
    }
    
    nextRoom() {
        return this.loadRoom(this.state.currentRoom + 1);
    }
}