# 🎬 CodeGuru Demo Video Guide

Step-by-step guide to record an impressive demo for your GitHub README.

---

## 🎯 Demo Goals

Show CodeGuru's key features in **under 2 minutes**:
1. Interactive chat mode
2. Multi-level explanations  
3. Export feature
4. Beautiful CLI interface

---

## 🛠️ Tools You'll Need

### Option 1: GIF (Recommended for README)
- **Windows**: [ScreenToGif](https://www.screentogif.com/) (Free)
- **Settings**: 15 FPS, 720p resolution

### Option 2: MP4 Video
- **Windows**: OBS Studio (Free)
- **Upload to**: YouTube or convert to GIF

---

## 📝 Demo Script (90 seconds)

### Scene 1: Chat Mode (30s)

```bash
# Start chat
python chat.py
```

**Actions:**
1. Wait for welcome screen (shows beautifully formatted UI)
2. Type: `How do Python decorators work?`
3. Wait for response (shows markdown formatted answer)
4. Scroll through to show structure
5. Type: `Can you show me a real example?`
6. Show follow-up response

### Scene 2: Export Feature (15s)

**Actions:**
1. Type: `export my_learning.md`
2. Show success message
3. Open `exports/my_learning.md` in text editor (briefly)

### Scene 3: Hints & Commands (15s)

**Actions:**
1. Type: `hints`
2. Show 5 suggested questions
3. Type: `clear`
4. Show cleared history message

### Scene 4: Exit & Summary (10s)

**Actions:**
1. Type: `exit`
2. Show goodbye message

---

## 🎨 Recording Tips

### Before Recording
1. **Clear your terminal history**: `cls` or `clear`
2. **Resize terminal**: Make it fill 80% of screen
3. **Choose dark theme**: Looks better on GitHub
4. **Test run once**: Ensure no errors

### During Recording
1. **Type slowly**: Let viewers read
2. **Pause 2-3 seconds** after each output
3. **Don't rush**: Quality > speed
4. **If you make a mistake**: Stop, restart (it's quick!)

### After Recording
1. **Trim**: Remove dead time at start/end
2. **Optimize GIF size**: Use ScreenToGif's optimizer
3. **Test**: Upload to Imgur, check if it loads fast

---

## 📐 Recommended Settings

**ScreenToGif Settings:**
```
Frame Rate: 15 FPS
Size: 1280x720 (720p)
Duration: 60-90 seconds
File Size Target: < 5MB (important for README!)
```

**If file is too large:**
- Reduce FPS to 12
- Reduce resolution to 1024x576
- Shorten demo to 60 seconds

---

## 🎞️ Advanced: Multiple Demos

Create 3 short GIFs instead of 1 long one:

### demo-chat.gif (30s)
Just the chat interaction

### demo-export.gif (15s)
Showing export feature

### demo-hints.gif (15s)
Showing hints command

*Benefit: Faster loading, modular for documentation*

---

## 📤 Where to Upload

1. **GitHub**: Paste GIF directly in README (drag & drop)
2. **Backup**: Upload to Imgur (in case GitHub fails)
3. **Alternative**: YouTube unlisted video

---

## 📋 README Integration

Once you have your GIF, add to README.md:

```markdown
## 🎬 See It In Action

![CodeGuru Demo](docs/demo.gif)

*Interactive chat mode showing multi-level explanations*

[Watch full demo on YouTube →](your-youtube-link)
```

---

## ✅ Quality Checklist

Before publishing your demo:

- [ ] Terminal is clean and professional
- [ ] Text is readable (not too small)
- [ ] No personal information visible
- [ ] Shows key features clearly
- [ ] File size < 5MB (for fast loading)
- [ ] Smooth playback (no stuttering)
- [ ] Demonstrates real value (not just UI)

---

## 🎬 Quick Start Recording Now

1. Open ScreenToGif → Recorder
2. Position over terminal window
3. Hit Record (F7)
4. Run the script above
5. Hit Stop (F8)
6. Editor → Save As → Optimize → Export

**You're done in 3 minutes!** 🚀

---

*Pro tip: Record 2-3 takes and pick the best one. Your first take is usually not perfect.*
