"""Command-line interface for CodeGuru."""

import sys
import asyncio
import click
from pathlib import Path
from typing import Optional

# Import modules
from .ui import ui, console
from .explainer import explainer_engine
from .diagram_generator import diagram_generator
from .config import settings
from .errors import handle_error
from .utils import detect_language


@click.group()
@click.version_option(version="0.2.0")
def cli():
    """🧠 CodeGuru - Your AI Coding Mentor
    
    Explains code, generates diagrams, and teaches programming concepts.
    """
    pass


@cli.command()
@click.argument("file", type=click.Path(exists=True))
@click.option("--function", "-f", help="Explain specific function")
@click.option("--class-name", "-c", help="Explain specific class")
@click.option("--depth", "-d", type=click.Choice(["simple", "detailed", "deep", "all"]), 
              default="all", help="Detail level of explanation")
@click.option("--diagram/--no-diagram", default=True, help="Generate visual diagrams")
def explain(file: str, function: Optional[str], class_name: Optional[str], depth: str, diagram: bool):
    """Explain code from a file.
    
    Example:
      codeguru explain main.py
      codeguru explain utils.py --function process_data --depth detailed
    """
    try:
        path = Path(file)
        
        # UI Feedback
        ui.show_info(f"Analyzing {path.name}...")
        
        # Async logic wrapper
        async def run_analysis():
            with ui.create_progress("Generating explanation...") as progress:
                if function:
                    explanation = await explainer_engine.explain_function(path, function, depth)
                elif class_name:
                    explanation = await explainer_engine.explain_class(path, class_name, depth)
                else:
                    explanation = await explainer_engine.explain_file(path, depth)
                
                # Show explanation
                ui.show_explanation(explanation, f"Explanation: {path.name}")
                
                # Generate diagram
                if diagram and settings.generate_diagrams:
                    progress.update(progress.tasks[0].id, description="Generating diagram...")
                    if function:
                        mermaid = diagram_generator.generate_diagram_for_code(path, function, "flowchart")
                        ui.show_diagram(mermaid, f"Flowchart: {function}")
                    elif class_name:
                        mermaid = diagram_generator.generate_diagram_for_code(path, class_name, "class")
                        ui.show_diagram(mermaid, f"Class Diagram: {class_name}")
                    else:
                        # Full file diagram? Maybe complex. Try class diagram if classes exist.
                        from .code_analyzer import code_analyzer
                        structure = code_analyzer.analyze_file(str(path))
                        if structure.classes:
                            mermaid = diagram_generator.generate_class_diagram(structure)
                            ui.show_diagram(mermaid, f"Class Diagram: {path.name}")

        asyncio.run(run_analysis())
        
    except Exception as e:
        handle_error(e)


@cli.command()
@click.argument("concept_name")
def concept(concept_name: str):
    """Learn about a programming concept.
    
    Example:
      codeguru concept "recursion"
      codeguru concept "REST API"
    """
    try:
        ui.show_info(f"Researching: {concept_name}...")
        
        async def run_concept():
            explanation = await explainer_engine.explain_concept(concept_name)
            ui.show_explanation(explanation, f"Concept: {concept_name}")
            
        asyncio.run(run_concept())
        
    except Exception as e:
        handle_error(e)


@cli.command()
def chat():
    """Start interactive chat mode."""
    try:
        # Import chat module dynamically to avoid circular imports
        import importlib.util
        spec = importlib.util.spec_from_file_location("chat", "chat.py")
        chat_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(chat_module)
        
        # Run chat main
        chat_module.main()
        
    except Exception as e:
        handle_error(e)


@cli.command()
@click.argument("file", type=click.Path(exists=True))
def watch(file: str):
    """Watch a file and auto-explain changes."""
    try:
        # Import watcher dynamically
        from .watcher import start_file_watcher
        start_file_watcher(file)
        
    except ImportError:
        ui.show_error("Watchdog library not installed.", "Run: pip install watchdog")
    except Exception as e:
        handle_error(e)


@cli.command()
def demo():
    """Run the interactive demo."""
    try:
        # Import demo dynamically
        import importlib.util
        spec = importlib.util.spec_from_file_location("demo", "demo.py")
        demo_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(demo_module)
        
        # Run demo main
        demo_module.main()
        
    except Exception as e:
        handle_error(e)


@cli.command()
def check():
    """Check system configuration."""
    ui.show_info("Checking system configuration...")
    
    console.print(f"LLM Provider: [green]{settings.llm_provider}[/green]")
    
    if settings.llm_provider == "ollama":
        console.print(f"Ollama URL: {settings.ollama_base_url}")
        console.print(f"Ollama Model: {settings.ollama_model}")
    elif settings.llm_provider == "groq":
        key_status = "Configured" if settings.groq_api_key else "Missing"
        console.print(f"Groq API Key: {key_status}")

    console.print(f"Supported Languages: {', '.join(settings.supported_languages_list)}")
    ui.show_success("System check complete.")


if __name__ == "__main__":
    cli()
