# Tetris Game - Full Stack Implementation

A modern implementation of the classic Tetris game built with a full-stack architecture, featuring a Python backend and HTML/CSS/JavaScript frontend. This project demonstrates game development principles, real-time communication, and responsive web design.

## 🎮 Game Overview

Tetris is a tile-matching puzzle game where players must arrange falling tetromino pieces to create complete horizontal lines. When lines are completed, they disappear, and the player earns points. The game increases in speed as the player progresses.

## 🏗️ Architecture

This project follows a full-stack architecture with clear separation of concerns:

```
tetris-main/
├── backend/           # Python server and game logic
├── frontend/          # HTML, CSS, JavaScript client
└── .vscode/          # Development environment configuration
```

### Technology Stack

- **Backend**: Python (31.7%)
- **Frontend**: HTML, CSS, JavaScript (68.3%)
- **Communication**: WebSocket/HTTP API
- **Development**: VS Code configuration included

## 🚀 Features

### Core Game Features
- **Classic Tetris Gameplay**: Authentic tetromino pieces and mechanics
- **Real-time Game Logic**: Server-side game state management
- **Responsive Controls**: Keyboard input handling
- **Score System**: Point calculation and high score tracking
- **Progressive Difficulty**: Increasing speed as levels advance
- **Line Clearing**: Complete horizontal line detection and removal
- **Game Over Detection**: Collision detection and game termination

### Technical Features
- **Full-Stack Architecture**: Separate backend and frontend components
- **Real-time Communication**: Live game state synchronization
- **Cross-Platform**: Web-based implementation for universal access
- **Modern UI**: Clean, responsive design
- **Development Ready**: VS Code configuration for easy setup

## 📁 Project Structure

```
tetris-main/
├── 🔧 Backend (Python)
│   ├── Game engine logic
│   ├── Server implementation
│   ├── API endpoints
│   └── Game state management
│
├── 🎨 Frontend (HTML/CSS/JS)
│   ├── Game UI components
│   ├── Styling and animations
│   ├── User input handling
│   └── Client-server communication
│
└── ⚙️ Development
    └── .vscode/              # VS Code workspace configuration
        ├── settings.json     # Editor preferences
        ├── launch.json       # Debug configuration
        └── extensions.json   # Recommended extensions
```

## 🛠️ Prerequisites

- **Python 3.7+**: For backend server
- **Modern Web Browser**: Chrome, Firefox, Safari, or Edge
- **VS Code** (Optional): For development with included configuration
- **Web Server**: For serving the frontend files

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/dharaneesh-2005/tetris-main.git
cd tetris-main
```

### 2. Backend Setup
```bash
# Navigate to backend directory
cd backend

# Install Python dependencies (if requirements.txt exists)
pip install -r requirements.txt

# Start the Python server
python server.py
```

### 3. Frontend Setup
```bash
# Navigate to frontend directory
cd frontend

# Serve the frontend (using Python's built-in server)
python -m http.server 8000

# Or use any web server of your choice
# For example, with Node.js:
# npx serve .
```

### 4. VS Code Development Setup
The project includes VS Code configuration for optimal development experience:

- **Launch Configuration**: Debug both backend and frontend
- **Recommended Extensions**: Python, HTML/CSS/JS support
- **Workspace Settings**: Optimized for game development

## 🎯 How to Play

### Game Controls
- **Arrow Keys**: Move and rotate tetromino pieces
  - `←` / `→`: Move left/right
  - `↓`: Soft drop (faster fall)
  - `↑`: Rotate piece clockwise
- **Space**: Hard drop (instant drop)
- **P**: Pause/Resume game
- **R**: Restart game

### Game Rules
1. **Objective**: Fill complete horizontal lines to clear them
2. **Scoring**: Points awarded for line clears and soft drops
3. **Levels**: Game speed increases every 10 lines cleared
4. **Game Over**: When pieces reach the top of the playing field

## 🔧 Development

### Backend Development
The Python backend handles:
- Game logic and state management
- Tetromino generation and movement
- Collision detection
- Line clearing algorithms
- Score calculation
- API endpoints for client communication

### Frontend Development
The frontend provides:
- Interactive game interface
- Real-time rendering
- User input handling
- Visual feedback and animations
- Responsive design for different screen sizes

### VS Code Integration
The included `.vscode` configuration provides:
- **Debugging**: Step-through debugging for both backend and frontend
- **Extensions**: Recommended extensions for Python and web development
- **Settings**: Optimized editor settings for game development

## 🎨 Customization

### Game Mechanics
- **Speed Settings**: Adjust fall speed and level progression
- **Scoring System**: Modify point values for different actions
- **Tetromino Colors**: Customize piece colors and themes
- **Grid Size**: Adjust playing field dimensions

### Visual Design
- **CSS Styling**: Customize colors, fonts, and animations
- **Responsive Design**: Adapt layout for different devices
- **Theme Support**: Implement light/dark mode themes

## 🧪 Testing

### Backend Testing
```bash
cd backend
python -m pytest tests/  # If test files exist
```

### Frontend Testing
- Manual testing in different browsers
- Responsive design testing on various devices
- Performance testing for smooth gameplay

## 📦 Deployment

### Local Deployment
1. Start the Python backend server
2. Serve the frontend files
3. Access the game through your web browser

### Production Deployment
1. **Backend**: Deploy Python server to cloud platform (Heroku, AWS, etc.)
2. **Frontend**: Deploy static files to CDN or web hosting service
3. **Configuration**: Update API endpoints for production URLs

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork the Repository**
   ```bash
   git fork https://github.com/dharaneesh-2005/tetris-main.git
   ```

2. **Create a Feature Branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```

3. **Make Your Changes**
   - Follow the existing code style
   - Add comments for complex logic
   - Test your changes thoroughly

4. **Commit and Push**
   ```bash
   git commit -m "Add amazing feature"
   git push origin feature/amazing-feature
   ```

5. **Open a Pull Request**
   - Describe your changes
   - Include screenshots if applicable
   - Reference any related issues

## 🐛 Bug Reports

If you find a bug, please create an issue with:
- **Description**: Clear explanation of the problem
- **Steps to Reproduce**: How to trigger the bug
- **Expected Behavior**: What should happen
- **Actual Behavior**: What actually happens
- **Environment**: Browser, OS, and version information

## 📈 Future Enhancements

### Planned Features
- [ ] **Multiplayer Mode**: Real-time multiplayer gameplay
- [ ] **Leaderboards**: Global high score tracking
- [ ] **Sound Effects**: Audio feedback and background music
- [ ] **Mobile Support**: Touch controls for mobile devices
- [ ] **Game Modes**: Sprint, Ultra, and other Tetris variants
- [ ] **Customization**: User-defined themes and settings
- [ ] **AI Opponent**: Computer-controlled player option

### Technical Improvements
- [ ] **Performance Optimization**: Better rendering and memory usage
- [ ] **Database Integration**: Persistent score storage
- [ ] **WebSocket Communication**: Real-time multiplayer support
- [ ] **Progressive Web App**: Offline gameplay capability

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 👨‍💻 Author

**Dharaneesh**
- GitHub: [@dharaneesh-2005](https://github.com/dharaneesh-2005)

## 🙏 Acknowledgments

- **Tetris Company**: For creating the iconic puzzle game
- **Open Source Community**: For inspiration and collaboration
- **Contributors**: Thanks to all who help improve this project

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/dharaneesh-2005/tetris-main/issues)
- **Discussions**: [GitHub Discussions](https://github.com/dharaneesh-2005/tetris-main/discussions)
- **Contact**: Reach out through GitHub profile

---

**Enjoy playing Tetris!** 🎮✨

*Built with ❤️ using Python and modern web technologies*
