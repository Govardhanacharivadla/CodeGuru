"""User-friendly error handling with helpful suggestions."""

from pathlib import Path
from .ui import ui, console


class CodeGuruError(Exception):
    """Base exception for CodeGuru with user-friendly messages."""
    
    def __init__(self, message: str, suggestion: str =None):
        self.message = message
        self.suggestion = suggestion
        super().__init__(message)
    
    def display(self):
        """Display error to user."""
        ui.show_error(self.message, self.suggestion)


class FileNotFoundError(CodeGuruError):
    """File not found error with helpful suggestions."""
    
    def __init__(self, filepath: str):
        message = f"Could not find file: {filepath}"
        suggestion = (
            "Please check:\n"
            "• File path is correct\n"
            "• File exists in the current directory\n"
            "• You have permission to read the file\n\n"
            f"Current directory: {Path.cwd()}"
        )
        super().__init__(message, suggestion)


class UnsupportedLanguageError(CodeGuruError):
    """Unsupported language error."""
    
    def __init__(self, file_path: str, detected_lang: str = None):
        ext = Path(file_path).suffix
        message = f"Unsupported file type: {ext}"
        suggestion = (
            "Supported languages:\n"
            "• Python (.py)\n"
            "• JavaScript (.js, .jsx)\n"
            "• TypeScript (.ts, .tsx)\n"
            "• Java (.java)\n"
            "• C (.c)\n"
            "• C++ (.cpp, .cc)\n\n"
            "Try renaming your file or choose a supported language."
        )
        super().__init__(message, suggestion)


class ParsingError(CodeGuruError):
    """Code parsing error."""
    
    def __init__(self, language: str, details: str = None):
        message = f"Failed to parse {language} code"
        suggestion = (
            "This could be because:\n"
            "• Code contains syntax errors\n"
            "• File encoding is not UTF-8\n"
            "• Language detection was incorrect\n\n"
"Try fixing syntax errors and try again."
        )
        if details:
            suggestion += f"\n\nDetails: {details}"
        super().__init__(message, suggestion)


class NetworkError(CodeGuruError):
    """LLM network error."""
    
    def __init__(self, provider: str, details: str = None):
        message = f"Failed to connect to {provider}"
        suggestion = (
            "Possible solutions:\n"
            "• Check your internet connection\n"
            "• Verify API key is correct (for Groq)\n"
        )
        
        if provider.lower() == "groq":
            suggestion += (
                "\n• Try switching to Ollama (local, no internet needed):\n"
                "  1. Install Ollama from ollama.com\n"
                "  2. Run: ollama pull qwen2.5-coder:7b\n"
                "  3. Update .env: LLM_PROVIDER=ollama"
            )
        else:  # Ollama
            suggestion += (
                "\n• Make sure Ollama is running\n"
                "• Check if model is installed: ollama list\n"
                "• Try: ollama pull qwen2.5-coder:7b"
            )
        
        if details:
            suggestion += f"\n\nError details: {details}"
        
        super().__init__(message, suggestion)


class FileTooLargeError(CodeGuruError):
    """File too large error."""
    
    def __init__(self, size_kb: int, max_kb: int):
        message = f"File is too large: {size_kb}KB (max: {max_kb}KB)"
        suggestion = (
            "To analyze large files:\n"
            "• Split into smaller files\n"
            "• Use --function flag to analyze specific functions\n"
            "• Increase MAX_FILE_SIZE_KB in .env (not recommended)\n\n"
            "Large files may slow down parsing significantly."
        )
        super().__init__(message, suggestion)


def handle_error(error: Exception, verbose: bool = False):
    """Handle any error gracefully."""
    if isinstance(error, CodeGuruError):
        error.display()
    else:
        # Generic error
        message = str(error)
        suggestion = None
        
        # Add specific suggestions based on error type
        if "No module named" in message:
            module = message.split("'")[1] if "'" in message else "unknown"
            suggestion = f"Install missing module:\n  pip install {module}"
        
        elif "Permission denied" in message:
            suggestion = "Check file permissions and try running with appropriate access."
        
        elif "Connection" in message or "timeout" in message.lower():
            suggestion = "Check your internet connection and try again."
        
        ui.show_error(f"Unexpected error: {message}", suggestion)
        
        if verbose:
            import traceback
            console.print("\n[dim]Full traceback:[/dim]")
            console.print(traceback.format_exc())
