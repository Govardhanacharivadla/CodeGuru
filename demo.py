#!/usr/bin/env python
"""CodeGuru Demo - Showcase all features beautifully."""

import sys
import asyncio
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from src.ui import ui, console
from src.code_analyzer import code_analyzer
from src.diagram_generator import diagram_generator
from src.explainer import explainer
from src.errors import handle_error


async def demo_parsing():
    """Demo: Multi-language code parsing."""
    console.print("\n[bold cyan]═══════= Demo 1: Multi-Language Code Parsing ═══════=[/bold cyan]\n")
    
    ui.show_info("CodeGuru can parse 6 languages: Python, JavaScript, TypeScript, Java, C, C++")
    
    # Demo with Java file
    ui.show_info("Analyzing Java code...")
    
    with ui.create_progress() as progress:
        task = progress.add_task("Parsing Java file...", total=100)
        
        structure = code_analyzer.analyze_file('tests/fixtures/Test.java')
        progress.update(task, advance=100)
    
    ui.show_success("Parsing complete!")
    ui.show_structure_table(structure)
    
    console.input("\n[dim]Press Enter to continue...[/dim]")


async def demo_explanation():
    """Demo: AI-powered explanations."""
    console.print("\n[bold cyan]═══════= Demo 2: AI-Powered Code Explanation ═══════=[/bold cyan]\n")
    
    ui.show_info("Let's explain a Python decorator...")
    
    # Sample code
    code = '''
@decorator
def greet(name):
    """Greet someone by name."""
    return f"Hello, {name}!"
'''.strip()
    
    ui.show_code(code, "python", "Sample Code")
    
    with ui.create_progress() as progress:
        task = progress.add_task("Generating explanation...", total=100)
        
        try:
            explanation = await explainer.explain_code(
                code=code,
                language="python",
                depth="simple"
            )
            progress.update(task, advance=100)
            
            ui.show_explanation(explanation, "Simple Explanation")
        except Exception as e:
            handle_error(e)
    
    console.input("\n[dim]Press Enter to continue...[/dim]")


async def demo_diagrams():
    """Demo: Automatic diagram generation."""
    console.print("\n[bold cyan]═══════= Demo 3: Automatic Diagram Generation ═══════=[/bold cyan]\n")
    
    ui.show_info("CodeGuru generates Mermaid diagrams automatically")
    
    with ui.create_progress() as progress:
        task = progress.add_task("Generating class diagram...", total=100)
        
        structure = code_analyzer.analyze_file('tests/fixtures/Calculator.cpp')
        progress.update(task, advance=50)
        
        diagram = diagram_generator.generate_class_diagram(structure)
        progress.update(task, advance=50)
    
    ui.show_diagram(diagram, "C++ Calculator Class Diagram")
    
    ui.show_info("Copy the code above to https://mermaid.live to visualize")
    
    console.input("\n[dim]Press Enter to continue...[/dim]")


async def demo_features():
    """Demo: Show all features at a glance."""
    console.print("\n[bold cyan]═══════= CodeGuru Features Overview ═══════=[/bold cyan]\n")
    
    from rich.table import Table
    
    table = Table(title="🌟 Features", show_header=True, header_style="bold cyan")
    table.add_column("Feature", style="cyan", width=25)
    table.add_column("Status", style="green", width=10)
    table.add_column("Description", style="dim", width=50)
    
    features = [
        ("Multi-Language Parsing", "✅", "Python, JS, TS, Java, C, C++ support"),
        ("AI Explanations", "✅", "Simple, Detailed, Deep, or All modes"),
        ("Diagram Generation", "✅", "Class diagrams, flowcharts, sequence diagrams"),
        ("Chat Mode", "✅", "Interactive Q&A with conversation history"),
        ("Dual LLM Support", "✅", "Groq (fast) or Ollama (private)"),
        ("Export Feature", "✅", "Save chats and explanations to Markdown"),
        ("Smart Caching", "✅", "Avoid re-explaining same code"),
        ("Beautiful CLI", "✅", "Rich formatting, syntax highlighting"),
    ]
    
    for feature, status, desc in features:
        table.add_row(feature, status, desc)
    
    console.print(table)
    
    console.print("\n[bold green]🎉 All features working perfectly![/bold green]\n")


async def main():
    """Run the complete demo."""
    ui.show_welcome()
    
    console.print("[bold]Welcome to CodeGuru - Your AI Coding Mentor![/bold]\n")
    console.print("This demo showcases CodeGuru's key features:\n")
    
    options = [
        ("1", "Multi-Language Code Parsing"),
        ("2", "AI-Powered Explanations"),
        ("3", "Automatic Diagram Generation"),
        ("4", "Features Overview"),
        ("5", "Run All Demos"),
        ("q", "Quit")
    ]
    
    ui.show_options_menu(options, "Choose a demo")
    
    choice = console.input("[bold cyan]Your choice:[/bold cyan] ").strip().lower()
    
    try:
        if choice == "1":
            await demo_parsing()
        elif choice == "2":
            await demo_explanation()
        elif choice == "3":
            await demo_diagrams()
        elif choice == "4":
            await demo_features()
        elif choice == "5":
            await demo_parsing()
            await demo_explanation()
            await demo_diagrams()
            await demo_features()
        elif choice == "q":
            ui.show_info("Goodbye! 👋")
            return
        else:
            ui.show_warning("Invalid choice. Running features overview...")
            await demo_features()
        
        # Final message
        console.print("\n[bold cyan]═══════════════════════════════════════[/bold cyan]")
        console.print("\n[bold]Want to try more?[/bold]")
        console.print("• Run: [cyan]python chat.py[/cyan] for interactive Q&A")
        console.print("• Run: [cyan]codeguru explain <file>[/cyan] to explain any code")
        console.print("• Check: [cyan]README.md[/cyan] for full documentation\n")
        
        ui.show_success("Demo complete!")
        
    except KeyboardInterrupt:
        console.print("\n[yellow]Demo interrupted.[/yellow]")
    except Exception as e:
        handle_error(e, verbose=False)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        console.print("\n[dim]Goodbye![/dim]")
