from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
import json
import uuid
from typing import Dict, List
from game_logic import GameRoom, GameState

app = FastAPI()

# Allow CORS for local testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files (for the frontend)
app.mount("/static", StaticFiles(directory="../frontend"), name="static")

# Global room management
rooms: Dict[str, GameRoom] = {}
player_rooms: Dict[str, str] = {}  # player_id -> room_id

@app.get("/")
async def get_index():
    """Serve the main game page."""
    try:
        with open("../frontend/index.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(content="<h1>Game file not found</h1>", status_code=404)
    except Exception as e:
        return HTMLResponse(content=f"<h1>Error loading game: {str(e)}</h1>", status_code=500)

@app.websocket("/ws/{player_id}")
async def websocket_endpoint(websocket: WebSocket, player_id: str):
    await websocket.accept()
    
    try:
        # Send initial connection confirmation
        await websocket.send_text(json.dumps({
            "type": "connection",
            "player_id": player_id,
            "message": "Connected successfully"
        }))
        
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Handle different message types
            response = await handle_message(player_id, message, websocket)
            
            if response:
                await websocket.send_text(json.dumps(response))
                
    except WebSocketDisconnect:
        # Handle player disconnection
        await handle_disconnect(player_id)
    except Exception as e:
        print(f"Error handling WebSocket: {e}")
        await handle_disconnect(player_id)

async def handle_message(player_id: str, message: Dict, websocket) -> Dict:
    """Handle incoming WebSocket messages."""
    msg_type = message.get("type")
    
    if msg_type == "join_room":
        return await handle_join_room(player_id, message, websocket)
    
    elif msg_type == "create_room":
        return await handle_create_room(player_id, message, websocket)
    
    elif msg_type == "start_game":
        return await handle_start_game(player_id, message)
    
    elif msg_type == "game_move":
        return await handle_game_move(player_id, message)
    
    elif msg_type == "leave_room":
        return await handle_leave_room(player_id, message)
    
    else:
        return {"type": "error", "message": "Unknown message type"}

async def handle_join_room(player_id: str, message: Dict, websocket) -> Dict:
    """Handle player joining a room."""
    room_id = message.get("room_id")
    
    if room_id not in rooms:
        return {"type": "error", "message": "Room not found"}
    
    room = rooms[room_id]
    
    # Remove player from previous room if any
    if player_id in player_rooms:
        old_room_id = player_rooms[player_id]
        if old_room_id in rooms:
            rooms[old_room_id].remove_player(player_id)
    
    # Add player to new room
    if room.add_player(player_id, websocket):
        player_rooms[player_id] = room_id
        
        # Broadcast room state to all players
        await room.broadcast({
            "type": "room_update",
            "room_state": room.get_room_state()
        })
        
        return {
            "type": "room_joined",
            "room_id": room_id,
            "room_state": room.get_room_state()
        }
    else:
        return {"type": "error", "message": "Room is full"}

async def handle_create_room(player_id: str, message: Dict, websocket) -> Dict:
    """Handle room creation. Only the creator can set time_limit_seconds."""
    room_id = str(uuid.uuid4())[:8]  # Short room ID
    max_players = message.get("max_players", 4)
    time_limit_seconds = message.get("time_limit_seconds", 120)
    # Remove player from previous room if any
    if player_id in player_rooms:
        old_room_id = player_rooms[player_id]
        if old_room_id in rooms:
            rooms[old_room_id].remove_player(player_id)
    # Create new room with custom time limit and track creator
    room = GameRoom(room_id, max_players, time_limit_seconds, creator_id=player_id)
    rooms[room_id] = room
    room.add_player(player_id, websocket)
    player_rooms[player_id] = room_id
    return {
        "type": "room_created",
        "room_id": room_id,
        "room_state": room.get_room_state()
    }

async def handle_start_game(player_id: str, message: Dict) -> Dict:
    """Handle game start request."""
    if player_id not in player_rooms:
        return {"type": "error", "message": "Player not in a room"}
    
    room_id = player_rooms[player_id]
    room = rooms[room_id]
    
    if await room.start_game():
        # Broadcast game start to all players
        await room.broadcast({
            "type": "game_started",
            "room_state": room.get_room_state()
        })
        
        return {"type": "game_started", "room_state": room.get_room_state()}
    else:
        return {"type": "error", "message": "Not enough players to start game"}

async def handle_game_move(player_id: str, message: Dict) -> Dict:
    """Handle game move from player."""
    if player_id not in player_rooms:
        return {"type": "error", "message": "Player not in a room"}
    
    room_id = player_rooms[player_id]
    room = rooms[room_id]
    
    # Handle the move
    result = await room.handle_move(player_id, message.get("move", {}))
    
    if "error" in result:
        return {"type": "error", "message": result["error"]}
    
    # Broadcast move result to other players
    await room.broadcast({
        "type": "player_move",
        "player_id": player_id,
        "move_result": result
    }, exclude_player=player_id)
    
    return {
        "type": "move_result",
        "result": result
    }

async def handle_leave_room(player_id: str, message: Dict) -> Dict:
    """Handle player leaving room."""
    await handle_disconnect(player_id)
    return {"type": "left_room", "message": "Successfully left room"}

async def handle_disconnect(player_id: str):
    """Handle player disconnection."""
    if player_id in player_rooms:
        room_id = player_rooms[player_id]
        if room_id in rooms:
            room = rooms[room_id]
            room.remove_player(player_id)
            
            # Broadcast player left to remaining players
            await room.broadcast({
                "type": "player_left",
                "player_id": player_id,
                "room_state": room.get_room_state()
            })
            
            # Remove room if empty
            if len(room.players) == 0:
                del rooms[room_id]
        
        del player_rooms[player_id]

@app.get("/rooms")
async def list_rooms():
    """List all available rooms."""
    return {
        "rooms": [
            {
                "room_id": room_id,
                "player_count": len(room.players),
                "max_players": room.max_players,
                "game_state": room.game_state.value
            }
            for room_id, room in rooms.items()
        ]
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=10000, reload=True) 