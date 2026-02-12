# Quick Start Without Ollama - Using Free Groq API

Don't want to install Ollama? No problem! Use Groq's free API instead.

## Step 1: Get Free Groq API Key (No Credit Card Required)

1. Go to: **https://console.groq.com**
2. Sign up with Google/GitHub (takes 30 seconds)
3. Click "API Keys" in sidebar
4. Click "Create API Key"
5. Copy your API key

## Step 2: Configure Explainer Agent

Create a `.env` file:

```bash
# In the explainer-agent directory
cp .env.example .env
```

Edit `.env` and add your key:

```env
# Use Groq instead of Ollama
LLM_PROVIDER=groq

# Paste your API key here
GROQ_API_KEY=gsk_your_api_key_here

# Groq model (free tier)
GROQ_MODEL=llama-3.1-70b-versatile

# Other settings (defaults work fine)
EXPLANATION_DEPTH=all
GENERATE_DIAGRAMS=true
```

## Step 3: Test It!

```bash
# Check configuration
python -m src.cli check

# Explain sample code
python -m src.cli explain --file tests/fixtures/sample.py --function fetch_user_data

# Learn a concept
python -m src.cli concept "async await"
```

## Benefits of Groq

✅ **No installation** - Just API key  
✅ **Completely free** - 30 requests/minute  
✅ **Extremely fast** - Fastest LLM API available  
✅ **No credit card** - Free forever  
✅ **Works immediately** - No model downloads  

## Rate Limits

Free tier: **30 requests per minute** (plenty for learning!)

---

**You can always install Ollama later for offline use!**
