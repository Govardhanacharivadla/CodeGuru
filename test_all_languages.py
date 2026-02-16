"""Comprehensive multi-language parsing test."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from src.code_analyzer import code_analyzer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

def test_language(file_path: str, language: str, expected_classes: int = None):
    """Test parsing a single language file."""
    try:
        structure = code_analyzer.analyze_file(file_path)
        
        # Create results table
        table = Table(title=f"{language.upper()} Parsing Results", show_header=True)
        table.add_column("Metric", style="cyan")
        table.add_column("Count", style="green", justify="right")
        table.add_column("Details", style="yellow")
        
        table.add_row("Classes", str(len(structure.classes)), 
                     ", ".join(c.name for c in structure.classes) if structure.classes else "None")
        table.add_row("Functions", str(len(structure.functions)),
                     ", ".join(f.name for f in structure.functions) if structure.functions else "None")
        table.add_row("Imports", str(len(structure.imports)),
                     str(len(structure.imports)) + " imports")
        
        # Show methods per class
        total_methods = sum(len(c.methods) for c in structure.classes)
        table.add_row("Total Methods", str(total_methods), 
                     " | ".join(f"{c.name}: {len(c.methods)}" for c in structure.classes) if structure.classes else "None")
        
        console.print(table)
        
        # Detailed class info
        for cls in structure.classes:
            if cls.methods:
                console.print(f"\n  [cyan]Class [bold]{cls.name}[/bold] methods:[/cyan]")
                for method in cls.methods:
                    console.print(f"    • {method.name}() [dim](lines {method.start_line}-{method.end_line})[/dim]")
        
        # Detailed function info
        for func in structure.functions:
            console.print(f"\n  [cyan]Function [bold]{func.name}[/bold]()[/cyan] [dim](lines {func.start_line}-{func.end_line})[/dim]")
        
        # Validation
        status = "✅ PASS"
        if expected_classes is not None and len(structure.classes) != expected_classes:
            status = f"⚠️  Expected {expected_classes} classes, got {len(structure.classes)}"
        
        console.print(f"\n[bold green]{status}[/bold green]\n")
        return True
        
    except Exception as e:
        console.print(f"[bold red]❌ FAIL: {e}[/bold red]\n")
        return False


def run_all_tests():
    """Run comprehensive tests for all languages."""
    
    console.print(Panel.fit(
        "[bold cyan]CodeGuru Multi-Language Parser Test Suite[/bold cyan]\n"
        "Testing: Python, JavaScript, TypeScript, Java, C, C++",
        border_style="cyan"
    ))
    
    tests = [
        ("Python", "test_parser.py", None),
        ("Java", "tests/fixtures/Test.java", 1),
        ("C++", "tests/fixtures/Calculator.cpp", 1),
        ("C", "tests/fixtures/math_utils.c", 0),  # C doesn't have classes
        ("JavaScript", "tests/fixtures/User.js", 1),
        ("TypeScript", "tests/fixtures/ShoppingCart.ts", 1),
    ]
    
    results = {}
    
    for lang, file, expected in tests:
        console.print(f"\n[bold yellow]{'='*70}[/bold yellow]")
        console.print(f"[bold yellow]Testing: {lang}[/bold yellow]")
        console.print(f"[bold yellow]{'='*70}[/bold yellow]\n")
        
        if not Path(file).exists():
            console.print(f"[red]❌ File not found: {file}[/red]\n")
            results[lang] = False
            continue
        
        results[lang] = test_language(file, lang, expected)
    
    # Summary
    console.print("\n" + "="*70)
    console.print("[bold cyan]SUMMARY[/bold cyan]")
    console.print("="*70 + "\n")
    
    summary_table = Table(show_header=True)
    summary_table.add_column("Language", style="cyan")
    summary_table.add_column("Status", style="bold")
    summary_table.add_column("File", style="dim")
    
    for (lang, file, _), passed in zip(tests, results.values()):
        status = "[green]✅ PASS[/green]" if passed else "[red]❌ FAIL[/red]"
        summary_table.add_row(lang, status, file)
    
    console.print(summary_table)
    
    passed_count = sum(1 for v in results.values() if v)
    total_count = len(results)
    
    console.print(f"\n[bold]Results: {passed_count}/{total_count} tests passed[/bold]")
    
    if passed_count == total_count:
        console.print("[bold green]🎉 All tests passed![/bold green]\n")
    else:
        console.print("[bold yellow]⚠️  Some tests failed[/bold yellow]\n")
    
    return passed_count == total_count


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
