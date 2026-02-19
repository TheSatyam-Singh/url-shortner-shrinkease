# GitHub Copilot Instructions for ShrinkEase

## Project Overview
ShrinkEase is a URL shortening service with a React frontend and Flask backend using SQLite. The application allows users to create short URLs, track clicks, generate QR codes, and manage their shortened URLs.

## Technology Stack

### Backend (Flask)
- **Framework**: Flask 3.1.0
- **Database**: SQLite3
- **Key Libraries**:
  - `flask-cors` for CORS handling
  - `qrcode[pil]` for QR code generation
  - `python-dotenv` for environment configuration
- **Python Version**: 3.10+

### Frontend (React)
- **Framework**: React 19.2.0
- **Build Tool**: Vite 7.3.1
- **Routing**: React Router DOM 7.13.0
- **Linting**: ESLint 9.39.1
- **Node Version**: 18+
- **Package Manager**: pnpm

## Architecture Patterns

### Backend Architecture
1. **Modular Blueprint Design**:
   - Routes are organized in separate blueprints under `backend/routes/`
   - `url_routes.py` - URL shortening, listing, deletion
   - `redirect_routes.py` - Short code redirects
   - `auth_routes.py` - Authentication endpoints
   
2. **Database Layer**:
   - SQLite database with connection per request using Flask's `g` object
   - Schema: `urls` table with fields: id, original_url, short_code, clicks, created_at, qr_code
   - No ORM - using raw SQL with sqlite3

3. **Configuration**:
   - Environment variables loaded via `config.py`
   - Key configs: SECRET_KEY, BASE_URL, CORS_ALLOWED_ORIGINS, DB_PATH
   - Smart CORS origin normalization supporting both wildcard and specific origins

### Frontend Architecture
1. **Component Structure**:
   - Pages in `frontend/src/pages/`
   - Main routing in `App.jsx`
   - Configuration utilities in `frontend/src/config/`

2. **Styling**:
   - CSS Modules approach with `.css` files alongside components
   - No external CSS framework

## Coding Standards

### Backend (Python)
1. **Code Style**:
   - Follow PEP 8 conventions
   - Use descriptive variable names
   - Add docstrings only for complex functions
   
2. **Error Handling**:
   - Return JSON responses with appropriate HTTP status codes
   - Use `jsonify()` for all API responses
   - Handle database errors gracefully with try-except blocks

3. **Database Patterns**:
   ```python
   # Get database connection
   db = get_urls_collection()
   
   # Execute queries
   cursor = db.execute("SELECT ...", (params,))
   
   # Commit changes
   db.commit()
   ```

4. **Blueprint Registration**:
   - Register all blueprints in `app.py`
   - Use `/api` prefix for API routes

5. **Security**:
   - Never commit SECRET_KEY or sensitive data
   - Use environment variables for configuration
   - Validate and sanitize user inputs

### Frontend (React)
1. **Component Style**:
   - Use functional components with hooks
   - No class components
   - Destructure props at component level
   
2. **File Naming**:
   - Components: PascalCase (e.g., `Dashboard.jsx`)
   - Regular files: camelCase
   - CSS files match component names (e.g., `Dashboard.css`)

3. **State Management**:
   - Use `useState` and `useEffect` for local state
   - No external state management library currently

4. **API Communication**:
   - Use `fetch` API for backend communication
   - Configure API base URL via `frontend/src/config/`
   - Handle loading and error states

5. **Routing**:
   - Use React Router DOM declaratively
   - Define routes in `App.jsx`

## Common Tasks

### Adding a New Backend Route
1. Create or modify blueprint in `backend/routes/`
2. Register blueprint in `backend/app.py` if new
3. Follow REST conventions (GET, POST, PUT, DELETE)
4. Return JSON responses with proper status codes

### Adding a New Frontend Page
1. Create component in `frontend/src/pages/`
2. Add corresponding CSS file
3. Register route in `App.jsx`
4. Use React Router's `<Route>` component

### Database Schema Changes
1. Modify the `init_db()` function in `app.py`
2. Consider data migration for existing databases
3. Update related route handlers

### Environment Variables
- Backend: Add to `backend/.env` (never commit!)
- Frontend: Add to `frontend/.env` (never commit!)
- Document new variables in respective `.env.example` files

## Development Workflow

### Running Locally
```bash
# Backend
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python app.py

# Frontend
cd frontend
pnpm install
cp .env.example .env
pnpm dev
```

### Deployment
- Backend: Deploy to Render, Heroku, or any WSGI host
- Frontend: Build with `pnpm build`, deploy to Netlify/Vercel
- Set production environment variables on hosting platforms

## Code Generation Guidelines

### When Generating Backend Code:
- Import from `flask` for routing decorators and responses
- Use `get_db()` from `app` for database access
- Return `jsonify()` responses with status codes
- Handle CORS through app configuration (already set up)
- Generate short codes using `string.ascii_letters + string.digits`
- Use `datetime.now(timezone.utc).isoformat()` for timestamps

### When Generating Frontend Code:
- Import React and hooks at the top
- Use `fetch` for API calls with proper error handling
- Apply consistent styling with CSS modules
- Use semantic HTML elements
- Handle loading states and errors gracefully

### When Modifying Database Code:
- Use parameterized queries to prevent SQL injection
- Always commit after INSERT/UPDATE/DELETE operations
- Use `cursor.fetchone()` or `cursor.fetchall()` for SELECT queries
- Convert sqlite3.Row objects to dictionaries when needed

## Testing Guidelines
- No formal test suite currently exists
- Manual testing recommended for all changes
- Test CORS configuration when modifying backend routes
- Test responsive design when modifying frontend UI

## Important Notes
- The project uses SQLite for simplicity - no complex migrations
- QR codes are generated server-side and returned as base64 strings
- The short code is a 6-character alphanumeric string by default
- CORS is configured to support multiple origins or wildcard (*)
- The frontend is a Single Page Application (SPA)

## Security Considerations
- Validate all user inputs before database operations
- Use environment variables for sensitive configuration
- Ensure CORS is properly configured for production
- Never log or expose SECRET_KEY
- Sanitize URLs to prevent XSS attacks
- Rate limiting should be considered for production use

## Dependency Management
- Backend: Use `requirements.txt` for Python dependencies
- Frontend: Use `pnpm` (preferred) or `npm` for JavaScript dependencies
- Keep dependencies minimal and up-to-date
- Document any new dependencies in README if they're critical

## AI Assistant Behavior
When assisting with this codebase:
1. Maintain the existing architecture and patterns
2. Keep changes minimal and focused
3. Follow the established code style
4. Update documentation when adding new features
5. Consider backward compatibility
6. Respect the principle of least privilege for security
7. Suggest improvements when appropriate but don't over-engineer
8. Keep the codebase simple and maintainable
