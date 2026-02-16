"""File watcher for auto-explanation."""

import time
import asyncio
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from .ui import ui, console
from .explainer import explainer_engine
from .errors import handle_error
from .utils import debounce

class CodeChangeHandler(FileSystemEventHandler):
    """Handle file system events."""
    
    def __init__(self, file_path: Path):
        self.file_path = file_path.resolve()
        self.last_modified = 0
    
    def on_modified(self, event):
        """Called when a file is modified."""
        if Path(event.src_path).resolve() == self.file_path:
            current_time = time.time()
            if current_time - self.last_modified > 1.0:  # Debounce 1s
                self.last_modified = current_time
                self.trigger_explanation()

    def trigger_explanation(self):
        """Trigger explanation for the modified file."""
        ui.show_info(f"File changed: {self.file_path.name}")
        
        async def run_explanation():
            try:
                console.print("\n[dim]Re-analyzing code...[/dim]")
                explanation = await explainer_engine.explain_file(
                    str(self.file_path),
                    depth="simple"  # Keep it fast
                )
                
                # Clear screen (optional based on pref)
                # console.clear()
                
                ui.show_explanation(explanation, f"Updated Analysis: {self.file_path.name}")
            except Exception as e:
                handle_error(e)
        
        # Run async in sync context
        asyncio.run(run_explanation())


def start_file_watcher(file_path: str):
    """Start watching a file for changes."""
    path = Path(file_path)
    if not path.exists():
        ui.show_error(f"File not found: {file_path}")
        return

    event_handler = CodeChangeHandler(path)
    observer = Observer()
    observer.schedule(event_handler, path=str(path.parent), recursive=False)
    observer.start()
    
    ui.show_success(f"Watching {path.name} for changes...")
    ui.show_info("Press Ctrl+C to stop")
    
    try:
        # Trigger initial explanation
        event_handler.trigger_explanation()
        
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        observer.stop()
        ui.show_info("Stopped watching.")
    
    observer.join()
