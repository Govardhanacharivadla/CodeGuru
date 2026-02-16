"""Beautiful CLI output formatting using Rich."""

from rich.console import Console
from rich.syntax import Syntax
from rich.panel import Panel
from rich.table import Table
from rich.markdown import Markdown
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.tree import Tree
from pathlib import Path

console = Console()


class CodeGuruUI:
    """Beautiful UI components for CodeGuru CLI."""
    
    @staticmethod
    def show_welcome():
        """Show welcome banner."""
        welcome = """
        [bold cyan]╔═══════════════════════════════════════╗[/bold cyan]
        [bold cyan]║[/bold cyan]   [bold white]🧠 CodeGuru - AI Coding Mentor[/bold white]    [bold cyan]║[/bold cyan]
        [bold cyan]╚═══════════════════════════════════════╝[/bold cyan]
        
        [dim]Your AI pair programmer that teaches[/dim]
        """
        console.print(welcome)
    
    @staticmethod
    def show_code(code: str, language: str, title: str = "Code"):
        """Display code with syntax highlighting."""
        syntax = Syntax(code, language, theme="monokai", line_numbers=True)
        console.print(Panel(syntax, title=f"📄 {title}", border_style="cyan"))
    
    @staticmethod
    def show_structure_table(structure):
        """Display code structure in a beautiful table."""
        table = Table(title="📊 Code Structure Analysis", show_header=True, header_style="bold cyan")
        table.add_column("Type", style="cyan", width=12)
        table.add_column("Name", style="green", width=25)
        table.add_column("Location", style="yellow", width=15)
        table.add_column("Details", style="dim")
        
        # Add classes
        for cls in structure.classes:
            methods_text = f"{len(cls.methods)} methods" if cls.methods else "No methods"
            table.add_row(
                "Class",
                cls.name,
                f"Lines {cls.start_line}-{cls.end_line}",
                methods_text
            )
            # Add methods as sub-items
            for method in cls.methods:
                table.add_row(
                    "  └─ Method",
                    f"  {method.name}()",
                    f"Lines {method.start_line}-{method.end_line}",
                    ""
                )
        
        # Add standalone functions
        for func in structure.functions:
            params_text = f"{len(func.parameters)} params" if func.parameters else "No params"
            table.add_row(
                "Function",
                f"{func.name}()",
                f"Lines {func.start_line}-{func.end_line}",
                params_text
            )
        
        # Add imports
        if structure.imports:
            table.add_row(
                "Imports",
                f"{len(structure.imports)} imports",
                "—",
                ", ".join(structure.imports[:3]) + ("..." if len(structure.imports) > 3 else "")
            )
        
        console.print(table)
        
        # Show complexity
        complexity_color = "green" if structure.complexity_score < 10 else "yellow" if structure.complexity_score < 20 else "red"
        console.print(f"\n[{complexity_color}]Complexity Score: {structure.complexity_score}[/{complexity_color}]")
    
    @staticmethod
    def show_explanation(explanation: str, title: str = "Explanation"):
        """Display explanation with markdown formatting."""
        md = Markdown(explanation)
        console.print(Panel(md, title=f"💡 {title}", border_style="green", padding=(1, 2)))
    
    @staticmethod
    def show_error(message: str, suggestion: str = None):
        """Display user-friendly error message."""
        error_panel = f"[bold red]❌ Error:[/bold red]\n{message}"
        if suggestion:
            error_panel += f"\n\n[bold yellow]💡 Suggestion:[/bold yellow]\n{suggestion}"
        console.print(Panel(error_panel, border_style="red", title="Error"))
    
    @staticmethod
    def show_success(message: str):
        """Display success message."""
        console.print(f"[bold green]✅ {message}[/bold green]")
    
    @staticmethod
    def show_info(message: str):
        """Display info message."""
        console.print(f"[cyan]ℹ️  {message}[/cyan]")
    
    @staticmethod
    def show_warning(message: str):
        """Display warning message."""
        console.print(f"[yellow]⚠️  {message}[/yellow]")
    
    @staticmethod
    def create_progress(description: str = "Processing..."):
        """Create a progress indicator."""
        return Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        )
    
    @staticmethod
    def show_file_tree(path: Path, max_depth: int = 3):
        """Display file tree structure."""
        tree = Tree(f"📁 {path.name}", guide_style="cyan")
        
        def add_tree_items(tree_node, directory, current_depth):
            if current_depth >= max_depth:
                return
            
            try:
                items = sorted(directory.iterdir(), key=lambda x: (x.is_file(), x.name))
                for item in items[:20]:  # Limit to 20 items
                    if item.is_file():
                        tree_node.add(f"📄 {item.name}")
                    elif item.is_dir() and not item.name.startswith('.'):
                        branch = tree_node.add(f"📁 {item.name}")
                        add_tree_items(branch, item, current_depth + 1)
            except PermissionError:
                tree_node.add("[dim]Permission denied[/dim]")
        
        if path.is_dir():
            add_tree_items(tree, path, 0)
        
        console.print(tree)
    
    @staticmethod
    def show_diagram(mermaid_code: str, title: str = "Diagram"):
        """Display Mermaid diagram code."""
        syntax = Syntax(mermaid_code, "mermaid", theme="monokai")
        console.print(Panel(
            syntax,
            title=f"🎨 {title}",
            subtitle="[dim]Copy to https://mermaid.live to visualize[/dim]",
            border_style="magenta"
        ))
    
    @staticmethod
    def show_options_menu(options: list[tuple[str, str]], title: str = "Choose an option"):
        """Display interactive menu."""
        console.print(f"\n[bold cyan]{title}:[/bold cyan]\n")
        for key, description in options:
            console.print(f"  [{key}] {description}")
        console.print()


# Global UI instance
ui = CodeGuruUI()
