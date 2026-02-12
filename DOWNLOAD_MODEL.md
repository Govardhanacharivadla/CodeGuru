# 🦙 Ollama Model Download - Visual Guide

## Method 1: Using Ollama App (Easiest!)

You already have the Ollama app open! Here's what to do:

### Step-by-Step:

1. **Look at the Ollama app window** you have open
2. **Find the search box** at the top (it says "Find model...")
3. **Type**: `qwen2.5-coder:7b`
4. **Look for it in the results**
5. **Click the cloud icon** (☁️ with arrow) next to it
6. **Wait for download** - You'll see a progress bar
7. **Done!** Model is ready when download completes

### What you'll see:
- Initially: Cloud icon (☁️↓) means "not downloaded"
- Downloading: Progress bar showing percentage
- Downloaded: Checkmark (✓) or solid icon

---

## Method 2: New Terminal Window

The `ollama` command won't work in your current terminal because PATH needs to refresh.

### Fix:
1. **Close VS Code completely**
2. **Reopen VS Code**
3. **Open new terminal**
4. **Try**: `ollama pull qwen2.5-coder:7b`

Or open a **fresh Command Prompt**:
1. Press **Windows key**
2. Type **cmd**
3. Press **Enter**
4. Run: `ollama pull qwen2.5-coder:7b`

---

## Method 3: Direct Download (Alternative)

If Ollama app is running in the background:

1. Open **new PowerShell** (not in VS Code)
2. Run:
```powershell
& "C:\Users\$env:USERNAME\AppData\Local\Programs\Ollama\ollama.exe" pull qwen2.5-coder:7b
```

---

## Verify Model is Downloaded

Once download completes, check:

### In Ollama App:
- Model will appear in your local models list
- Cloud icon changes to checkmark or solid icon

### In Terminal (new window):
```bash
ollama list
```

You should see `qwen2.5-coder:7b` in the list!

---

## After Download

### Test the model:
```bash
ollama run qwen2.5-coder:7b "What is async/await?"
```

### Switch Explainer Agent to use it:
```bash
python switch_provider.py
# Select option 2 (Ollama)
```

Or edit `.env` manually:
```env
LLM_PROVIDER=ollama
OLLAMA_MODEL=qwen2.5-coder:7b
```

### Test with Explainer Agent:
```bash
python demo.py
```

---

## Download Progress

Model size: **4.7 GB**

Approximate download times:
- Fast internet (100 Mbps): ~6 minutes
- Medium (50 Mbps): ~12 minutes  
- Slower (20 Mbps): ~30 minutes

**Tip**: Keep Ollama app open while downloading!

---

## What if Download Fails?

### Try a smaller model first:

**Gemma 2B** (only 1.6 GB):
```bash
ollama pull gemma:2b
```

Then use in `.env`:
```env
OLLAMA_MODEL=gemma:2b
```

It's faster to download and test, though slightly lower quality.

---

## I'm Stuck! Help!

### "Can't find Ollama app"
- Check system tray (bottom-right corner)
- Look for llama icon
- If not there, search for "Ollama" in Start menu

### "Download stuck at X%"
- Check internet connection
- Try pausing and resuming
- Restart Ollama app

### "Command not found" even in new terminal
- Ollama might not be installed correctly
- Download installer again from https://ollama.com
- Run installer as Administrator

---

## Current Status

✅ Ollama installed  
⏳ Model downloading (in progress)  
⏹️ Waiting for download to complete  
⏸️ Then configure Explainer Agent  
✅ Then test with `python demo.py`

---

**For now, keep using Groq!** It works perfectly. Ollama is just an optional extra for privacy and unlimited usage.

When the model finishes downloading, run:
```bash
python switch_provider.py
```

And select option 2 (Ollama)! 🦙
