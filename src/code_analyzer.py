"""Code analysis using tree-sitter for multi-language support."""

from pathlib import Path
from typing import Optional, NamedTuple
from dataclasses import dataclass

from .utils import logger, read_file, detect_language


@dataclass
class FunctionInfo:
    """Information about a function."""
    name: str
    start_line: int
    end_line: int
    parameters: list[str]
    body: str
    docstring: Optional[str] = None


@dataclass
class ClassInfo:
    """Information about a class."""
    name: str
    start_line: int
    end_line: int
    methods: list[FunctionInfo]
    base_classes: list[str]
    docstring: Optional[str] = None


@dataclass
class CodeStructure:
    """Parsed code structure."""
    language: str
    functions: list[FunctionInfo]
    classes: list[ClassInfo]
    imports: list[str]
    complexity_score: int


class CodeAnalyzer:
    """Analyzes code structure using tree-sitter."""
    
    def __init__(self):
        """Initialize code analyzer."""
        self.parsers = {}
        self._initialize_parsers()
    
    def _initialize_parsers(self):
        """Initialize tree-sitter parsers for supported languages."""
        try:
            from tree_sitter import Parser
            from tree_sitter_languages import get_language, get_parser
            
            # Python parser
            self.parsers["python"] = get_parser("python")
            
            # JavaScript parser
            self.parsers["javascript"] = get_parser("javascript")
            self.parsers["typescript"] = get_parser("typescript")
            
            logger.info(f"Initialized parsers for: {list(self.parsers.keys())}")
            
        except ImportError as e:
            logger.error(f"Failed to import tree-sitter: {e}")
            logger.info("Install with: pip install tree-sitter-languages")
            raise
    
    def analyze_file(self, file_path: str | Path) -> CodeStructure:
        """Analyze a code file and extract structure."""
        content = read_file(file_path)
        language = detect_language(file_path)
        
        if not language:
            raise ValueError(f"Unsupported language for file: {file_path}")
        
        if language not in self.parsers:
            raise ValueError(f"No parser available for language: {language}")
        
        return self.analyze_code(content, language)
    
    def analyze_code(self, code: str, language: str) -> CodeStructure:
        """Analyze code string and extract structure."""
        parser = self.parsers.get(language)
        if not parser:
            raise ValueError(f"No parser for language: {language}")
        
        tree = parser.parse(bytes(code, "utf-8"))
        root = tree.root_node
        
        # Extract structure based on language
        if language == "python":
            return self._analyze_python(root, code)
        elif language in ["javascript", "typescript"]:
            return self._analyze_javascript(root, code)
        else:
            # Generic analysis
            return CodeStructure(
                language=language,
                functions=[],
                classes=[],
                imports=[],
                complexity_score=0
            )
    
    def _analyze_python(self, root_node, code: str) -> CodeStructure:
        """Analyze Python code structure."""
        functions = []
        classes = []
        imports = []
        
        def extract_node_text(node) -> str:
            """Extract text from a node."""
            return code[node.start_byte:node.end_byte]
        
        def traverse(node):
            """Traverse AST and extract information."""
            if node.type == "function_definition":
                func_name_node = node.child_by_field_name("name")
                params_node = node.child_by_field_name("parameters")
                body_node = node.child_by_field_name("body")
                
                if func_name_node:
                    func_info = FunctionInfo(
                        name=extract_node_text(func_name_node),
                        start_line=node.start_point[0] + 1,
                        end_line=node.end_point[0] + 1,
                        parameters=self._extract_python_params(params_node, code) if params_node else [],
                        body=extract_node_text(body_node) if body_node else "",
                        docstring=self._extract_python_docstring(body_node, code) if body_node else None
                    )
                    functions.append(func_info)
            
            elif node.type == "class_definition":
                class_name_node = node.child_by_field_name("name")
                body_node = node.child_by_field_name("body")
                
                if class_name_node:
                    # Extract methods
                    methods = []
                    if body_node:
                        for child in body_node.children:
                            if child.type == "function_definition":
                                method_name = child.child_by_field_name("name")
                                if method_name:
                                    params_node = child.child_by_field_name("parameters")
                                    method_body = child.child_by_field_name("body")
                                    methods.append(FunctionInfo(
                                        name=extract_node_text(method_name),
                                        start_line=child.start_point[0] + 1,
                                        end_line=child.end_point[0] + 1,
                                        parameters=self._extract_python_params(params_node, code) if params_node else [],
                                        body=extract_node_text(method_body) if method_body else ""
                                    ))
                    
                    class_info = ClassInfo(
                        name=extract_node_text(class_name_node),
                        start_line=node.start_point[0] + 1,
                        end_line=node.end_point[0] + 1,
                        methods=methods,
                        base_classes=[],  # TODO: Extract base classes
                        docstring=self._extract_python_docstring(body_node, code) if body_node else None
                    )
                    classes.append(class_info)
            
            elif node.type in ["import_statement", "import_from_statement"]:
                imports.append(extract_node_text(node))
            
            # Recurse to children
            for child in node.children:
                traverse(child)
        
        traverse(root_node)
        
        # Calculate complexity (simple metric: number of functions + classes)
        complexity = len(functions) + len(classes) * 2
        
        return CodeStructure(
            language="python",
            functions=functions,
            classes=classes,
            imports=imports,
            complexity_score=complexity
        )
    
    def _analyze_javascript(self, root_node, code: str) -> CodeStructure:
        """Analyze JavaScript/TypeScript code structure."""
        functions = []
        classes = []
        imports = []
        
        def extract_node_text(node) -> str:
            return code[node.start_byte:node.end_byte]
        
        def traverse(node):
            if node.type == "function_declaration":
                name_node = node.child_by_field_name("name")
                params_node = node.child_by_field_name("parameters")
                body_node = node.child_by_field_name("body")
                
                if name_node:
                    functions.append(FunctionInfo(
                        name=extract_node_text(name_node),
                        start_line=node.start_point[0] + 1,
                        end_line=node.end_point[0] + 1,
                        parameters=[],  # TODO: Extract params
                        body=extract_node_text(body_node) if body_node else ""
                    ))
            
            elif node.type == "class_declaration":
                name_node = node.child_by_field_name("name")
                body_node = node.child_by_field_name("body")
                
                if name_node:
                    classes.append(ClassInfo(
                        name=extract_node_text(name_node),
                        start_line=node.start_point[0] + 1,
                        end_line=node.end_point[0] + 1,
                        methods=[],  # TODO: Extract methods
                        base_classes=[]
                    ))
            
            elif node.type == "import_statement":
                imports.append(extract_node_text(node))
            
            for child in node.children:
                traverse(child)
        
        traverse(root_node)
        
        return CodeStructure(
            language="javascript",
            functions=functions,
            classes=classes,
            imports=imports,
            complexity_score=len(functions) + len(classes) * 2
        )
    
    def _extract_python_params(self, params_node, code: str) -> list[str]:
        """Extract parameter names from Python function."""
        params = []
        for child in params_node.children:
            if child.type == "identifier":
                params.append(code[child.start_byte:child.end_byte])
        return params
    
    def _extract_python_docstring(self, body_node, code: str) -> Optional[str]:
        """Extract docstring from Python function/class body."""
        if body_node and body_node.children:
            first_stmt = body_node.children[0]
            if first_stmt.type == "expression_statement":
                expr = first_stmt.children[0] if first_stmt.children else None
                if expr and expr.type == "string":
                    docstring = code[expr.start_byte:expr.end_byte]
                    # Remove quotes
                    return docstring.strip('"""').strip("'''").strip()
        return None
    
    def find_function(self, structure: CodeStructure, function_name: str) -> Optional[FunctionInfo]:
        """Find a specific function in the code structure."""
        for func in structure.functions:
            if func.name == function_name:
                return func
        
        # Also check class methods
        for cls in structure.classes:
            for method in cls.methods:
                if method.name == function_name:
                    return method
        
        return None
    
    def find_class(self, structure: CodeStructure, class_name: str) -> Optional[ClassInfo]:
        """Find a specific class in the code structure."""
        for cls in structure.classes:
            if cls.name == class_name:
                return cls
        return None


# NOTE: Commented out for now due to tree-sitter compatibility issues
# Create analyzer instance manually when needed: code_analyzer = CodeAnalyzer()
code_analyzer = None
