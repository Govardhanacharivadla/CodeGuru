# 🦙 Ollama Setup Guide - Local AI Models

## Why Use Ollama?

**Advantages**:
- ✅ **100% Private** - Code never leaves your machine
- ✅ **Unlimited** - No rate limits, no usage caps
- ✅ **Offline** - Works without internet
- ✅ **No API keys** - No sign-ups required
- ✅ **Specialized models** - Code-specific models available

**Disadvantages**:
- ❌ Requires download (~4-8 GB per model)
- ❌ Slower than Groq (depends on your GPU/CPU)
- ❌ Requires good hardware (8GB+ RAM recommended)

---

## Step 1: Verify Ollama Installation

You already have Ollama installed! ✅

Check version:
```bash
ollama --version
```

If this doesn't work, close and reopen your terminal (PATH needs to refresh).

---

## Step 2: Pull a Model

### Recommended Models for Code Explanation

**Best Option - Qwen2.5 Coder (Recommended)**
Specialized for code, best quality:
```bash
ollama pull qwen2.5-coder:7b
```
- Size: ~4.7 GB
- RAM needed: 8 GB
- Quality: ⭐⭐⭐⭐⭐
- Speed: ⭐⭐⭐
- Best for: Code explanation, debugging

**Fast Option - Gemma 2B**
Smallest, fastest:
```bash
ollama pull gemma:2b
```
- Size: ~1.6 GB
- RAM needed: 4 GB
- Quality: ⭐⭐⭐
- Speed: ⭐⭐⭐⭐⭐
- Best for: Quick answers, simple explanations

**Balanced Option - Llama 3.2**
Good balance:
```bash
ollama pull llama3.2:3b
```
- Size: ~2 GB
- RAM needed: 6 GB
- Quality: ⭐⭐⭐⭐
- Speed: ⭐⭐⭐⭐
- Best for: General explanations

**Power User - CodeLlama**
Facebook's code model:
```bash
ollama pull codellama:7b
```
- Size: ~3.8 GB
- RAM needed: 8 GB
- Quality: ⭐⭐⭐⭐
- Speed: ⭐⭐⭐
- Best for: Code generation, refactoring

---

## Step 3: Configure Explainer Agent

### Option A: Use Ollama GUI (Easiest)

1. **Open the Ollama app** (you already have it running)
2. **Search for a model** in the search box at top
3. **Click the cloud icon** to download
4. **Wait for download** to complete

Then update `.env`:
```env
LLM_PROVIDER=ollama
OLLAMA_MODEL=qwen2.5-coder:7b
```

### Option B: Use Command Line

Open **Command Prompt** or **PowerShell** (NOT Git Bash):

```powershell
# Pull the recommended model
ollama pull qwen2.5-coder:7b

# Or pull a faster model
ollama pull gemma:2b
```

Then update `.env`:
```env
LLM_PROVIDER=ollama
OLLAMA_MODEL=qwen2.5-coder:7b  # or gemma:2b
```

---

## Step 4: Test Ollama

### Test 1: Verify Model is Downloaded

```bash
ollama list
```

You should see your model listed.

### Test 2: Test Model Directly

```bash
ollama run qwen2.5-coder:7b "Explain async/await in Python"
```

### Test 3: Test with Explainer Agent

Update your `.env`:
```env
LLM_PROVIDER=ollama
OLLAMA_MODEL=qwen2.5-coder:7b
```

Run the demo:
```bash
python demo.py
```

---

## Step 5: Switch Between Groq and Ollama

### Use Groq (Fast, Cloud)
Edit `.env`:
```env
LLM_PROVIDER=groq
GROQ_API_KEY=gsk_your_key_here
GROQ_MODEL=llama-3.3-70b-versatile
```

**When to use**:
- Need fastest responses
- Have internet connection
- Don't mind cloud processing

### Use Ollama (Private, Local)
Edit `.env`:
```env
LLM_PROVIDER=ollama
OLLAMA_MODEL=qwen2.5-coder:7b
```

**When to use**:
- Working with sensitive code
- No internet connection
- Unlimited usage needed
- Want specialized code models

---

## Advanced: Model Comparison

| Model | Size | RAM | Speed | Quality | Use Case |
|-------|------|-----|-------|---------|----------|
| qwen2.5-coder:7b | 4.7GB | 8GB | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | **Code explanation** |
| codellama:7b | 3.8GB | 8GB | ⭐⭐⭐ | ⭐⭐⭐⭐ | Code generation |
| llama3.2:3b | 2.0GB | 6GB | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | General use |
| gemma:2b | 1.6GB | 4GB | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | Quick answers |
| deepseek-coder:6.7b | 3.8GB | 8GB | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Code understanding |

---

## Troubleshooting

### "ollama: command not found"

**Fix**: Close and reopen your terminal (or restart VS Code)

Ollama installer adds to PATH, but terminals need to be restarted to see it.

### "Model not found"

**Fix**: Pull the model first:
```bash
ollama pull qwen2.5-coder:7b
```

### "Connection refused"

**Fix**: Make sure Ollama app is running in background.

You can start it with:
```bash
ollama serve
```

### Download is slow

**Fix**: 
- Close bandwidth-heavy apps
- Use wired connection if possible
- Try smaller model first (`gemma:2b`)

### Out of memory

**Fix**:
- Use smaller model (`gemma:2b` needs only 4GB)
- Close other applications
- Upgrade RAM if possible

---

## Quick Start Commands

```bash
# Download recommended model
ollama pull qwen2.5-coder:7b

# Test it directly
ollama run qwen2.5-coder:7b "Explain recursion"

# List downloaded models
ollama list

# Delete a model (if needed)
ollama rm gemma:2b

# Check Ollama status
ollama ps
```

---

## Configuration Examples

### Best for Code (Recommended)
```env
LLM_PROVIDER=ollama
OLLAMA_MODEL=qwen2.5-coder:7b
OLLAMA_BASE_URL=http://localhost:11434
```

### Best for Speed
```env
LLM_PROVIDER=ollama
OLLAMA_MODEL=gemma:2b
OLLAMA_BASE_URL=http://localhost:11434
```

### Hybrid (Groq with Ollama Fallback)
```env
# Primary: Fast cloud
LLM_PROVIDER=groq
GROQ_API_KEY=gsk_your_key
GROQ_MODEL=llama-3.3-70b-versatile

# Fallback: Local if Groq fails
OLLAMA_MODEL=qwen2.5-coder:7b
OLLAMA_BASE_URL=http://localhost:11434
```

The agent will automatically fall back to Ollama if Groq fails!

---

## Performance Tips

### 1. Use GPU Acceleration (if available)

Ollama automatically uses GPU if you have:
- NVIDIA GPU (CUDA)
- AMD GPU (ROCm)
- Apple Silicon (Metal)

### 2. Optimize for Your Hardware

**Low RAM (4-8 GB)**:
```env
OLLAMA_MODEL=gemma:2b
```

**Medium RAM (8-16 GB)**:
```env
OLLAMA_MODEL=qwen2.5-coder:7b
```

**High RAM (16+ GB)**:
```env
OLLAMA_MODEL=qwen2.5-coder:14b
```

### 3. Keep Ollama Running

For fastest responses, keep Ollama app running in background.

---

## Multi-Model Setup

You can have multiple models and switch between them:

```bash
# Download multiple models
ollama pull qwen2.5-coder:7b    # For code
ollama pull llama3.2:3b          # For general
ollama pull gemma:2b             # For speed

# List them
ollama list

# Switch in .env as needed
OLLAMA_MODEL=qwen2.5-coder:7b    # Change this
```

---

## Next Steps

1. **Pull your first model**: `ollama pull qwen2.5-coder:7b`
2. **Update `.env`**: Set `LLM_PROVIDER=ollama`
3. **Test it**: `python demo.py`
4. **Enjoy unlimited, private AI!** 🎉

---

**Need help? Common issues**:
- Terminal doesn't recognize `ollama` → Restart terminal
- Download stuck → Check internet, try smaller model
- Out of memory → Use `gemma:2b` instead
- Slow responses → Normal for CPU, much faster with GPU

**You're all set!** Ollama gives you unlimited, private AI explanations! 🦙
