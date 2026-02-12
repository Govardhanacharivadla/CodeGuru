"""Demo: Explain code with the Explainer Agent."""

import asyncio
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

from src.llm_client import llm_manager

console = Console()

SAMPLE_CODE = """
async def fetch_user_data(user_id: int) -> dict:
    '''Fetch user data from API asynchronously.'''
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://api.example.com/users/{user_id}")
        response.raise_for_status()
        return response.json()
"""

async def demo():
    console.print("\n[bold cyan]🧠 Explainer Agent - Live Demo[/bold cyan]\n")
    
    # Show code
    console.print(Panel(
        SAMPLE_CODE,
        title="[bold]Sample Code to Explain[/bold]",
        border_style="blue"
    ))
    
    console.print("\n[yellow]⏳ Generating explanation...[/yellow]\n")
    
    # Create prompt
    prompt = f"""Explain this Python code in a clear, educational way:

```python
{SAMPLE_CODE}
```

Provide:
1. **Summary** (1 sentence)
2. **Simple Explanation** (explain like I'm 5)
3. **How it works** (technical details)
4. **Key concepts** (what should the reader learn?)
5. **Best practices** (what's good about this code?)

Make it educational and engaging!"""

    # Get explanation
    explanation = await llm_manager.generate(prompt)
    
    # Display
    console.print(Panel(
        Markdown(explanation),
        title="[bold green]📚 Explanation[/bold green]",
        border_style="green"
    ))
    
    console.print("\n[bold green]✅ Demo complete![/bold green]\n")
    console.print("[dim]The Explainer Agent is working correctly with Groq! 🚀[/dim]\n")

if __name__ == "__main__":
    asyncio.run(demo())
