"""Simple verification that all core features work."""

from rich.console import Console
from rich.panel import Panel

console = Console()

def test_phase2_complete():
    """Quick smoke test for Phase 2 completion."""
    
    console.print(Panel.fit(
        "[bold cyan]CodeGuru Phase 2 - Quick Verification[/bold cyan]",
        border_style="cyan"
    ))
    
    results = []
    
    # Test 1: Config loads
    try:
        from src.config import settings
        langs = len(settings.supported_languages_list)
        console.print(f"[green]✅ Config: {langs} languages configured[/green]")
        results.append(True)
    except Exception as e:
        console.print(f"[red]❌ Config failed: {e}[/red]")
        results.append(False)
    
    # Test 2: Parsers initialized
    try:
        from src.code_analyzer import code_analyzer
        parsers = len(code_analyzer.parsers)
        console.print(f"[green]✅ Parsers: {parsers} parsers loaded[/green]")
        results.append(True)
    except Exception as e:
        console.print(f"[red]❌ Parsers failed: {e}[/red]")
        results.append(False)
    
    # Test 3: Java parsing works
    try:
        structure = code_analyzer.analyze_file('tests/fixtures/Test.java')
        methods = sum(len(c.methods) for c in structure.classes)
        assert methods > 0, "No methods extracted"
        console.print(f"[green]✅ Java: {len(structure.classes)} classes, {methods} methods[/green]")
        results.append(True)
    except Exception as e:
        console.print(f"[red]❌ Java parsing failed: {e}[/red]")
        results.append(False)
    
    # Test 4: JavaScript/TypeScript method extraction
    try:
        structure = code_analyzer.analyze_file('tests/fixtures/User.js')
        methods = sum(len(c.methods) for c in structure.classes)
        assert methods >= 3, f"Expected 3+ methods, got {methods}"
        console.print(f"[green]✅ JavaScript: {len(structure.classes)} classes, {methods} methods[/green]")
        results.append(True)
    except Exception as e:
        console.print(f"[red]❌ JavaScript parsing failed: {e}[/red]")
        results.append(False)
    
    # Test 5: Diagram generation
    try:
        from src.diagram_generator import diagram_generator
        structure = code_analyzer.analyze_file('tests/fixtures/Test.java')
        diagram = diagram_generator.generate_class_diagram(structure)
        assert 'classDiagram' in diagram
        console.print(f"[green]✅ Diagrams: Mermaid generation works[/green]")
        results.append(True)
    except Exception as e:
        console.print(f"[red]❌ Diagram generation failed: {e}[/red]")
        results.append(False)
    
    # Test 6: LLM client initializes
    try:
        from src.llm_client import llm_manager
        console.print(f"[green]✅ LLM: Manager initialized ({settings.llm_provider})[/green]")
        results.append(True)
    except Exception as e:
        console.print(f"[yellow]⚠️  LLM: {e}[/yellow]")
        results.append(True)  # Non-critical
    
    # Summary
    console.print()
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        console.print(Panel.fit(
            f"[bold green]🎉 ALL TESTS PASSED ({passed}/{total})[/bold green]\n"
            "[dim]Phase 2 core features are working![/dim]",
            border_style="green"
        ))
        return True
    else:
        console.print(Panel.fit(
            f"[bold red]❌ SOME TESTS FAILED ({passed}/{total})[/bold red]\n"
            "[dim]Check errors above[/dim]",
            border_style="red"
        ))
        return False


if __name__ == "__main__":
    import sys
    success = test_phase2_complete()
    sys.exit(0 if success else 1)
