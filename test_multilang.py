"""Test Java file parsing."""

# Force reload of config to pick up changes
import sys
if 'src.config' in sys.modules:
    del sys.modules['src.config']
if 'src.code_analyzer' in sys.modules:
    del sys.modules['src.code_analyzer']

from src.code_analyzer import code_analyzer
from rich.console import Console

console = Console()

console.print("\n[bold cyan]🧪 Testing Multi-Language Support[/bold cyan]\n")

# Test 1: Check supported languages
console.print(f"[green]✅ Parsers initialized: {sorted(code_analyzer.parsers.keys())}[/green]\n")

# Test 2: Parse Java file
try:
    console.print("[bold]Testing Java file parsing...[/bold]")
    structure = code_analyzer.analyze_file('tests/fixtures/Test.java')
    console.print(f"[green]✅ Java: Found {len(structure.classes)} classes, {len(structure.functions)} functions[/green]")
except Exception as e:
    console.print(f"[red]❌ Java parsing failed: {e}[/red]")

# Test 3: Parse Python file (should work)
try:
    console.print("\n[bold]Testing Python file parsing...[/bold]")
    structure = code_analyzer.analyze_file('test_parser.py')
    console.print(f"[green]✅ Python: Found {len(structure.classes)} classes, {len(structure.functions)} functions[/green]")
except Exception as e:
    console.print(f"[red]❌ Python parsing failed: {e}[/red]")

console.print("\n[cyan]Testing complete![/cyan]\n")
