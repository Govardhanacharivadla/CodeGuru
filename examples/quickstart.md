# 🧠 Explainer Agent - Quick Start Guide

## Installation

### 1. Install Ollama

Download and install from https://ollama.ai

```bash
# Verify installation
ollama --version
```

### 2. Pull Required Models

```bash
# Best for code explanation (recommended)
ollama pull qwen2.5-coder:7b

# Fast alternative for quick responses
ollama pull llama3.2:3b
```

### 3. Install Python Dependencies

```bash
# From the explainer-agent directory
pip install -r requirements.txt
```

### 4. Configure (Optional)

```bash
# Create .env file
cp .env.example .env

# Edit .env to customize settings
# Default values work fine for most users
```

## Basic Usage

### Explain a Function

```bash
python -m src.cli explain --file tests/fixtures/sample.py --function fetch_user_data
```

### Explain an Entire File

```bash
python -m src.cli explain --file tests/fixtures/sample.py
```

### Learn a Concept

```bash
python -m src.cli concept "event loop"
python -m src.cli concept "async await python"
```

### Interactive Mode

```bash
python -m src.cli interactive
```

### Check System Configuration

```bash
python -m src.cli check
```

## Usage Examples

### Simple Explanation

```bash
python -m src.cli explain --file sample.py --function my_function --depth simple
```

### Full Explanation with Diagrams

```bash
python -m src.cli explain --file sample.py --function my_function --depth all
```

### Without Diagrams

```bash
python -m src.cli explain --file sample.py --function my_function --no-diagram
```

## Troubleshooting

### Ollama Connection Failed

Make sure Ollama is running:

```bash
ollama serve
```

### Model Not Found

Pull the required model:

```bash
ollama pull qwen2.5-coder:7b
```

### File Too Large

Edit `.env` and increase `MAX_FILE_SIZE_KB`:

```env
MAX_FILE_SIZE_KB=1000
```

### Unsupported Language

Check supported languages:

```bash
python -m src.cli check
```

Add language in `.env`:

```env
SUPPORTED_LANGUAGES=python,javascript,typescript,rust,java
```

## Advanced Usage

### Using Groq API (Optional, Free Tier)

1. Sign up at https://console.groq.com (no credit card required)
2. Get API key
3. Edit `.env`:

```env
LLM_PROVIDER=groq
GROQ_API_KEY=your_api_key_here
```

Groq is faster but requires internet. Ollama is private and runs locally.

### Custom Models

Edit `.env` to use different Ollama models:

```env
# Faster but less accurate
OLLAMA_MODEL=llama3.2:3b

# Better quality but slower
OLLAMA_MODEL=qwen2.5-coder:14b
```

## Tips

1. **Start with simple explanations** - Use `--depth simple` first
2. **Use specific functions** - Explaining specific functions is better than entire files
3. **Generate diagrams** - Visualizations help understand complex code
4. **Interactive mode** - Great for exploring multiple concepts quickly
5. **Cache is enabled** - Repeated explanations are instant (cached for 1 hour)

## Next Steps

- Try explaining your own code
- Experiment with different explanation depths
- Use concept command to learn CS fundamentals
- Check out the architecture docs in the main README

Enjoy learning! 🚀
