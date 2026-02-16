"""Enhanced diagram generator with visual rendering support."""

import base64
import webbrowser
from pathlib import Path
from typing import Optional, Literal
from urllib.parse import quote
import httpx

from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

console = Console()


class DiagramVisualizer:
    """Renders Mermaid diagrams as images."""
    
    @staticmethod
    def render_to_png(mermaid_code: str, output_path: Optional[Path] = None) -> Optional[Path]:
        """Render Mermaid code to PNG using mermaid.ink API."""
        try:
            # Encode Mermaid code for URL
            encoded = base64.b64encode(mermaid_code.encode('utf-8')).decode('utf-8')
            
            # Use mermaid.ink (free service)
            url = f"https://mermaid.ink/img/{encoded}"
            
            console.print(f"\n[cyan]📷 Generating visual diagram...[/cyan]")
            
            # Download the image
            response = httpx.get(url, timeout=10.0)
            response.raise_for_status()
            
            # Save to file
            if output_path is None:
                output_path = Path("diagrams") / "diagram.png"
            
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_bytes(response.content)
            
            console.print(f"[green]✅ Diagram saved to: {output_path}[/green]")
            return output_path
            
        except Exception as e:
            console.print(f"[yellow]⚠️  Could not generate visual: {e}[/yellow]")
            console.print("[yellow]💡 You can copy the Mermaid code to https://mermaid.live[/yellow]")
            return None
    
    @staticmethod
    def open_in_browser(mermaid_code: str):
        """Open diagram in browser using mermaid.live."""
        try:
            # URL encode the mermaid code
            encoded = quote(mermaid_code)
            
            # Create mermaid.live URL with state
            state = {
                "code": mermaid_code,
                "mermaid": {"theme": "default"},
                "updateEditor": True
            }
            import json
            state_json = json.dumps(state)
            state_b64 = base64.b64encode(state_json.encode()).decode()
            
            url = f"https://mermaid.live/edit#pako:{state_b64}"
            
            console.print(f"\n[cyan]🌐 Opening diagram in browser...[/cyan]")
            webbrowser.open(url)
            console.print("[green]✅ Opened in default browser[/green]")
            
        except Exception as e:
            console.print(f"[yellow]⚠️  Could not open browser: {e}[/yellow]")
            manual_url = "https://mermaid.live"
            console.print(f"[yellow]💡 Manually open: {manual_url} and paste the code[/yellow]")


def display_diagram_options(mermaid_code: str, title: str = "Diagram"):
    """Display diagram with user choice for format."""
    
    # Show the diagram panel
    console.print(f"\n[bold cyan]{'='*60}[/bold cyan]")
    console.print(Panel(
        Markdown(f"```mermaid\n{mermaid_code}\n```"),
        title=f"🎨 {title}",
        border_style="cyan"
    ))
    
    console.print("\n[bold yellow]Choose how to view this diagram:[/bold yellow]")
    console.print("  [1] Copy Mermaid code (shown above)")
    console.print("  [2] Save as PNG image")
    console.print("  [3] Open in browser (mermaid.live)")
    console.print("  [4] All of the above")
    console.print("  [Enter] Skip")
    
    choice = console.input("\n[bold cyan]Your choice (1-4):[/bold cyan] ").strip()
    
    if choice == "1":
        console.print("\n[green]✅ Mermaid code is shown above. Copy and paste to mermaid.live[/green]")
        console.print(f"[dim]Copy from the code block above[/dim]")
        
    elif choice == "2":
        output_path = Path("diagrams") / f"{title.lower().replace(' ', '_')}.png"
        result = DiagramVisualizer.render_to_png(mermaid_code, output_path)
        if result:
            console.print(f"\n[green]✅ Image saved! Open: {result}[/green]")
            
    elif choice == "3":
        DiagramVisualizer.open_in_browser(mermaid_code)
        
    elif choice == "4":
        # Do all
        console.print("\n[cyan]📋 Mermaid code (shown above)[/cyan]")
        
        output_path = Path("diagrams") / f"{title.lower().replace(' ', '_')}.png"
        DiagramVisualizer.render_to_png(mermaid_code, output_path)
        
        DiagramVisualizer.open_in_browser(mermaid_code)
        
    else:
        console.print("[dim]Skipped visualization[/dim]")
    
    return mermaid_code


def auto_render_diagram(mermaid_code: str, title: str = "Diagram", 
                        mode: Literal["code", "image", "browser", "all"] = "code") -> Optional[Path]:
    """Automatically render diagram based on mode (non-interactive)."""
    
    if mode == "code":
        console.print(Panel(
            Markdown(f"```mermaid\n{mermaid_code}\n```"),
            title=f"🎨 {title}",
            border_style="cyan"
        ))
        
    elif mode == "image":
        output_path = Path("diagrams") / f"{title.lower().replace(' ', '_')}.png"
        return DiagramVisualizer.render_to_png(mermaid_code, output_path)
        
    elif mode == "browser":
        DiagramVisualizer.open_in_browser(mermaid_code)
        
    elif mode == "all":
        console.print(Panel(
            Markdown(f"```mermaid\n{mermaid_code}\n```"),
            title=f"🎨 {title}",
            border_style="cyan"
        ))
        output_path = Path("diagrams") / f"{title.lower().replace(' ', '_')}.png"
        DiagramVisualizer.render_to_png(mermaid_code, output_path)
        DiagramVisualizer.open_in_browser(mermaid_code)
        return output_path
    
    return None
