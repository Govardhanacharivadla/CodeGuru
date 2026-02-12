"""Utility functions for file I/O, formatting, and logging."""

import logging
import hashlib
from pathlib import Path
from typing import Optional
from rich.console import Console
from rich.logging import RichHandler

from .config import settings


# Rich console for beautiful output
console = Console()


def setup_logging() -> logging.Logger:
    """Set up logging with rich handler."""
    logging.basicConfig(
        level=settings.log_level,
        format="%(message)s",
        handlers=[RichHandler(rich_tracebacks=True, console=console)]
    )
    return logging.getLogger("explainer")


logger = setup_logging()


def read_file(file_path: str | Path) -> str:
    """Read file contents with error handling."""
    try:
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        file_size_kb = path.stat().st_size / 1024
        if file_size_kb > settings.max_file_size_kb:
            raise ValueError(
                f"File too large: {file_size_kb:.1f}KB "
                f"(max: {settings.max_file_size_kb}KB)"
            )
        
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        raise ValueError(f"Cannot decode file: {file_path} (not UTF-8)")


def get_file_hash(content: str) -> str:
    """Generate hash of file content for caching."""
    return hashlib.sha256(content.encode()).hexdigest()[:16]


def detect_language(file_path: str | Path) -> Optional[str]:
    """Detect programming language from file extension."""
    path = Path(file_path)
    ext_to_lang = {
        ".py": "python",
        ".js": "javascript",
        ".ts": "typescript",
        ".tsx": "typescript",
        ".jsx": "javascript",
        ".rs": "rust",
        ".java": "java",
        ".cpp": "cpp",
        ".cc": "cpp",
        ".c": "c",
        ".go": "go",
        ".rb": "ruby",
        ".php": "php",
    }
    
    ext = path.suffix.lower()
    lang = ext_to_lang.get(ext)
    
    if lang and lang in settings.supported_languages_list:
        return lang
    
    return None


def format_code_block(code: str, language: str = "python") -> str:
    """Format code block for terminal display."""
    from rich.syntax import Syntax
    
    syntax = Syntax(code, language, theme="monokai", line_numbers=True)
    return syntax


def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text with ellipsis."""
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."


def ensure_dir(path: str | Path) -> Path:
    """Ensure directory exists, create if not."""
    dir_path = Path(path)
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path
