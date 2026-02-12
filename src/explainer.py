"""Core explanation engine - generates multi-level educational explanations."""

import json
from typing import Literal
from pathlib import Path

from .llm_client import llm_manager, Explanation, Concept
from .context_builder import context_builder, CodeContext
from .config import settings
from .utils import logger


class ExplainerEngine:
    """Generates educational explanations of code."""
    
    SYSTEM_PROMPT = """You are an expert programming teacher and computer science educator.

Your goal is to help developers DEEPLY UNDERSTAND code, not just know what it does.

For every piece of code you explain, you must:
1. Explain WHAT it does (surface-level description)
2. Explain HOW it works (step-by-step implementation details)
3. Explain WHY it's designed this way (architectural reasoning, design patterns)
4. Teach key CONCEPTS (computer science principles, not just syntax)
5. Highlight common MISTAKES people make with similar code
6. Share BEST PRACTICES and alternative approaches

Always assume the user wants to LEARN and become a better developer, not just get a quick answer.
Be thorough but clear. Use analogies when helpful. Explain terminology."""

    def __init__(self):
        """Initialize explainer engine."""
        self.llm = llm_manager
    
    async def explain_function(
        self,
        file_path: str | Path,
        function_name: str,
        depth: Literal["simple", "detailed", "deep", "all"] = "all"
    ) -> Explanation:
        """Generate explanation for a specific function."""
        
        # Build context
        context = context_builder.build_function_context(file_path, function_name)
        
        # Generate explanation
        return await self._generate_explanation(context, depth)
    
    async def explain_class(
        self,
        file_path: str | Path,
        class_name: str,
        depth: Literal["simple", "detailed", "deep", "all"] = "all"
    ) -> Explanation:
        """Generate explanation for a specific class."""
        
        context = context_builder.build_class_context(file_path, class_name)
        return await self._generate_explanation(context, depth)
    
    async def explain_file(
        self,
        file_path: str | Path,
        depth: Literal["simple", "detailed", "deep", "all"] = "all"
    ) -> Explanation:
        """Generate explanation for entire file."""
        
        context = context_builder.build_file_context(file_path)
        return await self._generate_explanation(context, depth)
    
    async def explain_concept(self, concept_name: str) -> str:
        """Explain a programming concept in detail."""
        
        prompt = f"""Explain the programming concept: "{concept_name}"

Provide:
1. Clear definition
2. Why it exists and what problem it solves
3. How it works (with simple code examples)
4. When to use it vs when not to
5. Common mistakes and misconceptions
6. Best practices
7. Related concepts

Make it educational and thorough."""

        response = await self.llm.generate(
            prompt=prompt,
            system_prompt=self.SYSTEM_PROMPT,
            use_cache=True
        )
        
        return response
    
    async def _generate_explanation(
        self,
        context: CodeContext,
        depth: Literal["simple", "detailed", "deep", "all"]
    ) -> Explanation:
        """Generate structured explanation from context."""
        
        # Select appropriate model for depth
        if depth == "simple":
            self.llm.select_model_for_task("simple")
        elif depth == "detailed":
            self.llm.select_model_for_task("detailed")
        else:
            self.llm.select_model_for_task("deep")
        
        # Build comprehensive prompt
        prompt = self._build_explanation_prompt(context, depth)
        
        # Try to get structured JSON response
        try:
            response = await self.llm.generate(
                prompt=prompt,
                system_prompt=self.SYSTEM_PROMPT,
                response_format=Explanation,
                use_cache=True
            )
            
            # Parse JSON response
            explanation_data = json.loads(response)
            explanation = Explanation(**explanation_data)
            
        except (json.JSONDecodeError, Exception) as e:
            logger.warning(f"Failed to parse structured response, using fallback: {e}")
            
            # Fallback to unstructured explanation
            explanation = await self._generate_fallback_explanation(context, response)
        
        return explanation
    
    def _build_explanation_prompt(
        self,
        context: CodeContext,
        depth: Literal["simple", "detailed", "deep", "all"]
    ) -> str:
        """Build detailed prompt for LLM."""
        
        prompt = f"""Analyze and explain this {context.language} {context.element_type}:

```{context.language}
{context.code}
```

"""
        
        # Add context information
        if context.element_name:
            prompt += f"Element name: {context.element_name}\n"
        
        if context.docstring:
            prompt += f"Existing docstring: {context.docstring}\n"
        
        if context.imports:
            prompt += f"\nImports in file:\n"
            for imp in context.imports[:5]:  # Limit to first 5
                prompt += f"- {imp}\n"
        
        if context.dependencies:
            prompt += f"\nDepends on: {', '.join(context.dependencies[:5])}\n"
        
        prompt += f"\nComplexity score: {context.complexity}\n"
        
        # Specify desired depth
        if depth == "all" or depth == "simple":
            prompt += "\n**Simple explanation (ELI5)**: Explain in plain English what this code does."
        
        if depth == "all" or depth == "detailed":
            prompt += "\n**Detailed explanation**: Step-by-step breakdown of how it works."
        
        if depth == "all" or depth == "deep":
            prompt += "\n**Deep dive**: Explain the underlying concepts, why it's designed this way, design patterns used."
        
        prompt += """

Provide your response in JSON format with these fields:
{
  "summary": "One sentence summary",
  "simple_explanation": "ELI5 explanation",
  "detailed_explanation": "Technical step-by-step breakdown",
  "deep_dive": "Conceptual understanding and design rationale",
  "key_concepts": [
    {
      "name": "Concept name",
      "definition": "Clear definition",
      "related_topics": ["topic1", "topic2"]
    }
  ],
  "common_mistakes": ["mistake 1", "mistake 2"],
  "best_practices": ["practice 1", "practice 2"],
  "related_resources": ["resource 1", "resource 2"]
}
"""
        
        return prompt
    
    async def _generate_fallback_explanation(
        self,
        context: CodeContext,
        raw_response: str
    ) -> Explanation:
        """Generate explanation from unstructured response."""
        
        # Create basic structure
        lines = raw_response.split('\n')
        
        return Explanation(
            summary=f"Explanation of {context.element_name or context.element_type}",
            simple_explanation=raw_response[:200],
            detailed_explanation=raw_response,
            deep_dive="(See detailed explanation above)",
            key_concepts=[
                Concept(
                    name=context.language.title(),
                    definition=f"Programming language: {context.language}",
                    related_topics=[]
                )
            ],
            common_mistakes=[],
            best_practices=[],
            related_resources=[]
        )


# Global explainer engine instance
explainer_engine = ExplainerEngine()
