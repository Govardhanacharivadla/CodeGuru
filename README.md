# 🧠 Explainer Agent

An AI-powered code explanation tool that teaches you **why** code works, not just **what** it does.

Unlike traditional code assistants that just describe code, Explainer Agent:
- 📚 **Teaches concepts** - Explains the underlying computer science principles
- 🎨 **Visualizes execution** - Auto-generates diagrams (flowcharts, sequence diagrams, call graphs)
- 🎓 **Multi-level explanations** - Simple → Detailed → Deep conceptual understanding
- 🔒 **100% Free & Private** - Runs locally using Ollama, no API costs

## ✨ Features

- **Multi-Level Explanations**
  - Simple (ELI5): Plain English explanation
  - Detailed: Step-by-step technical breakdown
  - Deep: Conceptual understanding with CS principles

- **Automatic Diagram Generation**
  - Control flow diagrams
  - Sequence diagrams for object interactions
  - Call graphs showing function dependencies
  - Class diagrams for OOP structures

- **Educational Focus**
  - Key concept definitions
  - Common mistakes to avoid
  - Best practices and patterns
  - Links to learning resources

- **Privacy-First Options**
  - Use Groq (cloud, free) for fastest responses
  - Use Ollama (local) for complete privacy
  - Automatic failover between providers

## 🚀 Quick Start

**Choose your preferred setup:**

### ⚡ Option 1: Groq (Fastest - 2 minutes)

**Best for**: Fastest setup, best quality, no downloads

1. **Get free API key** (no credit card):
   - Visit https://console.groq.com
   - Sign up with Google/GitHub
   - Create API key

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure**:
   ```bash
   # Edit .env file
   LLM_PROVIDER=groq
   GROQ_API_KEY=your_key_here
   ```

4. **Test**:
   ```bash
   python demo.py
   ```

✅ **Done!** You have instant AI explanations with 70B model!

---

### 🦙 Option 2: Ollama (Most Private - 10 minutes)

**Best for**: Privacy, unlimited usage, offline work

1. **Install Ollama**:
   - Download from https://ollama.com
   - Run installer
   - Restart terminal

2. **Pull a model**:
   ```bash
   # Best for code (recommended)
   ollama pull qwen2.5-coder:7b
   
   # OR faster download
   ollama pull gemma:2b
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure**:
   ```bash
   # Edit .env file
   LLM_PROVIDER=ollama
   OLLAMA_MODEL=qwen2.5-coder:7b
   ```

5. **Test**:
   ```bash
   python demo.py
   ```

✅ **Done!** You have unlimited, private AI explanations!

---

### 🔄 Switch Between Providers Anytime

```bash
python switch_provider.py
```

**Or manually edit `.env`**:
```env
# For Groq (fast, cloud)
LLM_PROVIDER=groq

# For Ollama (private, local)
LLM_PROVIDER=ollama
```

---

## 📚 Documentation

- **QUICK_REFERENCE.md** - Common commands and troubleshooting
- **OLLAMA_SETUP.md** - Complete Ollama guide
- **GROQ_SETUP.md** - Groq setup alternative
- **SUCCESS.md** - What's working, usage examples

## 📖 Usage

### Explain a Function

```bash
python -m src.cli explain --file utils.py --function process_data
```

### Explain an Entire File

```bash
python -m src.cli explain --file server.py
```

### Learn a Concept

```bash
python -m src.cli concept "event loop"
```

### Interactive Mode

```bash
python -m src.cli interactive
```

## 🎯 Example Output

```
📝 Function: async_fetch_data()

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔹 Simple Explanation:
This function fetches data from a URL without blocking other code from running.

🔹 Detailed Explanation:
1. Marks function as async, enabling non-blocking operations
2. Uses 'await' to pause execution until HTTP request completes
3. Returns parsed JSON data to caller
4. Can handle multiple requests concurrently

🔹 Deep Dive:
This implements asynchronous I/O using Python's event loop...

🎓 Key Concepts:
- Event Loop: Manages async task execution
- Async/Await: Syntactic sugar for coroutines
- Non-blocking I/O: Allows concurrent operations

⚠️  Common Mistakes:
- Forgetting 'await' keyword (returns coroutine object instead)
- Not running in event loop context
- Blocking operations inside async functions

📊 Execution Flow Diagram:
[Auto-generated Mermaid diagram showing async flow]
```

## 🏗️ Architecture

```
explainer-agent/
├── src/
│   ├── cli.py              # CLI interface
│   ├── code_analyzer.py    # Tree-sitter parsing
│   ├── context_builder.py  # Context extraction
│   ├── explainer.py        # Explanation generation
│   ├── diagram_generator.py # Mermaid diagrams
│   ├── llm_client.py       # Ollama/Groq integration
│   └── config.py           # Configuration
└── tests/                  # Test suite
```

## 🔧 Configuration

Edit `.env` to configure:

```env
# LLM Settings
LLM_PROVIDER=ollama  # ollama or groq
OLLAMA_MODEL=qwen2.5-coder:7b
GROQ_API_KEY=  # Optional, for faster responses

# Explanation Settings
EXPLANATION_DEPTH=all  # simple, detailed, deep, or all
GENERATE_DIAGRAMS=true
```

## 🎓 Supported Languages

- ✅ Python
- ✅ JavaScript/TypeScript
- ✅ Rust
- 🔜 Java, C++, Go (coming soon)

## 🤝 Contributing

This is an MVP prototype. Contributions welcome!

## 📄 License

MIT License

## 🌟 Why This Exists

Most AI coding tools just give you answers. This tool **teaches** you:
- The 'why' behind code design decisions
- Computer science concepts in practice
- How to think like an experienced developer

**Goal**: Make every developer 10x more capable by turning AI into a patient teacher.

## 🔮 Roadmap

- [ ] Web interface for better diagram rendering
- [ ] Interactive code exploration mode
- [ ] Support for more programming languages
- [ ] Domain expertise (compilers, OS, databases)
- [ ] Multi-codebase pattern learning
- [ ] Team knowledge sharing features

---

Built with ❤️ to make coding more accessible and educational.
