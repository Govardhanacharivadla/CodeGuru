# ⚠️  Quick Fix Needed!

Ollama is installed but no models are downloaded yet.

## Fix: Pull a Model

**In the Ollama app you have open:**

1. **Click the search box** at the top
2. **Type**:  `gemma:2b` (small, fast model - good for testing)
3. **Click the download icon** (cloud with arrow)
4. **Wait** for download (~1.5 GB)

**OR use terminal** (if ollama command works):

```bash
ollama pull gemma:2b
```

## Then Update Config

Edit `.env` file and change:

```env
OLLAMA_MODEL=gemma:2b
```

## Alternative - Skip Ollama and Use Groq

If downloading models is taking too long:

1. Go to **https://console.groq.com**
2. Sign up (free, no credit card)
3. Get API key
4. Edit `.env`:
   ```env
   LLM_PROVIDER=groq
   GROQ_API_KEY=your_key_here
   ```

Then test with:
```bash
python test_llm.py
```

---

**I recommend Groq for now** - it's instant! No downloads needed.
