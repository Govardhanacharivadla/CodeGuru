"""Build rich context around code for better LLM explanations."""

from pathlib import Path
from typing import Optional
from dataclasses import dataclass

from .code_analyzer import CodeStructure, FunctionInfo, ClassInfo, code_analyzer
from .utils import read_file, logger


@dataclass
class CodeContext:
    """Rich context about code for explanation."""
    code: str
    language: str
    element_type: str  # "function", "class", or "file"
    element_name: Optional[str]
    docstring: Optional[str]
    imports: list[str]
    dependencies: list[str]  # Other functions/classes used
    complexity: int
    related_code: str  # Surrounding context
    file_path: Optional[str]


class ContextBuilder:
    """Builds rich context around code elements."""
    
    def build_function_context(
        self,
        file_path: str | Path,
        function_name: str
    ) -> CodeContext:
        """Build context for a specific function."""
        code = read_file(file_path)
        structure = code_analyzer.analyze_file(file_path)
        
        func = code_analyzer.find_function(structure, function_name)
        if not func:
            raise ValueError(f"Function '{function_name}' not found in {file_path}")
        
        # Extract dependencies (simplified - just look for function calls)
        dependencies = self._extract_dependencies(func.body, structure)
        
        # Get surrounding context (imports + first 50 lines)
        related_code = self._get_file_context(code, structure)
        
        return CodeContext(
            code=func.body,
            language=structure.language,
            element_type="function",
            element_name=func.name,
            docstring=func.docstring,
            imports=structure.imports,
            dependencies=dependencies,
            complexity=self._calculate_function_complexity(func),
            related_code=related_code,
            file_path=str(file_path)
        )
    
    def build_class_context(
        self,
        file_path: str | Path,
        class_name: str
    ) -> CodeContext:
        """Build context for a specific class."""
        code = read_file(file_path)
        structure = code_analyzer.analyze_file(file_path)
        
        cls = code_analyzer.find_class(structure, class_name)
        if not cls:
            raise ValueError(f"Class '{class_name}' not found in {file_path}")
        
        # Build class code (name + all methods)
        class_code = f"class {cls.name}:\n"
        for method in cls.methods:
            class_code += f"  {method.name}(...)\n"
        
        dependencies = []
        for method in cls.methods:
            deps = self._extract_dependencies(method.body, structure)
            dependencies.extend(deps)
        
        related_code = self._get_file_context(code, structure)
        
        return CodeContext(
            code=class_code,
            language=structure.language,
            element_type="class",
            element_name=cls.name,
            docstring=cls.docstring,
            imports=structure.imports,
            dependencies=list(set(dependencies)),  # Unique deps
            complexity=len(cls.methods),
            related_code=related_code,
            file_path=str(file_path)
        )
    
    def build_file_context(self, file_path: str | Path) -> CodeContext:
        """Build context for entire file."""
        code = read_file(file_path)
        structure = code_analyzer.analyze_file(file_path)
        
        # Summary of file contents
        summary = f"{len(structure.functions)} functions, {len(structure.classes)} classes"
        
        return CodeContext(
            code=code,
            language=structure.language,
            element_type="file",
            element_name=Path(file_path).name,
            docstring=None,
            imports=structure.imports,
            dependencies=[],
            complexity=structure.complexity_score,
            related_code="",
            file_path=str(file_path)
        )
    
    def _extract_dependencies(
        self,
        code: str,
        structure: CodeStructure
    ) -> list[str]:
        """Extract function/class names called in code (simplified)."""
        dependencies = []
        
        # Look for function calls (simple heuristic)
        for func in structure.functions:
            if func.name in code:
                dependencies.append(func.name)
        
        for cls in structure.classes:
            if cls.name in code:
                dependencies.append(cls.name)
        
        return dependencies
    
    def _get_file_context(self, code: str, structure: CodeStructure) -> str:
        """Get relevant file context (imports + structure overview)."""
        lines = code.split('\n')
        
        # Get imports
        import_lines = []
        for i, line in enumerate(lines):
            if line.strip().startswith('import ') or line.strip().startswith('from '):
                import_lines.append(line)
            if i > 50:  # Only check first 50 lines
                break
        
        context = '\n'.join(import_lines)
        
        # Add structure summary
        context += f"\n\n# File contains:\n"
        context += f"# - {len(structure.functions)} functions\n"
        context += f"# - {len(structure.classes)} classes\n"
        
        return context
    
    def _calculate_function_complexity(self, func: FunctionInfo) -> int:
        """Calculate simple complexity metric for function."""
        # Count control flow statements
        complexity = 1  # Base complexity
        
        body_lower = func.body.lower()
        
        # Add for each control flow statement
        complexity += body_lower.count('if ')
        complexity += body_lower.count('elif ')
        complexity += body_lower.count('for ')
        complexity += body_lower.count('while ')
        complexity += body_lower.count('try:')
        complexity += body_lower.count('except ')
        
        return complexity


# Global context builder instance
context_builder = ContextBuilder()
