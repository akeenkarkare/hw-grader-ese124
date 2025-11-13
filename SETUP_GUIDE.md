# Quick Setup Guide

## Current Status

✅ **Backend**: Fully functional and running on http://localhost:8000
✅ **Frontend**: Fully functional and running on http://localhost:5173
✅ **Database**: Initialized with sample data
✅ **Authentication**: Working (JWT-based)
✅ **API Endpoints**: All tested and working

## What's Already Running

Both servers are currently running:
- Backend: `http://localhost:8000`
- Frontend: `http://localhost:5173`

## Test Credentials

**Admin Account:**
- Username: `admin`
- Password: `admin123`

**Test Student Account:**
- Username: `student1`
- Password: `test123`

## Quick Start (Already Done)

The application is already set up and running! You can:

1. **Access the frontend** at http://localhost:5173
2. **Login as admin** to manage problems
3. **Login as student** to solve problems
4. **API docs** available at http://localhost:8000/docs

## What You Need to Configure Next

### Judge0 Integration

The Judge0 client is implemented but needs API access to execute code. You have two options:

#### Option 1: RapidAPI (Quick Setup)
1. Sign up at https://rapidapi.com/
2. Subscribe to Judge0 CE: https://rapidapi.com/judge0-official/api/judge0-ce
3. Get your API key
4. Update `backend/.env`:
   ```
   JUDGE0_MODE=rapidapi
   JUDGE0_RAPIDAPI_KEY=your-actual-api-key-here
   ```

#### Option 2: Self-Hosted (Full Control)
1. Install Docker and Docker Compose
2. Clone Judge0:
   ```bash
   git clone https://github.com/judge0/judge0.git
   cd judge0
   docker-compose up -d
   ```
3. Update `backend/.env`:
   ```
   JUDGE0_MODE=self-hosted
   JUDGE0_SELF_HOSTED_URL=http://localhost:2358
   ```

### Restart Backend After Configuration
```bash
# Stop the current backend (it's running in background)
pkill -f "python main.py"

# Restart with new configuration
cd backend
source venv/bin/activate
python main.py
```

## Verified Features

### Backend API
✅ User registration and authentication
✅ Admin can create/edit/delete problems
✅ Admin can add visible and hidden test cases
✅ Students can view problems (only visible test cases)
✅ Students can create custom test cases
✅ Submission endpoint ready (needs Judge0 API key)

### Frontend
✅ Login/Register page
✅ Admin dashboard for problem management
✅ Problem list page
✅ Problem solver with Monaco code editor
✅ Test case management
✅ Submission results display

## Testing the Application

### Test Admin Functions
1. Go to http://localhost:5173
2. Login with `admin` / `admin123`
3. Click "Admin Dashboard"
4. View the "Sum of Two Numbers" problem
5. See 3 visible + 10 hidden test cases
6. Try creating a new problem

### Test Student Functions
1. Logout (or use incognito window)
2. Register a new account
3. Browse problems
4. Click on "Sum of Two Numbers"
5. See the 3 visible test cases
6. Add a custom test case
7. Write C code in the editor

### Test Submission (After Judge0 Setup)
1. Login as student
2. Open a problem
3. Write C code:
   ```c
   #include <stdio.h>
   
   int main() {
       int a, b;
       scanf("%d %d", &a, &b);
       printf("%d\n", a + b);
       return 0;
   }
   ```
4. Submit code
5. See score (0-100%) based on hidden tests passed

## Project Structure

```
hw-grader-ese124/
├── backend/
│   ├── main.py              # FastAPI app (✅ running)
│   ├── database.py          # SQLite config
│   ├── models.py            # Database models
│   ├── schemas.py           # API schemas
│   ├── auth.py              # JWT authentication
│   ├── judge0_client.py     # Judge0 integration (⚠️ needs API key)
│   ├── seed.py              # Database seeding (✅ executed)
│   ├── homework_grader.db   # SQLite database (✅ created)
│   └── venv/                # Python virtual environment
├── frontend/
│   ├── src/
│   │   ├── pages/           # React pages (✅ built)
│   │   ├── components/      # React components (✅ built)
│   │   └── context/         # Auth context (✅ built)
│   └── node_modules/        # NPM dependencies (✅ installed)
└── README.md                # Full documentation
```

## Common Commands

### Backend
```bash
cd backend
source venv/bin/activate
python main.py                    # Start server
python seed.py                    # Reset database
```

### Frontend
```bash
cd frontend
npm run dev                       # Start dev server
npm run build                     # Build for production
```

## Troubleshooting

### Backend Not Responding
```bash
pkill -f "python main.py"
cd backend && source venv/bin/activate && python main.py
```

### Frontend Not Loading
```bash
pkill -f "vite"
cd frontend && npm run dev
```

### Database Issues
```bash
cd backend
rm homework_grader.db
python seed.py
```

## Next Steps

1. **Configure Judge0** (see above) to enable code execution
2. **Create more problems** using the admin dashboard
3. **Test with students** by having them solve problems
4. **Monitor submissions** in the admin panel

## Architecture Overview

### Authentication Flow
1. User logs in → Backend issues JWT token
2. Frontend stores token in localStorage
3. All API requests include token in Authorization header
4. Backend validates token for protected routes

### Submission Flow
1. Student writes code and submits
2. Backend receives code and problem ID
3. Backend fetches all **hidden** test cases for the problem
4. Backend sends code to Judge0 for execution against each test case
5. Backend calculates score: (passed/total) × 100
6. Backend stores submission with results
7. Frontend displays score and test results

### Security
- Passwords hashed with bcrypt
- JWT tokens with 30-day expiration
- Admin routes require admin role
- Students can only see their own submissions
- Hidden test cases never exposed to students

## Support

If you encounter issues:
1. Check that both servers are running
2. Verify database exists: `ls backend/homework_grader.db`
3. Check backend logs for errors
4. Ensure Python 3.14 is being used
5. Verify all dependencies are installed

For Judge0 issues, see the README.md for detailed configuration instructions.

