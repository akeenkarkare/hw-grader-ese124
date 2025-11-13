# Upgrade Instructions

Follow these steps to upgrade your existing Homework Grader installation with the latest improvements.

## Prerequisites

- Existing installation of Homework Grader
- Python 3.8+
- Node.js 16+

## Step 1: Backup Your Data

```bash
# Backup your database
cd backend
cp homework_grader.db homework_grader.db.manual-backup
```

## Step 2: Update Backend Dependencies

```bash
cd backend

# Update dependencies
pip install -r requirements.txt

# This will install the new slowapi package for rate limiting
```

## Step 3: Update Environment Variables

Edit your `backend/.env` file and add these new optional variables:

```bash
# Optional: Set to 'production' in production environment
ENV=development

# Optional: Comma-separated list of allowed origins
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000

# IMPORTANT: Set a strong SECRET_KEY for production!
SECRET_KEY=your-strong-secret-key-change-this
```

## Step 4: Migrate Database

```bash
cd backend
python migrate_db.py
```

The migration script will:
- Create an automatic backup
- Convert results column from TEXT to JSON
- Add performance indexes
- Show progress and confirm success

Type "yes" when prompted to proceed.

## Step 5: Test Backend

```bash
cd backend
python main.py
```

You should see:
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

Check for any warnings about SECRET_KEY.

## Step 6: Update Frontend

No dependency changes needed for frontend, but clear browser cache:

```bash
cd frontend

# Optional: Clear node_modules and reinstall if issues
# rm -rf node_modules package-lock.json
# npm install

npm run dev
```

## Step 7: Test the Application

1. **Open browser**: http://localhost:5173
2. **Login** with your credentials
3. **Test auto-save**:
   - Open a problem
   - Type some code
   - Refresh the page
   - Code should be restored
4. **Test submission**:
   - Submit a solution
   - Verify results display properly
5. **Test rate limiting** (optional):
   - Try making 10+ rapid login attempts
   - Should see rate limit error

## Verification Checklist

- [ ] Backend starts without errors
- [ ] Frontend loads successfully
- [ ] Can login with existing credentials
- [ ] Auto-save works (type code, refresh, code restored)
- [ ] Submissions work and show results
- [ ] Clear Code button works
- [ ] No console errors in browser

## New Features Available

### For Students:
- ✨ **Auto-save**: Code automatically saved every second
- ✨ **Clear Code button**: Easy way to start over
- ✨ **Better error messages**: More helpful feedback
- ✨ **Perfect score indicator**: Celebration when you get 100%!

### For Admins:
- 🔒 **Rate limiting**: Protection against abuse
- 📊 **Logging**: All operations logged for debugging
- ⚡ **Faster queries**: New indexes speed up database

### For Developers:
- 🛡️ **Security improvements**: SECRET_KEY validation, input validation
- 🎯 **Better error handling**: Compilation vs runtime errors
- 📝 **Whitespace tolerance**: Smarter output comparison
- 🗄️ **JSON columns**: Better data storage

## Troubleshooting

### Issue: Migration fails

**Solution**: The migration script automatically creates a backup. Check the error message and:
```bash
cd backend
# Restore from backup
cp homework_grader.db.backup homework_grader.db
# Try migration again
python migrate_db.py
```

### Issue: "Module slowapi not found"

**Solution**: Install dependencies
```bash
cd backend
pip install -r requirements.txt
```

### Issue: "SECRET_KEY must be set in production"

**Solution**: Set ENV=development in .env, or set a strong SECRET_KEY for production

### Issue: Rate limit errors

**Solution**: This is expected behavior. Wait 1 minute and try again.

### Issue: Auto-save not working

**Solution**:
- Check browser console for errors
- Verify localStorage is enabled in browser
- Clear browser cache and reload

### Issue: Old submissions not showing

**Solution**: The migration handles backward compatibility. If issues persist:
```bash
cd backend
# Check if migration completed
python -c "import sqlite3; conn = sqlite3.connect('homework_grader.db'); cursor = conn.cursor(); cursor.execute('PRAGMA table_info(submissions)'); print([col for col in cursor.fetchall() if col[1] == 'results'])"
```

## Rolling Back

If you encounter issues and need to rollback:

```bash
cd backend
# Restore database
cp homework_grader.db.manual-backup homework_grader.db

# Use git to revert code changes
git log  # find previous commit
git checkout <previous-commit-hash>

# Reinstall old dependencies
pip install -r requirements.txt
```

## Support

- Check [IMPROVEMENTS.md](IMPROVEMENTS.md) for detailed list of changes
- Check [README.md](README.md) for general usage instructions
- File issues on GitHub if problems persist

## Production Deployment Notes

For production deployment, make sure to:

1. Set `ENV=production` in .env
2. Set a strong `SECRET_KEY` (64+ random characters)
3. Configure `ALLOWED_ORIGINS` with your actual domain
4. Use a production-grade database (PostgreSQL recommended)
5. Set up proper logging and monitoring
6. Configure Judge0 with RapidAPI or self-hosted instance
7. Use a reverse proxy (nginx) for HTTPS
8. Set up automatic backups

Example production .env:
```bash
ENV=production
SECRET_KEY=your-very-long-random-secret-key-here-min-64-chars
ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
DATABASE_URL=postgresql://user:pass@localhost/hwgrader
JUDGE0_MODE=rapidapi
JUDGE0_RAPIDAPI_KEY=your-actual-key
```
