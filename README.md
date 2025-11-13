# Homework Grader - LeetCode Style C Programming Judge

A full-stack web application for grading C programming homework problems with automated testing using Judge0.

## Features

### Student Features
- Browse programming problems by difficulty
- Write C code in an integrated Monaco Editor
- View 3 visible test cases per problem
- Create custom test cases for additional testing
- Submit code for automated grading
- Receive partial credit based on percentage of hidden tests passed
- View submission history and detailed results

### Admin Features
- Create and manage programming problems
- Add problem descriptions with Markdown support
- Create visible and hidden test cases
- View all student submissions
- Delete problems and test cases

## Tech Stack

- **Backend**: FastAPI (Python)
- **Frontend**: React + Vite
- **Database**: SQLite
- **Code Execution**: Judge0 (RapidAPI or self-hosted)
- **Authentication**: JWT tokens
- **Code Editor**: Monaco Editor

## Prerequisites

- Python 3.8+
- Node.js 16+
- Judge0 API access (RapidAPI or self-hosted)

## Installation

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file:
```bash
cp .env.example .env
```

5. Edit `.env` and configure:
```
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///./homework_grader.db
JUDGE0_MODE=rapidapi  # or "self-hosted"
JUDGE0_RAPIDAPI_URL=https://judge0-ce.p.rapidapi.com
JUDGE0_RAPIDAPI_KEY=your-rapidapi-key
JUDGE0_SELF_HOSTED_URL=http://localhost:2358
```

6. Initialize database and create admin user:
```bash
python seed.py
```

This creates:
- Admin user: `admin` / `admin123`
- Sample problem: "Sum of Two Numbers"

7. Run the backend server:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Run the development server:
```bash
npm run dev
```

The app will be available at `http://localhost:5173`

## Judge0 Configuration

### Option 1: RapidAPI (Recommended for Development)

1. Sign up for RapidAPI: https://rapidapi.com/
2. Subscribe to Judge0 CE: https://rapidapi.com/judge0-official/api/judge0-ce
3. Copy your API key
4. In `backend/.env`:
```
JUDGE0_MODE=rapidapi
JUDGE0_RAPIDAPI_KEY=your-api-key-here
```

### Option 2: Self-Hosted Judge0

1. Install Docker and Docker Compose
2. Clone Judge0 repository:
```bash
git clone https://github.com/judge0/judge0.git
cd judge0
```

3. Follow Judge0 installation instructions
4. Start Judge0:
```bash
docker-compose up -d
```

5. In `backend/.env`:
```
JUDGE0_MODE=self-hosted
JUDGE0_SELF_HOSTED_URL=http://localhost:2358
```

## Usage

### First Time Setup

1. Start backend server: `cd backend && python main.py`
2. Start frontend: `cd frontend && npm run dev`
3. Open browser to `http://localhost:5173`
4. Login with admin credentials: `admin` / `admin123`

### Creating Problems (Admin)

1. Login as admin
2. Navigate to "Admin Dashboard"
3. Click "New Problem"
4. Fill in problem details:
   - Title
   - Description (supports Markdown)
   - Difficulty (Easy/Medium/Hard)
   - Constraints
5. Add 3 visible test cases (shown to students)
6. Add 10+ hidden test cases (used for grading)

### Solving Problems (Student)

1. Register a new account or login
2. Browse problems from the home page
3. Click on a problem to open the solver
4. Read the problem description and view visible test cases
5. Write C code in the editor
6. Optionally add custom test cases
7. Submit code for grading
8. View results showing percentage score

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login and get JWT token
- `GET /api/auth/me` - Get current user info

### Admin Endpoints
- `POST /api/admin/problems` - Create problem
- `GET /api/admin/problems` - List all problems
- `GET /api/admin/problems/{id}` - Get problem details
- `PUT /api/admin/problems/{id}` - Update problem
- `DELETE /api/admin/problems/{id}` - Delete problem
- `POST /api/admin/problems/{id}/testcases` - Add test case
- `DELETE /api/admin/testcases/{id}` - Delete test case
- `GET /api/admin/submissions` - View all submissions

### Student Endpoints
- `GET /api/problems` - List all problems (with visible tests only)
- `GET /api/problems/{id}` - Get problem details
- `POST /api/submit` - Submit code for grading
- `GET /api/submissions/{id}` - Get submission details
- `GET /api/problems/{id}/submissions` - Get user's submissions for problem
- `POST /api/user-testcases` - Create custom test case
- `GET /api/problems/{id}/user-testcases` - Get user's test cases
- `DELETE /api/user-testcases/{id}` - Delete custom test case

## Grading System

- Code is executed against all **hidden** test cases only
- Score = (Passed Tests / Total Hidden Tests) × 100
- Visible test cases are for student reference only
- Students can add custom test cases for their own testing
- Detailed results show:
  - Pass/fail status for each test
  - Expected vs actual output
  - Compilation errors
  - Runtime errors
  - Execution time and memory usage

## Project Structure

```
hw-grader-ese124/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── database.py          # Database configuration
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── auth.py              # Authentication logic
│   ├── judge0_client.py     # Judge0 API client
│   ├── seed.py              # Database seeding script
│   ├── requirements.txt     # Python dependencies
│   └── .env                 # Environment variables
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── pages/           # Page components
│   │   ├── context/         # React context (auth)
│   │   ├── App.jsx          # Main app component
│   │   └── main.jsx         # Entry point
│   ├── package.json         # NPM dependencies
│   └── vite.config.js       # Vite configuration
└── README.md                # This file
```

## Security Considerations

- Passwords are hashed using bcrypt
- JWT tokens for authentication
- Admin-only routes protected with role checks
- SQL injection prevention via ORM
- CORS configured for frontend-backend communication
- Code execution sandboxed via Judge0

## Troubleshooting

### Backend Issues

**Database errors:**
```bash
rm homework_grader.db  # Delete database
python seed.py          # Recreate and seed
```

**Judge0 connection errors:**
- Check your API key is correct
- Verify Judge0 service is running (if self-hosted)
- Check network connectivity

### Frontend Issues

**CORS errors:**
- Ensure backend is running on port 8000
- Check `vite.config.js` proxy configuration

**Build errors:**
```bash
rm -rf node_modules package-lock.json
npm install
```

## Future Enhancements

- Support for multiple programming languages
- Real-time code execution feedback
- Leaderboards and rankings
- Time limits for submissions
- Plagiarism detection
- Discussion forums
- Code templates per problem
- Batch test case upload
- Export submissions

## License

MIT License

## Support

For issues and questions, please create an issue in the repository or contact your instructor.

