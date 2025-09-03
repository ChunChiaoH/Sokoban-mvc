// Game configuration and constants
export const CONFIG = {
    TILE_SIZE: 40,
    CANVAS_WIDTH: 600,
    CANVAS_HEIGHT: 600
};

// Game symbols
export const SYMBOLS = Object.freeze({
    EMPTY: ' ',
    WALL: '+',
    DEST: '0',
    CAT: 'C',
    GLASS: 'G',
    GLASS_ON_DEST: 'H'
});

// Movement directions
export const DIRECTIONS = Object.freeze({
    'UP': [-1, 0],
    'DOWN': [1, 0], 
    'LEFT': [0, -1],
    'RIGHT': [0, 1]
});

// Key mappings for input
export const KEY_MAPPINGS = Object.freeze({
    'ArrowUp': 'UP', 'w': 'UP', 'W': 'UP',
    'ArrowDown': 'DOWN', 's': 'DOWN', 'S': 'DOWN',
    'ArrowLeft': 'LEFT', 'a': 'LEFT', 'A': 'LEFT',
    'ArrowRight': 'RIGHT', 'd': 'RIGHT', 'D': 'RIGHT'
});

// Sample rooms data
export const SAMPLE_ROOMS = [
    {
        layout: [
            "++++++++",
            "+      +",
            "+ C G 0+", 
            "+      +",
            "++++++++"
        ],
        description: "Simple tutorial room"
    },
    {
        layout: [
            "++++++++++",
            "+    +   +",
            "+ C  G 0 +",
            "+    +   +",
            "++++++++++",
        ],
        description: "Easy room with obstacle"
    },
    {
        layout: [
            "+++++++++++",
            "+         +",
            "+ C G G 0 +",
            "+     0   +",
            "+++++++++++",
        ],
        description: "Two glasses challenge"
    }
];