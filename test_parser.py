"""Test code parsing with tree-sitter."""

from src.code_analyzer import code_analyzer
from rich.console import Console
from rich.table import Table

console = Console()

# Test Python code
test_code = """
def hello_world(name: str) -> str:
    '''Greet someone by name.'''
    return f"Hello, {name}!"

class Calculator:
    '''Simple calculator class.'''
    
    def add(self, a: int, b: int) -> int:
        '''Add two numbers.'''
        return a + b
    
    def multiply(self, a: int, b: int) -> int:
        '''Multiply two numbers.'''
        return a * b
"""

def main():
    console.print("\n[bold cyan]🔍 Testing Tree-sitter Code Parser[/bold cyan]\n")
    
    if code_analyzer is None:
        console.print("[red]❌ Code analyzer not initialized![/red]")
        console.print("[yellow]Tree-sitter packages may not be installed properly[/yellow]")
        return
    
    console.print("[green]✓ Code analyzer initialized[/green]")
    
    # Test parsing
    console.print("\n[bold]Parsing Python code...[/bold]\n")
    
    try:
        structure = code_analyzer.analyze_code(test_code, "python")
        
        console.print(f"[green]✓ Parsing successful![/green]\n")
        
        # Show results
        console.print(f"[bold]Language:[/bold] {structure.language}")
        console.print(f"[bold]Complexity:[/bold] {structure.complexity_score}")
        console.print(f"[bold]Imports:[/bold] {len(structure.imports)}")
        
        # Functions table
        if structure.functions:
            console.print("\n[bold cyan]📝 Functions:[/bold cyan]")
            table = Table(show_header=True, header_style="bold cyan")
            table.add_column("Name")
            table.add_column("Lines")
            table.add_column("Parameters")
            
            for func in structure.functions:
                table.add_row(
                    func.name,
                    f"{func.start_line}-{func.end_line}",
                    ", ".join(func.parameters) if func.parameters else "none"
                )
            console.print(table)
        
        # Classes table
        if structure.classes:
            console.print("\n[bold magenta]🏛️  Classes:[/bold magenta]")
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Name")
            table.add_column("Lines")
            table.add_column("Methods")
            
            for cls in structure.classes:
                table.add_row(
                    cls.name,
                    f"{cls.start_line}-{cls.end_line}",
                    str(len(cls.methods))
                )
            console.print(table)
            
            # Show methods
            for cls in structure.classes:
                if cls.methods:
                    console.print(f"\n[dim]  Methods in {cls.name}:[/dim]")
                    for method in cls.methods:
                        params = ", ".join(method.parameters) if method.parameters else "none"
                        console.print(f"    • {method.name}({params})")
        
        console.print("\n[green]✅ Tree-sitter is working perfectly![/green]\n")
        
    except Exception as e:
        console.print(f"[red]❌ Parsing failed: {e}[/red]")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
