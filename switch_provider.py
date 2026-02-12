"""Helper script to switch between LLM providers."""

import sys
from pathlib import Path
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich.table import Table

console = Console()

def read_env():
    """Read current .env file."""
    env_file = Path(".env")
    if not env_file.exists():
        return {}
    
    env_vars = {}
    for line in env_file.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, value = line.split("=", 1)
            env_vars[key.strip()] = value.strip()
    return env_vars

def write_env(env_vars, provider):
    """Write updated .env file."""
    lines = []
    
    # Header
    lines.append("# LLM Provider Configuration")
    lines.append(f"LLM_PROVIDER={provider}")
    lines.append("")
    
    if provider == "groq":
        lines.append("# Groq Settings (Free API)")
        lines.append(f"GROQ_API_KEY={env_vars.get('GROQ_API_KEY', 'your_key_here')}")
        lines.append(f"GROQ_MODEL={env_vars.get('GROQ_MODEL', 'llama-3.3-70b-versatile')}")
        lines.append("")
        lines.append("# Ollama Settings (Local LLM - fallback)")
    else:
        lines.append("# Ollama Settings (Local LLM)")
    
    lines.append(f"OLLAMA_BASE_URL={env_vars.get('OLLAMA_BASE_URL', 'http://localhost:11434')}")
    lines.append(f"OLLAMA_MODEL={env_vars.get('OLLAMA_MODEL', 'qwen2.5-coder:7b')}")
    lines.append("")
    
    if provider == "ollama":
        lines.append("# Groq Settings (Free API - not used)")
        lines.append(f"GROQ_API_KEY={env_vars.get('GROQ_API_KEY', '')}")
        lines.append(f"GROQ_MODEL={env_vars.get('GROQ_MODEL', 'llama-3.3-70b-versatile')}")
        lines.append("")
    
    # Other settings
    lines.append("# Explanation Settings")
    lines.append(f"EXPLANATION_DEPTH={env_vars.get('EXPLANATION_DEPTH', 'all')}")
    lines.append(f"GENERATE_DIAGRAMS={env_vars.get('GENERATE_DIAGRAMS', 'true')}")
    lines.append(f"MAX_DIAGRAM_NODES={env_vars.get('MAX_DIAGRAM_NODES', '50')}")
    lines.append("")
    lines.append("# Code Analysis Settings")
    lines.append(f"MAX_FILE_SIZE_KB={env_vars.get('MAX_FILE_SIZE_KB', '500')}")
    lines.append(f"SUPPORTED_LANGUAGES={env_vars.get('SUPPORTED_LANGUAGES', 'python,javascript,typescript,rust')}")
    lines.append("")
    lines.append("# Cache Settings")
    lines.append(f"ENABLE_CACHE={env_vars.get('ENABLE_CACHE', 'true')}")
    lines.append(f"CACHE_TTL_SECONDS={env_vars.get('CACHE_TTL_SECONDS', '3600')}")
    lines.append("")
    lines.append("# Logging")
    lines.append(f"LOG_LEVEL={env_vars.get('LOG_LEVEL', 'INFO')}")
    
    Path(".env").write_text("\n".join(lines))

def show_current_config():
    """Display current configuration."""
    env_vars = read_env()
    
    console.print("\n[bold cyan]📋 Current Configuration[/bold cyan]\n")
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Setting", style="cyan")
    table.add_column("Value", style="green")
    
    current_provider = env_vars.get("LLM_PROVIDER", "not set")
    table.add_row("Provider", current_provider)
    
    if current_provider == "groq":
        api_key = env_vars.get("GROQ_API_KEY", "not set")
        masked_key = api_key[:10] + "..." if len(api_key) > 10 else api_key
        table.add_row("Groq API Key", masked_key)
        table.add_row("Groq Model", env_vars.get("GROQ_MODEL", "not set"))
    else:
        table.add_row("Ollama URL", env_vars.get("OLLAMA_BASE_URL", "not set"))
        table.add_row("Ollama Model", env_vars.get("OLLAMA_MODEL", "not set"))
    
    console.print(table)
    console.print()

def switch_to_groq():
    """Switch to Groq provider."""
    console.print("\n[bold yellow]🌩️  Switching to Groq (Cloud API)[/bold yellow]\n")
    
    env_vars = read_env()
    
    # Check if API key exists
    api_key = env_vars.get("GROQ_API_KEY", "")
    if not api_key or api_key == "your_key_here":
        console.print("[yellow]⚠️  Groq API key not found![/yellow]\n")
        console.print("Get your free API key from: [link]https://console.groq.com[/link]\n")
        
        api_key = Prompt.ask("Enter your Groq API key (or press Enter to skip)")
        if api_key:
            env_vars["GROQ_API_KEY"] = api_key
        else:
            console.print("[red]❌ Cannot switch to Groq without API key[/red]")
            return False
    
    write_env(env_vars, "groq")
    
    console.print("\n[green]✅ Switched to Groq![/green]")
    console.print("[dim]Fast cloud-based AI with 70B parameter model[/dim]\n")
    return True

def switch_to_ollama():
    """Switch to Ollama provider."""
    console.print("\n[bold yellow]🦙 Switching to Ollama (Local AI)[/bold yellow]\n")
    
    env_vars = read_env()
    
    # Check if model is specified
    current_model = env_vars.get("OLLAMA_MODEL", "")
    
    if not current_model:
        console.print("[yellow]⚠️  No Ollama model specified![/yellow]\n")
        console.print("Popular models:")
        console.print("  1. qwen2.5-coder:7b (recommended for code)")
        console.print("  2. gemma:2b (fastest)")
        console.print("  3. llama3.2:3b (balanced)")
        console.print("  4. codellama:7b (code generation)\n")
        
        model = Prompt.ask(
            "Enter model name",
            default="qwen2.5-coder:7b"
        )
        env_vars["OLLAMA_MODEL"] = model
        
        console.print(f"\n[yellow]💡 Remember to pull the model:[/yellow]")
        console.print(f"   [cyan]ollama pull {model}[/cyan]\n")
    
    write_env(env_vars, "ollama")
    
    console.print("\n[green]✅ Switched to Ollama![/green]")
    console.print("[dim]Private, unlimited local AI[/dim]\n")
    return True

def main():
    """Main menu."""
    console.print(Panel.fit(
        "[bold cyan]🔄 LLM Provider Switcher[/bold cyan]\n\n"
        "Easily switch between Groq (cloud) and Ollama (local)",
        border_style="cyan"
    ))
    
    show_current_config()
    
    # Menu
    console.print("[bold]Choose an option:[/bold]\n")
    console.print("  [cyan]1.[/cyan] Switch to Groq (fast, cloud)")
    console.print("  [cyan]2.[/cyan] Switch to Ollama (private, local)")
    console.print("  [cyan]3.[/cyan] View current config")
    console.print("  [cyan]4.[/cyan] Exit\n")
    
    choice = Prompt.ask("Select option", choices=["1", "2", "3", "4"], default="3")
    
    if choice == "1":
        if switch_to_groq():
            console.print("\n[bold green]Ready to use![/bold green] Run: [cyan]python demo.py[/cyan]\n")
    elif choice == "2":
        if switch_to_ollama():
            console.print("\n[bold green]Ready to use![/bold green] Run: [cyan]python demo.py[/cyan]\n")
    elif choice == "3":
        show_current_config()
    else:
        console.print("\n[cyan]Goodbye! 👋[/cyan]\n")

if __name__ == "__main__":
    main()
