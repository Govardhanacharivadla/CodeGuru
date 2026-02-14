"""Interactive Q&A chat mode for CodeGuru."""

import asyncio
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.prompt import Prompt

from src.llm_client import llm_manager

console = Console()

# Helpful hints for users
HINTS = [
    "💡 Try: 'Explain how decorators work in Python with examples'",
    "💡 Try: 'What's the difference between async and threading?'",
    "💡 Try: 'How do I structure a large Python project?'",
    "💡 Try: 'Explain list comprehensions vs generator expressions'",
    "💡 Try: 'What are Python context managers and when to use them?'",
    "💡 Try: 'How does garbage collection work in Python?'",
    "💡 Try: 'Explain the difference between == and is'",
    "💡 Try: 'What are metaclasses and when to use them?'",
    "💡 Try: 'How do I handle exceptions properly?'",
    "💡 Try: 'What's the best way to manage dependencies?'",
]

async def show_hints():
    """Display helpful hints for users."""
    console.print("\n[yellow]🤔 Not sure what to ask? Here are some ideas:[/yellow]\n")
    
    import random
    hints_to_show = random.sample(HINTS, min(5, len(HINTS)))
    
    for hint in hints_to_show:
        console.print(f"  {hint}")
    
    console.print("\n[dim]Type 'hints' anytime to see more suggestions[/dim]")
    console.print("[dim]Type 'exit' or 'quit' to end the session[/dim]\n")

async def chat_session():
    """Run an interactive Q&A chat session."""
    
    # Welcome message
    console.print(Panel.fit(
        "[bold cyan]🧠 CodeGuru Interactive Q&A[/bold cyan]\n\n"
        "Ask me anything about programming!\n"
        "I'll explain concepts, code patterns, and best practices.\n\n"
        "[dim]Type 'hints' for ideas, 'export' to save chat, or 'exit' to quit[/dim]",
        border_style="cyan"
    ))
    
    # Show initial hints
    await show_hints()
    
    # Chat history for context
    chat_history = []
    
    while True:
        # Get user question
        console.print("[bold green]You:[/bold green] ", end="")
        question = Prompt.ask("").strip()
        
        # Handle special commands
        if question.lower() in ['exit', 'quit', 'q']:
            console.print("\n[cyan]👋 Thanks for using CodeGuru! Keep learning! 🚀[/cyan]\n")
            break
        
        if question.lower() == 'hints':
            await show_hints()
            continue
        
        if question.lower() == 'clear':
            console.clear()
            chat_history = []
            console.print("[dim]Chat history cleared[/dim]\n")
            continue
        
        if question.lower().startswith('export'):
            # Usage: export filename.md
            parts = question.split()
            filename = parts[1] if len(parts) > 1 else "chat_history.md"
            if not filename.endswith('.md'):
                filename += '.md'
            
            # Ensure exports directory exists
            from pathlib import Path
            exports_dir = Path("exports")
            exports_dir.mkdir(exist_ok=True)
            
            output_path = exports_dir / filename
            
            try:
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write("# CodeGuru Chat Session\n\n")
                    for i in range(0, len(chat_history), 2):
                        if i+1 < len(chat_history):
                            f.write(f"## Q: {chat_history[i]}\n\n")
                            f.write(f"{chat_history[i+1]}\n\n")
                            f.write("---\n\n")
                console.print(f"\n[green]✅ Chat saved to {output_path}[/green]\n")
            except Exception as e:
                console.print(f"\n[red]❌ Failed to save: {e}[/red]\n")
            continue
        
        if not question:
            console.print("[yellow]Please ask a question![/yellow]\n")
            continue
        
        # Show thinking indicator
        console.print("\n[dim]🤔 Thinking...[/dim]")
        
        try:
            # Build context-aware prompt
            context = ""
            if chat_history:
                # Include last 2 exchanges for context
                recent = chat_history[-4:]  # Last 2 Q&A pairs
                context = "Previous conversation:\n"
                for i in range(0, len(recent), 2):
                    if i+1 < len(recent):
                        context += f"Q: {recent[i]}\nA: {recent[i+1][:200]}...\n"
                context += "\n"
            
            prompt = f"""{context}User Question: {question}

Please provide a clear, educational answer that:
1. Explains the concept simply
2. Provides concrete code examples
3. Mentions common pitfalls
4. Suggests best practices

Use markdown formatting for code blocks.
"""
            
            # Get response
            response = await llm_manager.generate(prompt)
            
            # Display response
            console.print()
            console.print(Panel(
                Markdown(response),
                title="[bold cyan]CodeGuru[/bold cyan]",
                border_style="cyan",
                padding=(1, 2)
            ))
            console.print()
            
            # Save to history
            chat_history.append(question)
            chat_history.append(response)
            
            # Keep history manageable (last 10 exchanges)
            if len(chat_history) > 20:
                chat_history = chat_history[-20:]
        
        except Exception as e:
            console.print(f"\n[red]❌ Error: {e}[/red]\n")
            console.print("[yellow]Try rephrasing your question or check your internet connection[/yellow]\n")

def main():
    """Main entry point."""
    try:
        asyncio.run(chat_session())
    except KeyboardInterrupt:
        console.print("\n\n[cyan]👋 Session ended. Keep learning! 🚀[/cyan]\n")

if __name__ == "__main__":
    main()
