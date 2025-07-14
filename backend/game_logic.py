import random
import json
import asyncio
import time
from typing import List, Dict, Optional, Tuple
from enum import Enum

class PieceType(Enum):
    I = "I"
    O = "O"
    T = "T"
    S = "S"
    Z = "Z"
    J = "J"
    L = "L"

class GameState(Enum):
    WAITING = "waiting"
    PLAYING = "playing"
    FINISHED = "finished"

class TetrisGame:
    BOARD_WIDTH = 10
    BOARD_HEIGHT = 20
    
    
    # Tetris pieces (I, O, T, S, Z, J, L)
    PIECES = {
        PieceType.I: [[1, 1, 1, 1]],
        PieceType.O: [[1, 1], [1, 1]],
        PieceType.T: [[0, 1, 0], [1, 1, 1]],
        PieceType.S: [[0, 1, 1], [1, 1, 0]],
        PieceType.Z: [[1, 1, 0], [0, 1, 1]],
        PieceType.J: [[1, 0, 0], [1, 1, 1]],
        PieceType.L: [[0, 0, 1], [1, 1, 1]]
    }
    
    def __init__(self, player_id: str):
        self.player_id = player_id
        self.board = [[0 for _ in range(self.BOARD_WIDTH)] for _ in range(self.BOARD_HEIGHT)]
        self.current_piece = None
        self.current_x = 0
        self.current_y = 0
        self.score = 0
        self.lines_cleared = 0
        self.garbage_lines = 0
        self.game_state = GameState.WAITING
        self.hold_piece = None
        self.can_hold = True
        self.level = 1
        self.last_drop_time = time.time()
        self.drop_interval = 1.0  # 1 second at level 1
        
    def calculate_drop_interval(self):
        """Calculate drop interval based on level (standard Tetris formula)."""
        # Tetris speed formula: frames per drop = max(1, (0.8 - ((level - 1) * 0.007))^(level - 1) * 60)
        # Simplified: 1 second at level 1, decreases with level
        if self.level <= 8:
            return max(0.05, 1.0 - (self.level - 1) * 0.1)  # 1.0s, 0.9s, 0.8s, etc.
        else:
            return max(0.05, 0.2)  # Minimum 0.05 seconds for very high levels
    
    def update_level(self):
        """Update level based on lines cleared (every 10 lines = 1 level)."""
        new_level = (self.lines_cleared // 10) + 1
        if new_level != self.level:
            self.level = new_level
            self.drop_interval = self.calculate_drop_interval()
    
    def new_piece(self) -> Dict:
        """Generate a new piece and place it at the top of the board."""
        piece_type = random.choice(list(PieceType))
        piece = self.PIECES[piece_type]
        
        self.current_piece = {
            'type': piece_type.value,
            'shape': piece,
            'x': self.BOARD_WIDTH // 2 - len(piece[0]) // 2,
            'y': 0
        }
        
        self.current_x = self.current_piece['x']
        self.current_y = self.current_piece['y']
        self.last_drop_time = time.time()
        
        # Check if game over (new piece can't be placed)
        if not self.is_valid_move(0, 0):
            self.game_state = GameState.FINISHED
            return None
            
        return self.current_piece
    
    def is_valid_move(self, dx: int, dy: int, rotation: int = 0) -> bool:
        """Check if a move is valid."""
        if not self.current_piece:
            return False
            
        shape = self.current_piece['shape']
        
        # Apply rotation
        if rotation:
            shape = self.rotate_piece(shape, rotation)
        
        new_x = self.current_x + dx
        new_y = self.current_y + dy
        
        # Check boundaries and collisions
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    board_x = new_x + x
                    board_y = new_y + y
                    
                    if (board_x < 0 or board_x >= self.BOARD_WIDTH or 
                        board_y >= self.BOARD_HEIGHT or
                        (board_y >= 0 and self.board[board_y][board_x])):
                        return False
        return True
    
    def rotate_piece(self, shape: List[List[int]], rotations: int) -> List[List[int]]:
        """Rotate piece clockwise."""
        for _ in range(rotations):
            shape = list(zip(*shape[::-1]))  # Transpose and reverse
        return [list(row) for row in shape]
    
    def move_piece(self, dx: int, dy: int) -> bool:
        """Move the current piece."""
        if self.is_valid_move(dx, dy):
            self.current_x += dx
            self.current_y += dy
            # Update the piece position in the current_piece dict
            if self.current_piece:
                self.current_piece['x'] = self.current_x
                self.current_piece['y'] = self.current_y
            return True
        return False
    
    def rotate_current_piece(self) -> bool:
        """Rotate the current piece."""
        if self.is_valid_move(0, 0, 1):
            shape = self.current_piece['shape']
            self.current_piece['shape'] = self.rotate_piece(shape, 1)
            return True
        return False
    
    def hard_drop(self) -> int:
        """Drop the piece all the way down and return lines cleared."""
        drop_distance = 0
        while self.is_valid_move(0, 1):
            self.current_y += 1
            drop_distance += 1
        
        # Add score for hard drop (2 points per line dropped)
        self.score += drop_distance * 2
        
        return self.place_piece()
    
    def soft_drop(self) -> bool:
        """Drop the piece one line down."""
        success = self.move_piece(0, 1)
        if success:
            # Add score for soft drop (1 point per line)
            self.score += 1
        return success
    
    def auto_drop(self) -> int:
        """Automatically drop the piece based on time and level."""
        if self.game_state != GameState.PLAYING or not self.current_piece:
            return 0
        
        current_time = time.time()
        if current_time - self.last_drop_time >= self.drop_interval:
            if not self.move_piece(0, 1):
                # Piece can't move down, place it
                lines_cleared = self.place_piece()
                if lines_cleared > 0:
                    self.update_level()
                # If the game is finished after placing, return a special value
                return lines_cleared
            else:
                self.last_drop_time = current_time
        return 0
    
    def place_piece(self) -> int:
        """Place the current piece on the board and return lines cleared."""
        if not self.current_piece:
            return 0
            
        shape = self.current_piece['shape']
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    board_x = self.current_x + x
                    board_y = self.current_y + y
                    if 0 <= board_y < self.BOARD_HEIGHT and 0 <= board_x < self.BOARD_WIDTH:
                        self.board[board_y][board_x] = 1
        
        lines_cleared = self.clear_lines()
        self.current_piece = None
        self.can_hold = True
        # Generate new piece only if still playing
        if self.game_state == GameState.PLAYING:
            piece = self.new_piece()
            # If new_piece returns None, the game is now finished for this player
            if piece is None:
                self.game_state = GameState.FINISHED
        return lines_cleared
    
    def clear_lines(self) -> int:
        """Clear completed lines and return number of lines cleared."""
        lines_to_clear = []
        
        for y in range(self.BOARD_HEIGHT):
            if all(self.board[y]):
                lines_to_clear.append(y)
        
        # Remove cleared lines
        for line in reversed(lines_to_clear):
            del self.board[line]
            self.board.insert(0, [0 for _ in range(self.BOARD_WIDTH)])
        
        lines_cleared = len(lines_to_clear)
        if lines_cleared > 0:
            self.lines_cleared += lines_cleared
            
            # Standard Tetris scoring
            if lines_cleared == 1:
                self.score += 100 * self.level
            elif lines_cleared == 2:
                self.score += 300 * self.level
            elif lines_cleared == 3:
                self.score += 500 * self.level
            elif lines_cleared == 4:  # Tetris!
                self.score += 800 * self.level
        
        return lines_cleared
    
    def add_garbage_lines(self, lines: int):
        """Add garbage lines at the bottom."""
        for _ in range(lines):
            # Remove top line
            self.board.pop(0)
            # Add garbage line at bottom (with one hole)
            garbage_line = [1] * self.BOARD_WIDTH
            hole_pos = random.randint(0, self.BOARD_WIDTH - 1)
            garbage_line[hole_pos] = 0
            self.board.append(garbage_line)
            self.garbage_lines += 1
    
    def hold_piece_action(self) -> bool:
        """Hold the current piece."""
        if not self.can_hold or not self.current_piece:
            return False
        
        if self.hold_piece is None:
            self.hold_piece = self.current_piece['type']
            self.new_piece()
        else:
            # Swap current and held piece
            temp = self.hold_piece
            self.hold_piece = self.current_piece['type']
            self.current_piece = {
                'type': temp,
                'shape': self.PIECES[PieceType(temp)],
                'x': self.BOARD_WIDTH // 2 - len(self.PIECES[PieceType(temp)][0]) // 2,
                'y': 0
            }
            self.current_x = self.current_piece['x']
            self.current_y = self.current_piece['y']
        
        self.can_hold = False
        return True
    
    def get_board_state(self) -> Dict:
        """Get the current board state for transmission."""
        return {
            'board': self.board,
            'current_piece': self.current_piece,
            'hold_piece': self.hold_piece,
            'score': self.score,
            'lines_cleared': self.lines_cleared,
            'garbage_lines': self.garbage_lines,
            'game_state': self.game_state.value,
            'level': self.level,
            'drop_interval': self.drop_interval
        }
    
    def to_dict(self) -> Dict:
        """Convert game state to dictionary for JSON serialization."""
        return {
            'player_id': self.player_id,
            'board_state': self.get_board_state()
        }

class GameRoom:
    def __init__(self, room_id: str, max_players: int = 4):
        self.room_id = room_id
        self.max_players = max_players
        self.players: Dict[str, TetrisGame] = {}
        self.spectators: List[str] = []
        self.game_state = GameState.WAITING
        self.connections: Dict[str, any] = {}  # WebSocket connections
        self.game_task = None
        
    def add_player(self, player_id: str, websocket) -> bool:
        """Add a player to the room."""
        if len(self.players) >= self.max_players:
            return False
        
        self.players[player_id] = TetrisGame(player_id)
        self.connections[player_id] = websocket
        return True
    
    def remove_player(self, player_id: str):
        """Remove a player from the room."""
        if player_id in self.players:
            del self.players[player_id]
        if player_id in self.connections:
            del self.connections[player_id]
        if player_id in self.spectators:
            self.spectators.remove(player_id)
    
    async def start_game(self) -> bool:
        """Start the game if enough players."""
        if len(self.players) < 2:
            return False
        
        self.game_state = GameState.PLAYING
        for player in self.players.values():
            player.game_state = GameState.PLAYING
            player.new_piece()
        
        # Start the game loop
        await self.start_game_loop()
        
        return True
    
    async def check_and_broadcast_game_over(self):
        """Check if the game is over and broadcast the winner if so."""
        playing_players = [pid for pid, game in self.players.items() if game.game_state == GameState.PLAYING]
        finished_players = [pid for pid, game in self.players.items() if game.game_state == GameState.FINISHED]
        if len(playing_players) == 1 and len(finished_players) >= 1:
            # One winner
            winner_id = playing_players[0]
            self.game_state = GameState.FINISHED
            await self.broadcast({
                "type": "game_over",
                "winner_id": winner_id,
                "room_state": self.get_room_state()
            })
        elif len(playing_players) == 0 and len(finished_players) > 0:
            # All finished, no winner (tie or all lost)
            self.game_state = GameState.FINISHED
            await self.broadcast({
                "type": "game_over",
                "winner_id": None,
                "room_state": self.get_room_state()
            })
    
    async def start_game_loop(self):
        """Start the game loop for automatic piece dropping."""
        async def game_loop():
            while self.game_state == GameState.PLAYING:
                await asyncio.sleep(0.1)  # Check every 100ms for smoother gameplay
                
                # Auto-drop for all players based on their individual timers
                for player_id, game in self.players.items():
                    if game.game_state == GameState.PLAYING:
                        lines_cleared = game.auto_drop()
                        if lines_cleared > 0:
                            await self.handle_line_clear(player_id, lines_cleared)
                        # If the game just finished for this player, check for game over
                        if game.game_state == GameState.FINISHED:
                            await self.check_and_broadcast_game_over()
                
                # Broadcast updated state after all auto-drops
                await self.broadcast({
                    "type": "game_update",
                    "room_state": self.get_room_state()
                })
                # Also check for game over in case all are finished
                await self.check_and_broadcast_game_over()
        
        # Start the game loop
        asyncio.create_task(game_loop())
    
    async def handle_move(self, player_id: str, move_data: Dict) -> Dict:
        """Handle a player move and return game updates."""
        if player_id not in self.players:
            return {'error': 'Player not found'}
        
        game = self.players[player_id]
        if game.game_state != GameState.PLAYING:
            return {'error': 'Game not in playing state'}
        
        move_type = move_data.get('type')
        lines_cleared = 0
        
        if move_type == 'move':
            dx = move_data.get('dx', 0)
            dy = move_data.get('dy', 0)
            success = game.move_piece(dx, dy)
            
        elif move_type == 'rotate':
            success = game.rotate_current_piece()
            
        elif move_type == 'hard_drop':
            lines_cleared = game.hard_drop()
            success = True
            
        elif move_type == 'soft_drop':
            success = game.soft_drop()
            
        elif move_type == 'hold':
            success = game.hold_piece_action()
            
        else:
            return {'error': 'Invalid move type'}
        
        # Handle line clears and garbage attacks
        if lines_cleared > 0:
            await self.handle_line_clear(player_id, lines_cleared)
        
        # If the game just finished for this player, check for game over
        if game.game_state == GameState.FINISHED:
            await self.check_and_broadcast_game_over()
        
        # Always broadcast updated state after a move
        await self.broadcast({
            "type": "game_update",
            "room_state": self.get_room_state()
        })
        # Also check for game over in case all are finished
        await self.check_and_broadcast_game_over()
        
        return {
            'success': success,
            'player_state': game.get_board_state(),
            'lines_cleared': lines_cleared
        }
    
    async def handle_line_clear(self, player_id: str, lines_cleared: int):
        """Handle line clear and send garbage to other players."""
        if lines_cleared >= 2:  # Only send garbage for 2+ lines
            garbage_lines = lines_cleared - 1  # Send one less than cleared
            
            for other_id, other_game in self.players.items():
                if other_id != player_id and other_game.game_state == GameState.PLAYING:
                    other_game.add_garbage_lines(garbage_lines)
    
    def get_room_state(self) -> Dict:
        """Get the current state of the room."""
        return {
            'room_id': self.room_id,
            'game_state': self.game_state.value,
            'players': {pid: game.to_dict() for pid, game in self.players.items()},
            'spectators': self.spectators,
            'max_players': self.max_players
        }
    
    async def broadcast(self, message: Dict, exclude_player: str = None):
        """Broadcast message to all players in the room."""
        for player_id, connection in self.connections.items():
            if player_id != exclude_player:
                try:
                    await connection.send_text(json.dumps(message))
                except Exception:
                    pass  # Connection might be closed 