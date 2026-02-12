# 🚀 Explainer Agent - Quick Reference

## Switch Between Providers

### Interactive Switcher (Easiest)
```bash
python switch_provider.py
```

### Manual Switch

**To Groq (Cloud, Fast)**:
```bash
# Edit .env
LLM_PROVIDER=groq
GROQ_API_KEY=your_key_here
```

**To Ollama (Local, Private)**:
```bash
# Edit .env
LLM_PROVIDER=ollama
OLLAMA_MODEL=qwen2.5-coder:7b
```

---

## Quick Commands

### Groq Setup (5 minutes)
```bash
# 1. Get API key from https://console.groq.com
# 2. Edit .env
LLM_PROVIDER=groq
GROQ_API_KEY=gsk_your_key_here

# 3. Test
python demo.py
```

### Ollama Setup (10 minutes)
```bash
# 1. Pull a model
ollama pull qwen2.5-coder:7b

# 2. Edit .env
LLM_PROVIDER=ollama
OLLAMA_MODEL=qwen2.5-coder:7b

# 3. Test
python demo.py
```

---

## Common Tasks

### Explain Code
```python
from src.llm_client import llm_manager
import asyncio

code = """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
"""

async def explain():
    prompt = f"Explain this code:\n{code}"
    response = await llm_manager.generate(prompt)
    print(response)

asyncio.run(explain())
```

### Learn a Concept
```python
async def learn():
    response = await llm_manager.generate(
        "Explain dependency injection with Python examples"
    )
    print(response)

asyncio.run(learn())
```

### Get Best Practices
```python
async def best_practices():
    response = await llm_manager.generate(
        "What are Python async/await best practices?"
    )
    print(response)

asyncio.run(best_practices())
```

---

## Ollama Models Quick Reference

| Model | Command | Size | Quality | Use Case |
|-------|---------|------|---------|----------|
| **Qwen Coder** | `ollama pull qwen2.5-coder:7b` | 4.7GB | ⭐⭐⭐⭐⭐ | Code (recommended) |
| **Gemma** | `ollama pull gemma:2b` | 1.6GB | ⭐⭐⭐ | Fast/testing |
| **Llama** | `ollama pull llama3.2:3b` | 2.0GB | ⭐⭐⭐⭐ | General use |
| **CodeLlama** | `ollama pull codellama:7b` | 3.8GB | ⭐⭐⭐⭐ | Code generation |

---

## Troubleshooting

### Groq Issues

**"Invalid API key"**
```bash
# Check .env file
cat .env | grep GROQ_API_KEY

# Get new key at console.groq.com
```

**"Rate limit exceeded"**
```bash
# Wait 1 minute (30 req/min limit)
# Or switch to Ollama
python switch_provider.py
```

### Ollama Issues

**"Model not found"**
```bash
# Pull the model first
ollama pull qwen2.5-coder:7b

# List available models
ollama list
```

**"Connection refused"**
```bash
# Start Ollama service
ollama serve

# Or open Ollama app
```

**"ollama command not found"**
```bash
# Restart terminal (PATH needs refresh)
# Or restart VS Code
```

---

## Performance Tips

### Groq (Cloud)
- ✅ Fastest responses (<1 second)
- ✅ Best quality (70B model)
- ✅ No downloads needed
- ❌ Requires internet
- ❌ 30 requests/minute limit

### Ollama (Local)
- ✅ Unlimited requests
- ✅ Works offline
- ✅ 100% private
- ✅ Specialized code models
- ❌ Slower (depends on hardware)
- ❌ Requires model download

### Hybrid Approach
Use Groq as primary, Ollama as fallback!

The agent automatically switches if Groq fails.

---

## File Structure

```
explainer-agent/
├── demo.py                  # Quick demo
├── switch_provider.py       # Switch LLM providers
├── test_llm.py             # Test LLM connection
├── .env                    # Your configuration
├── README.md               # Full documentation
├── OLLAMA_SETUP.md         # Ollama guide
├── GROQ_SETUP.md           # Groq guide
├── SUCCESS.md              # What's working
└── src/
    ├── llm_client.py       # LLM integration
    ├── explainer.py        # Explanation engine
    └── cli.py              # CLI interface
```

---

## One-Line Commands

```bash
# Quick demo
python demo.py

# Switch provider
python switch_provider.py

# Test LLM
python test_llm.py

# Pull Ollama model
ollama pull qwen2.5-coder:7b

# List Ollama models
ollama list

# Test Ollama directly
ollama run qwen2.5-coder:7b "Explain async await"
```

---

## What's Next?

1. **Pull Ollama model**: `ollama pull qwen2.5-coder:7b`
2. **Try both providers**: Test Groq vs Ollama
3. **Read documentation**: Check `OLLAMA_SETUP.md`
4. **Build features**: Add your own use cases

---

**Quick help**: See `OLLAMA_SETUP.md` or `GROQ_SETUP.md` for detailed guides!
