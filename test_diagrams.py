"""Test diagram generation."""

from pathlib import Path
from src.diagram_generator import diagram_generator
from src.code_analyzer import code_analyzer
from rich.console import Console
from rich.syntax import Syntax

console = Console()

# Test code file
TEST_FILE = Path("tests/fixtures/sample_diagram.py")
TEST_FILE.parent.mkdir(parents=True, exist_ok=True)

TEST_CODE = """
class processor:
    def __init__(self, data):
        self.data = data

    def process(self):
        result = []
        for item in self.data:
            if item > 0:
                result.append(item * 2)
            else:
                result.append(0)
        return result

def main():
    data = [1, -5, 10, 0]
    p = processor(data)
    result = p.process()
    print(result)
"""

def main():
    console.print("\n[bold cyan]📊 Testing Diagram Generator[/bold cyan]\n")
    
    if code_analyzer is None:
        console.print("[red]❌ Code analyzer not initialized![/red]")
        return
        
    # Create test file
    TEST_FILE.write_text(TEST_CODE)
    console.print(f"[green]✓ Created test file: {TEST_FILE}[/green]")
    
    try:
        # Analyze file first
        console.print("\n[bold]1. Analyzing code structure...[/bold]")
        structure = code_analyzer.analyze_file(TEST_FILE)
        console.print(f"Found {len(structure.classes)} classes and {len(structure.functions)} top-level functions")
        
        # Test 1: Class Diagram
        console.print("\n[bold]2. Generating Class Diagram...[/bold]")
        class_diagram = diagram_generator.generate_class_diagram(structure)
        
        if class_diagram and "classDiagram" in class_diagram:
            console.print("[green]✓ Class diagram generated![/green]")
            console.print(Syntax(class_diagram, "mermaid", theme="monokai", line_numbers=True))
        else:
            console.print("[red]❌ Failed to generate class diagram[/red]")
            
        # Test 2: Flowchart for 'process' method
        console.print("\n[bold]3. Generating Flowchart for 'processor.process'...[/bold]")
        
        # We need to find the specific function info. code_analyzer.find_function handles methods too.
        # But wait, find_function takes structure and name.
        # In the test code, 'process' is a method of 'processor'.
        # code_analyzer.find_function implementation checks function list then class methods.
        
        func_info = code_analyzer.find_function(structure, "process")
        
        if func_info:
            flowchart = diagram_generator.generate_flowchart(func_info, "python")
            if flowchart and "flowchart TD" in flowchart:
                console.print(f"[green]✓ Flowchart generated for {func_info.name}![/green]")
                console.print(Syntax(flowchart, "mermaid", theme="monokai", line_numbers=True))
            else:
                console.print("[red]❌ Failed to generate flowchart[/red]")
        else:
            console.print("[red]❌ Could not find function 'process'[/red]")
            
        # Test 3: Sequence Diagram
        console.print("\n[bold]4. Generating Sequence Diagram for 'main'...[/bold]")
        func_main = code_analyzer.find_function(structure, "main")
        if func_main:
            seq_diagram = diagram_generator.generate_sequence_diagram(func_main)
            if seq_diagram and "sequenceDiagram" in seq_diagram:
                console.print("[green]✓ Sequence diagram generated![/green]")
                console.print(Syntax(seq_diagram, "mermaid", theme="monokai", line_numbers=True))
            else:
                console.print("[red]❌ Failed to generate sequence diagram[/red]")
        
        console.print("\n[green]✨ Diagram generation verified![/green]\n")
        
    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")
        import traceback
        traceback.print_exc()
    finally:
        # Clean up
        if TEST_FILE.exists():
            TEST_FILE.unlink()
            try:
                TEST_FILE.parent.rmdir()
            except OSError:
                pass  # Directory not empty

if __name__ == "__main__":
    main()
