"""Generate Mermaid diagrams from code structures."""

from typing import Optional
from pathlib import Path

from .code_analyzer import CodeStructure, FunctionInfo, code_analyzer
from .config import settings
from .utils import logger, ensure_dir


class DiagramGenerator:
    """Generates Mermaid diagrams from code."""
    
    def __init__(self, output_dir: str = "diagrams"):
        """Initialize diagram generator."""
        self.output_dir = Path(output_dir)
        ensure_dir(self.output_dir)
    
    def generate_flowchart(self, function: FunctionInfo, language: str) -> str:
        """Generate flowchart for a function's control flow."""
        
        mermaid = "flowchart TD\n"
        mermaid += f'    Start(["{function.name}()"])\n'
        
        # Analyze function body for control flow
        body_lines = function.body.split('\n')
        
        node_id = 1
        prev_node = "Start"
        
        for line in body_lines:
            line_stripped = line.strip()
            
            if not line_stripped or line_stripped.startswith('#'):
                continue
            
            current_node = f"N{node_id}"
            
            if line_stripped.startswith('if '):
                # Conditional
                condition = line_stripped[3:].rstrip(':')
                mermaid += f'    {current_node}{{{{{condition}?}}}}\n'
                mermaid += f'    {prev_node} --> {current_node}\n'
                prev_node = current_node
                node_id += 1
                
            elif line_stripped.startswith('return '):
                # Return statement
                value = line_stripped[7:]
                mermaid += f'    {current_node}["Return: {value}"]\n'
                mermaid += f'    {prev_node} --> {current_node}\n'
                mermaid += f'    {current_node} --> End\n'
                prev_node = current_node
                node_id += 1
                
            elif line_stripped.startswith('for ') or line_stripped.startswith('while '):
                # Loop
                loop_type = line_stripped.split()[0]
                mermaid += f'    {current_node}["{loop_type} loop"]\n'
                mermaid += f'    {prev_node} --> {current_node}\n'
                prev_node = current_node
                node_id += 1
        
        mermaid += '    End([End])\n'

        if prev_node != "Start" and "End" not in mermaid:
            mermaid += f'    {prev_node} --> End\n'
        
        return mermaid
    
    def generate_call_graph(self, structure: CodeStructure, entry_point: Optional[str] = None) -> str:
        """Generate call graph showing function dependencies."""
        
        mermaid = "graph TD\n"
        
        # Add all functions as nodes
        for func in structure.functions:
            mermaid += f'    {func.name}["{func.name}()"]\n'
        
        # Simple dependency detection (look for function names in bodies)
        for func in structure.functions:
            for other_func in structure.functions:
                if other_func.name != func.name and other_func.name in func.body:
                    mermaid += f'    {func.name} --> {other_func.name}\n'
        
        return mermaid
    
    def generate_class_diagram(self, structure: CodeStructure) -> str:
        """Generate UML class diagram."""
        
        mermaid = "classDiagram\n"
        
        for cls in structure.classes:
            mermaid += f'    class {cls.name} {{\n'
            
            # Add methods
            for method in cls.methods:
                params = ", ".join(method.parameters[:3])  # Limit params
                if len(method.parameters) > 3:
                    params += ", ..."
                mermaid += f'        +{method.name}({params})\n'
            
            mermaid += '    }\n'
            
            # Add inheritance (if detected)
            for base in cls.base_classes:
                mermaid += f'    {base} <|-- {cls.name}\n'
        
        return mermaid
    
    def generate_sequence_diagram(self, function: FunctionInfo) -> str:
        """Generate sequence diagram for function calls."""
        
        mermaid = "sequenceDiagram\n"
        mermaid += f'    participant User\n'
        mermaid += f'    participant {function.name}\n'
        
        mermaid += f'    User->>+{function.name}: call\n'
        
        # Detect function calls in body (simplified)
        lines = function.body.split('\n')
        for line in lines:
            if '(' in line and ')' in line and not line.strip().startswith('#'):
                # Try to extract function call
                parts = line.split('(')
                if parts:
                    func_call = parts[0].strip().split()[-1]
                    if func_call and func_call != function.name:
                        mermaid += f'    {function.name}->>+{func_call}: execute\n'
                        mermaid += f'    {func_call}-->>-{function.name}: return\n'
        
        mermaid += f'    {function.name}-->>-User: return\n'
        
        return mermaid
    
    def save_diagram(self, mermaid_code: str, filename: str) -> Path:
        """Save Mermaid diagram to file."""
        output_path = self.output_dir / f"{filename}.mmd"
        output_path.write_text(mermaid_code, encoding="utf-8")
        logger.info(f"Saved diagram to: {output_path}")
        return output_path
    
    def generate_diagram_for_code(
        self,
        file_path: str | Path,
        element_name: Optional[str] = None,
        diagram_type: str = "flowchart"
    ) -> str:
        """Generate appropriate diagram for code element."""
        
        if not settings.generate_diagrams:
            return ""
        
        structure = code_analyzer.analyze_file(file_path)
        
        if diagram_type == "flowchart" and element_name:
            # Function flowchart
            func = code_analyzer.find_function(structure, element_name)
            if func:
                return self.generate_flowchart(func, structure.language)
        
        elif diagram_type == "class":
            # Class diagram for OOP code
            if structure.classes:
                return self.generate_class_diagram(structure)
        
        elif diagram_type == "call_graph":
            # Call graph for file
            return self.generate_call_graph(structure, element_name)
        
        elif diagram_type == "sequence" and element_name:
            # Sequence diagram for function
            func = code_analyzer.find_function(structure, element_name)
            if func:
                return self.generate_sequence_diagram(func)
        
        # Default to flowchart if available
        if structure.functions and element_name:
            func = code_analyzer.find_function(structure, element_name)
            if func:
                return self.generate_flowchart(func, structure.language)
        
        return ""


# Global diagram generator instance
diagram_generator = DiagramGenerator()
