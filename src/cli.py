"""Command-line interface for Explainer Agent."""

import asyncio
import sys
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.markdown import Markdown
from rich.table import Table

from .explainer import explainer_engine
from .diagram_generator import diagram_generator
from .config import settings
from .utils import logger, detect_language


console = Console()


def print_explanation(explanation, show_diagrams: bool = True):
    """Pretty-print explanation to console."""
    
    # Summary
    console.print("\n")
    console.print(Panel(
        f"[bold cyan]{explanation.summary}[/bold cyan]",
        title="📝 Summary",
        border_style="cyan"
    ))
    
    # Simple explanation
    if explanation.simple_explanation:
        console.print("\n[bold green]🔹 Simple Explanation (ELI5)[/bold green]")
        console.print(Markdown(explanation.simple_explanation))
    
    # Detailed explanation
    if explanation.detailed_explanation:
        console.print("\n[bold yellow]🔹 Detailed Explanation[/bold yellow]")
        console.print(Markdown(explanation.detailed_explanation))
    
    # Deep dive
    if explanation.deep_dive and explanation.deep_dive != "(See detailed explanation above)":
        console.print("\n[bold magenta]🔹 Deep Dive[/bold magenta]")
        console.print(Markdown(explanation.deep_dive))
    
    # Key concepts
    if explanation.key_concepts:
        console.print("\n[bold blue]🎓 Key Concepts[/bold blue]")
        table = Table(show_header=True, header_style="bold blue")
        table.add_column("Concept")
        table.add_column("Definition")
        
        for concept in explanation.key_concepts:
            table.add_row(concept.name, concept.definition)
        
        console.print(table)
    
    # Common mistakes
    if explanation.common_mistakes:
        console.print("\n[bold red]⚠️  Common Mistakes[/bold red]")
        for mistake in explanation.common_mistakes:
            console.print(f"  • {mistake}")
    
    # Best practices
    if explanation.best_practices:
        console.print("\n[bold green]✅ Best Practices[/bold green]")
        for practice in explanation.best_practices:
            console.print(f"  • {practice}")
    
    # Related resources
    if explanation.related_resources:
        console.print("\n[bold cyan]📚 Related Resources[/bold cyan]")
        for resource in explanation.related_resources:
            console.print(f"  • {resource}")


def print_mermaid_diagram(mermaid_code: str):
    """Print Mermaid diagram code."""
    if mermaid_code:
        console.print("\n[bold blue]📊 Generated Diagram (Mermaid)[/bold blue]")
        console.print("\n[dim]Copy this code to https://mermaid.live to visualize:[/dim]\n")
        
        syntax = Syntax(mermaid_code, "mermaid", theme="monokai", line_numbers=False)
        console.print(Panel(syntax, border_style="blue"))


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """🧠 Explainer Agent - AI-powered code explanation tool
    
    Explains code with multi-level depth and auto-generated diagrams.
    """
    pass


@cli.command()
@click.option("--file", "-f", required=True, help="Path to code file")
@click.option("--function", help="Specific function to explain")
@click.option("--class-name", help="Specific class to explain")
@click.option("--depth", type=click.Choice(["simple", "detailed", "deep", "all"]),
              default="all", help="Explanation depth")
@click.option("--diagram/--no-diagram", default=True, help="Generate diagrams")
def explain(file: str, function: Optional[str], class_name: Optional[str], 
            depth: str, diagram: bool):
    """Explain code from a file."""
    
    try:
        file_path = Path(file)
        if not file_path.exists():
            console.print(f"[red]Error: File not found: {file}[/red]")
            sys.exit(1)
        
        language = detect_language(file_path)
        if not language:
            console.print(f"[red]Error: Unsupported file type: {file}[/red]")
            console.print(f"[yellow]Supported: {', '.join(settings.supported_languages_list)}[/yellow]")
            sys.exit(1)
        
        console.print(f"\n[cyan]Analyzing {language} code...[/cyan]")
        
        # Run async explanation
        explanation = asyncio.run(_explain_async(file_path, function, class_name, depth))
        
        # Print explanation
        print_explanation(explanation, show_diagrams=diagram)
        
        # Generate diagram
        if diagram and settings.generate_diagrams:
            if function:
                mermaid = diagram_generator.generate_diagram_for_code(
                    file_path, function, "flowchart"
                )
                print_mermaid_diagram(mermaid)
            elif class_name:
                mermaid = diagram_generator.generate_diagram_for_code(
                    file_path, None, "class"
                )
                print_mermaid_diagram(mermaid)
        
        console.print("\n[green]✨ Done![/green]\n")
        
    except Exception as e:
        console.print(f"\n[red]Error: {e}[/red]")
        logger.exception("Explanation failed")
        sys.exit(1)


async def _explain_async(file_path, function, class_name, depth):
    """Async wrapper for explanation."""
    if function:
        return await explainer_engine.explain_function(file_path, function, depth)
    elif class_name:
        return await explainer_engine.explain_class(file_path, class_name, depth)
    else:
        return await explainer_engine.explain_file(file_path, depth)


@cli.command()
@click.argument("concept_name")
def concept(concept_name: str):
    """Learn about a programming concept."""
    
    try:
        console.print(f"\n[cyan]Researching concept: {concept_name}...[/cyan]\n")
        
        explanation = asyncio.run(explainer_engine.explain_concept(concept_name))
        
        console.print(Markdown(explanation))
        console.print("\n[green]✨ Done![/green]\n")
        
    except Exception as e:
        console.print(f"\n[red]Error: {e}[/red]")
        sys.exit(1)


@cli.command()
def interactive():
    """Start interactive mode."""
    console.print("\n[bold cyan]🧠 Explainer Agent - Interactive Mode[/bold cyan]")
    console.print("[dim]Type 'help' for commands, 'exit' to quit[/dim]\n")
    
    while True:
        try:
            user_input = console.input("[bold green]>[/bold green] ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ["exit", "quit", "q"]:
                console.print("\n[cyan]Goodbye! 👋[/cyan]\n")
                break
            
            if user_input.lower() == "help":
                console.print("""
[bold]Available commands:[/bold]
  explain <file> [--function <name>]  - Explain code
  concept <name>                      - Learn a concept
  exit                                - Quit

[bold]Examples:[/bold]
  explain utils.py --function process_data
  concept "event loop"
                """)
                continue
            
            # Parse command
            parts = user_input.split()
            cmd = parts[0].lower()
            
            if cmd == "explain" and len(parts) >= 2:
                file_path = parts[1]
                function_name = None
                
                if "--function" in parts:
                    idx = parts.index("--function")
                    if idx + 1 < len(parts):
                        function_name = parts[idx + 1]
                
                explanation = asyncio.run(_explain_async(file_path, function_name, None, "all"))
                print_explanation(explanation)
                
            elif cmd == "concept" and len(parts) >= 2:
                concept_name = " ".join(parts[1:])
                explanation = asyncio.run(explainer_engine.explain_concept(concept_name))
                console.print(Markdown(explanation))
            
            else:
                console.print("[yellow]Unknown command. Type 'help' for usage.[/yellow]")
        
        except KeyboardInterrupt:
            console.print("\n\n[cyan]Goodbye! 👋[/cyan]\n")
            break
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")


@cli.command()
def check():
    """Check system configuration."""
    console.print("\n[bold cyan]🔧 System Check[/bold cyan]\n")
    
    # Check LLM provider
    console.print(f"LLM Provider: [green]{settings.llm_provider}[/green]")
    
    if settings.llm_provider == "ollama":
        console.print(f"Ollama URL: {settings.ollama_base_url}")
        console.print(f"Ollama Model: {settings.ollama_model}")
        
        # Try to connect to Ollama
        try:
            from .llm_client import OllamaClient
            client = OllamaClient()
            console.print("[green]✅ Ollama connection successful[/green]")
        except Exception as e:
            console.print(f"[red]❌ Ollama connection failed: {e}[/red]")
            console.print("[yellow]Make sure Ollama is running: ollama serve[/yellow]")
    
    elif settings.llm_provider == "groq":
        if settings.groq_api_key:
            console.print("[green]✅ Groq API key configured[/green]")
        else:
            console.print("[red]❌ Groq API key not set[/red]")
    
    # Check supported languages
    console.print(f"\nSupported languages: {', '.join(settings.supported_languages_list)}")
    
    # Check diagram generation
    console.print(f"Diagram generation: {'[green]Enabled[/green]' if settings.generate_diagrams else '[yellow]Disabled[/yellow]'}")
    
    console.print("\n[green]✨ Check complete![/green]\n")


if __name__ == "__main__":
    cli()
