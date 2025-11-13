# Judge0 Setup Guide

## Current Status: Mock Mode

The system is currently running in **MOCK MODE**, which simulates code execution without actually running C code. This is useful for testing the UI and workflow, but doesn't provide real code execution.

### What Mock Mode Does:

- ✅ Analyzes code structure (looks for scanf, printf, operators)
- ✅ Provides instant feedback (no network delays)
- ✅ Simulates partial credit scoring
- ⚠️ **Cannot actually compile or run C code**
- ⚠️ **Cannot detect logic errors**
- ⚠️ **Cannot test edge cases properly**

### Mock Mode Behavior:

**Code with basic structure** (has scanf, printf, +):
- Passes ~70% of tests
- Score: 70%
- Message: "⚠️ MOCK MODE - Configure Judge0 for real execution"

**Code missing basic elements**:
- Fails all tests
- Score: 0%
- Message: "Code does not match expected pattern"

---

## Enable Real Code Execution

To get real C code execution, you need to configure Judge0. Choose one option:

---

## Option 1: RapidAPI (Recommended for Quick Setup)

**Time**: ~5 minutes  
**Cost**: Free tier available (50 requests/day)  
**Best for**: Development, small classes

### Steps:

1. **Sign up for RapidAPI**
   - Go to https://rapidapi.com/
   - Create a free account

2. **Subscribe to Judge0 CE**
   - Visit https://rapidapi.com/judge0-official/api/judge0-ce
   - Click "Subscribe to Test"
   - Choose "Basic" plan (Free - 50 requests/day)
   - Or choose "Pro" plan ($5/month - 2000 requests/day)

3. **Get Your API Key**
   - After subscribing, you'll see your API key in the "X-RapidAPI-Key" header
   - Copy this key

4. **Configure the Backend**
   
   Edit `backend/.env` (create it if it doesn't exist):
   ```bash
   SECRET_KEY=dev-secret-key-change-in-production-12345678
   DATABASE_URL=sqlite:///./homework_grader.db
   JUDGE0_MODE=rapidapi
   JUDGE0_RAPIDAPI_URL=https://judge0-ce.p.rapidapi.com
   JUDGE0_RAPIDAPI_KEY=YOUR_ACTUAL_KEY_HERE
   ```

5. **Restart the Backend**
   ```bash
   # Stop the current backend
   pkill -f "python main.py"
   
   # Start it again
   cd backend
   source venv/bin/activate
   python main.py
   ```

6. **Test It**
   - Submit this correct code:
   ```c
   #include <stdio.h>
   
   int main() {
       int a, b;
       scanf("%d %d", &a, &b);
       printf("%d\n", a + b);
       return 0;
   }
   ```
   - Should get 100% score
   
   - Submit this wrong code:
   ```c
   #include <stdio.h>
   
   int main() {
       printf("wrong\n");
       return 0;
   }
   ```
   - Should get 0% score

---

## Option 2: Self-Hosted Judge0 (Full Control)

**Time**: ~30 minutes  
**Cost**: Free (uses your server resources)  
**Best for**: Production, large classes, privacy concerns

### Prerequisites:
- Docker installed
- Docker Compose installed
- At least 2GB RAM available

### Steps:

1. **Clone Judge0 Repository**
   ```bash
   cd ~
   git clone https://github.com/judge0/judge0.git
   cd judge0
   ```

2. **Configure Judge0**
   ```bash
   # Copy example config
   cp docker-compose.yml.example docker-compose.yml
   
   # Optional: Edit docker-compose.yml to customize ports/settings
   nano docker-compose.yml
   ```

3. **Start Judge0**
   ```bash
   docker-compose up -d
   ```
   
   This will start:
   - Judge0 server on port 2358
   - PostgreSQL database
   - Redis cache

4. **Wait for Initialization** (1-2 minutes)
   ```bash
   # Check if Judge0 is ready
   curl http://localhost:2358/about
   ```
   
   Should return JSON with version info

5. **Configure the Backend**
   
   Edit `backend/.env`:
   ```bash
   SECRET_KEY=dev-secret-key-change-in-production-12345678
   DATABASE_URL=sqlite:///./homework_grader.db
   JUDGE0_MODE=self-hosted
   JUDGE0_SELF_HOSTED_URL=http://localhost:2358
   ```

6. **Restart the Backend**
   ```bash
   pkill -f "python main.py"
   cd ~/hw-grader-ese124/backend
   source venv/bin/activate
   python main.py
   ```

7. **Test It** (same test code as RapidAPI)

### Managing Self-Hosted Judge0:

```bash
# Stop Judge0
cd ~/judge0
docker-compose down

# Start Judge0
docker-compose up -d

# View logs
docker-compose logs -f

# Check status
docker-compose ps
```

---

## Troubleshooting

### "All tests passing" with wrong code
- **Cause**: Still in mock mode
- **Solution**: Check `.env` file has correct `JUDGE0_MODE` and API key
- **Verify**: Backend logs should NOT show "MOCK MODE" warnings

### "Submission takes too long"
- **RapidAPI**: Check your API key is valid
- **Self-hosted**: Ensure Docker containers are running: `docker ps`
- **Network**: Check firewall isn't blocking connections

### "Compilation Error" for correct code
- **Check**: Make sure C language ID is correct (50 for GCC 9.2.0)
- **RapidAPI**: Try the Judge0 API directly to test
- **Self-hosted**: Check Judge0 logs: `docker-compose logs judge0-server`

### "Connection refused"
- **Self-hosted**: Judge0 containers not running
  ```bash
  cd ~/judge0
  docker-compose up -d
  ```

### "Invalid API key"
- **RapidAPI**: Recheck your key from RapidAPI dashboard
- **Make sure**: Key is in `.env` file correctly (no quotes, no spaces)

---

## Verification Checklist

After configuring Judge0, verify:

- [ ] Backend starts without "MOCK MODE" warning
- [ ] Correct code gets 100% score
- [ ] Wrong code gets 0% or partial score
- [ ] Compilation errors are shown
- [ ] Runtime errors are caught
- [ ] Execution time is displayed
- [ ] Results show actual output vs expected

---

## Cost Comparison

| Method | Setup Time | Monthly Cost | Requests/Day | Latency |
|--------|------------|--------------|--------------|---------|
| Mock Mode | 0 min | Free | Unlimited | <1ms |
| RapidAPI Free | 5 min | Free | 50 | ~500ms |
| RapidAPI Pro | 5 min | $5 | 2000 | ~500ms |
| Self-Hosted | 30 min | Server costs | Unlimited | ~100ms |

---

## Recommendations

**For Development/Testing:**
- Use Mock Mode (already set up)

**For Small Classes (<10 students):**
- Use RapidAPI Free tier
- Upgrade to Pro if needed

**For Production/Large Classes:**
- Use Self-Hosted Judge0
- More control, better performance
- No per-request costs

**For Your Server:**
Since you mentioned you have a server, I recommend:
1. Start with RapidAPI for quick testing (5 minutes)
2. Set up self-hosted Judge0 on your server for production use
3. Point all environments to your self-hosted instance

---

## Next Steps

1. Choose your Judge0 setup method
2. Follow the steps above
3. Test with sample submissions
4. Create real homework problems!

Need help? Check the backend logs for detailed error messages.

