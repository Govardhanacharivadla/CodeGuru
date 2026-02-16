"""Enhanced diagram testing with visual rendering options."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from src.diagram_generator import diagram_generator
from src.diagram_visualizer import display_diagram_options, auto_render_diagram
from src.code_analyzer import code_analyzer
from rich.console import Console

console = Console()

def test_all_diagrams_interactive():
    """Test diagram generation with interactive visualization."""
    
    console.print("\n[bold green]🎨 CodeGuru Diagram Generator - Visual Mode[/bold green]\n")
    
    # Test 1: Class Diagram (Java)
    console.print("[bold cyan]Test 1: Java Class Diagram[/bold cyan]")
    structure = code_analyzer.analyze_file('tests/fixtures/Test.java')
    if structure.classes:
        mermaid = diagram_generator.generate_class_diagram(structure)
        display_diagram_options(mermaid, "Java Class Diagram")
    
    # Test 2: Flowchart (Python)
    console.print("\n[bold cyan]Test 2: Python Function Flowchart[/bold cyan]")
    structure = code_analyzer.analyze_file('test_parser.py')
    if structure.functions:
        func = structure.functions[0]
        mermaid = diagram_generator.generate_flowchart(func, 'python')
        display_diagram_options(mermaid, f"Flowchart: {func.name}")
    
    # Test 3: Class Diagram (C++)
    console.print("\n[bold cyan]Test 3: C++ Class Diagram[/bold cyan]")
    structure = code_analyzer.analyze_file('tests/fixtures/Calculator.cpp')
    if structure.classes:
        mermaid = diagram_generator.generate_class_diagram(structure)
        display_diagram_options(mermaid, "C++ Calculator Class")
    
    console.print("\n[bold green]✅ All diagram tests complete![/bold green]\n")


def test_all_diagrams_auto():
    """Test diagram generation with automatic image generation."""
    
    console.print("\n[bold green]🎨 CodeGuru Diagram Generator - Auto Mode[/bold green]\n")
    
    diagrams_created = []
    
    # Test various languages
    test_files = [
        ('tests/fixtures/Test.java', 'Java HelloWorld'),
        ('tests/fixtures/Calculator.cpp', 'C++ Calculator'),
        ('tests/fixtures/User.js', 'JavaScript User'),
        ('tests/fixtures/ShoppingCart.ts', 'TypeScript ShoppingCart'),
    ]
    
    for file_path, title in test_files:
        try:
            console.print(f"\n[cyan]Processing: {title}[/cyan]")
            structure = code_analyzer.analyze_file(file_path)
            
            if structure.classes:
                mermaid = diagram_generator.generate_class_diagram(structure)
                img_path = auto_render_diagram(mermaid, title, mode="image")
                if img_path:
                    diagrams_created.append((title, img_path))
                    
        except Exception as e:
            console.print(f"[yellow]⚠️  Skipped {title}: {e}[/yellow]")
    
    console.print(f"\n[bold green]✅ Generated {len(diagrams_created)} diagram images![/bold green]")
    for title, path in diagrams_created:
        console.print(f"  📷 {title}: {path}")
    
    console.print()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--auto":
        test_all_diagrams_auto()
    else:
        test_all_diagrams_interactive()
