# 🧠 CodeGuru - AI Coding Mentor

> Transform code confusion into crystal-clear understanding

**CodeGuru** is an AI-powered coding mentor that doesn't just explain code—it teaches you **why** it works. Built for developers who want to truly understand what they're building.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Status: MVP](https://img.shields.io/badge/status-MVP-brightgreen.svg)]()

---

## ✨ What Makes CodeGuru Different?

Unlike traditional AI assistants that just describe code, CodeGuru:

- 📚 **Teaches Concepts** - Explains underlying computer science principles
- 🎓 **Multi-Level Learning** - Simple (ELI5) → Detailed → Deep conceptual
- 🎨 **Visual Learning** - Auto-generates diagrams (flowcharts, sequence diagrams)
- 🔒 **Privacy-First** - Choose between cloud (fast) or local (private)
- 💰 **100% Free** - No API costs, works with free Groq tier or local Ollama
- ⚡ **Lightning Fast** - Sub-second responses

---

## 🚀 Quick Start (2 minutes)

### Option 1: Groq (Fastest)

```bash
# 1. Get free API key from console.groq.com (no credit card!)
# 2. Clone and setup
git clone https://github.com/yourusername/CodeGuru.git
cd CodeGuru/explainer-agent
pip install -r requirements.txt

# 3. Configure
# Edit .env:
LLM_PROVIDER=groq
GROQ_API_KEY=your_key_here

# 4. Test
python demo.py
```

### Option 2: Ollama (Private & Unlimited)

```bash
# 1. Install Ollama from ollama.com
# 2. Pull model
ollama pull qwen2.5-coder:7b

# 3. Setup
pip install -r requirements.txt

# 4. Configure  
# Edit .env:
LLM_PROVIDER=ollama
OLLAMA_MODEL=qwen2.5-coder:7b

# 5. Test
python demo.py
```

---

## 🎯 Features

### 🎓 Educational Explanations
- **Simple Mode**: Plain English, ELI5 style
- **Detailed Mode**: Step-by-step technical breakdown  
- **Deep Mode**: CS concepts, patterns, best practices
- **All Mode**: Complete learning experience

### 🎨 Automatic Diagrams
- Control flow diagrams
- Sequence diagrams for OOP
- Call graphs showing dependencies
- Class diagrams for architecture

### 🔧 Multiple LLM Providers
- **Groq**: Fast cloud AI (70B model, free tier)
- **Ollama**: Private local AI (unlimited, offline)
- **Auto-failover**: Seamless switching

### 💡 Learning Focus
- Key concept definitions
- Common mistakes to avoid
- Best practices and patterns  
- Links to learning resources

---

## 📖 Usage Examples

### Explain a Code Snippet

```python
from src.llm_client import llm_manager
import asyncio

async def explain():
    code = """
    async def fetch_data(url):
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            return response.json()
    """
    
    prompt = f"Explain this code in detail:\n{code}"
    explanation = await llm_manager.generate(prompt)
    print(explanation)

asyncio.run(explain())
```

### Learn a Concept

```bash
python -c "
from src.llm_client import llm_manager
import asyncio

async def learn():
    response = await llm_manager.generate(
        'Explain dependency injection with Python examples'
    )
    print(response)

asyncio.run(learn())
"
```

### Switch Providers

```bash
python switch_provider.py
# Interactive menu to switch between Groq and Ollama
```

---

## 📚 Documentation

- **[README.md](README.md)** - This file
- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - Common commands
- **[OLLAMA_SETUP.md](OLLAMA_SETUP.md)** - Local AI setup
- **[GROQ_SETUP.md](GROQ_SETUP.md)** - Cloud AI setup
- **[SUCCESS.md](SUCCESS.md)** - Working features & examples
- **[COMPLETE_SETUP.md](COMPLETE_SETUP.md)** - Full documentation

---

## 🏗️ Project Structure

```
CodeGuru/
└── explainer-agent/
    ├── src/
    │   ├── cli.py              # Command-line interface
    │   ├── llm_client.py       # Groq/Ollama integration
    │   ├── explainer.py        # Explanation engine
    │   ├── code_analyzer.py    # Tree-sitter parsing
    │   ├── context_builder.py  # Context extraction
    │   ├── diagram_generator.py # Mermaid diagrams
    │   └── config.py           # Configuration
    ├── demo.py                 # Quick demo
    ├── switch_provider.py      # Provider switcher
    ├── requirements.txt        # Dependencies
    └── .env                    # Your configuration
```

---

## 🔧 Configuration

Edit `.env` to customize:

```env
# LLM Provider (groq or ollama)
LLM_PROVIDER=groq

# Groq Settings
GROQ_API_KEY=your_key_here
GROQ_MODEL=llama-3.3-70b-versatile

# Ollama Settings  
OLLAMA_MODEL=qwen2.5-coder:7b
OLLAMA_BASE_URL=http://localhost:11434

# Features
EXPLANATION_DEPTH=all
GENERATE_DIAGRAMS=true
```

---

## 🎯 Roadmap

### ✅ MVP (Complete)
- [x] Multi-level explanations
- [x] Groq + Ollama support
- [x] Beautiful CLI
- [x] Configuration system
- [x] Comprehensive docs

### 🚧 Short-term (This Month)
- [ ] Fix tree-sitter for full code parsing
- [ ] Enable automatic diagram generation
- [ ] Add more language support
- [ ] Improve prompt engineering

### 🔮 Long-term (Next Quarter)
- [ ] Web interface
- [ ] IDE plugins (VS Code, JetBrains)
- [ ] Project-wide analysis
- [ ] Code refactoring suggestions
- [ ] Knowledge base/memory

---

## 🤝 Contributing

We're building CodeGuru together! Contributions welcome:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit your changes**: `git commit -m 'Add amazing feature'`
4. **Push to branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request**

---

## 📊 Tech Stack

- **Python 3.11+** - Core language
- **Groq API** - Fast cloud LLM (free tier)
- **Ollama** - Local LLM runtime
- **Tree-sitter** - Code parsing
- **Rich** - Terminal UI
- **Pydantic** - Configuration
- **AsyncIO** - Async operations

---

## 🎓 Supported Languages

- ✅ Python
- ✅ JavaScript/TypeScript  
- 🔜 Java, C++, Go, Rust (coming soon)

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

## 🌟 Why CodeGuru?

**Most AI coding tools give you answers. CodeGuru teaches you.**

Our goal: Make every developer 10x more capable by turning AI into a patient, knowledgeable mentor.

---

## 💡 Inspiration

Built with the belief that:
- Understanding > Memorizing
- Teaching > Telling
- Concepts > Code
- Learning > Copying

---

## 🙏 Acknowledgments

- [Groq](https://groq.com) for blazing-fast free API
- [Ollama](https://ollama.com) for local LLM runtime
- [Tree-sitter](https://tree-sitter.github.io/) for code parsing
- [Rich](https://rich.readthedocs.io/) for beautiful terminal UI

---

## 📞 Support & Feedback

- **Issues**: [GitHub Issues](https://github.com/yourusername/CodeGuru/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/CodeGuru/discussions)
- **Email**: your.email@example.com

---

## 🚀 Daily Development

We're building this in public!  
Follow along for daily updates and improvements.

**Star the repo** ⭐ to stay updated!

---

**Built with ❤️ to make coding more accessible and educational.**

```
Made by Durga Prasad Chary
```
