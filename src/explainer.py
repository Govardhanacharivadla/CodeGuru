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
    
    SYSTEM_PROMPT = """You are CodeGuru, an expert programming teacher specializing in making complex code easy to understand.

Your teaching philosophy:
- Transform confusion into clarity through structured explanations
- Teach WHY before HOW - explain the reasoning behind design decisions
- Use real-world analogies to make abstract concepts concrete
- Emphasize practical application over theory
- Point out common pitfalls to accelerate learning

For every code explanation, structure your response to answer:
1. **What**: One-sentence summary of purpose
2. **How**: Step-by-step breakdown of implementation
3. **Why**: Design rationale and architectural choices
4. **Concepts**: Core CS principles being applied (with definitions)
5. **Pitfalls**: Common mistakes developers make with similar code
6. **Best Practices**: Industry-standard approaches

Always use markdown formatting with code blocks, headers, and emphasis.
Write like you're teaching a colleague who wants to deeply understand, not just copy-paste."""

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

Structure your explanation:

## Definition
Clear, concise definition in one sentence.

## The Problem It Solves
Why does this concept exist? What problem does it address?

## How It Works
Step-by-step breakdown with simple code examples.

## When To Use It
Practical scenarios where this concept shines.

## When NOT To Use It
Cases where alternatives are better.

## Common Mistakes
Typical errors developers make.

## Best Practices
Industry-standard approaches.

## Related Concepts
Other topics to explore.

Use markdown formatting and code examples."""

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
            prompt += f"**Element**: `{context.element_name}`\n"
        
        if context.docstring:
            prompt += f"**Existing docs**: {context.docstring}\n"
        
        if context.imports:
            prompt += f"\n**Imports**:\n"
            for imp in context.imports[:5]:  # Limit to first 5
                prompt += f"- `{imp}`\n"
        
        if context.dependencies:
            prompt += f"\n**Dependencies**: {', '.join(f'`{d}`' for d in context.dependencies[:5])}\n"
        
        prompt += f"\n**Complexity**: {context.complexity}/10\n\n---\n\n"
        
        # Specify desired depth with clear instructions
        if depth == "all" or depth == "simple":
            prompt += """## Simple Explanation (ELI5)
Explain what this code does in plain English. Imagine explaining to a non-programmer.

"""
        
        if depth == "all" or depth == "detailed":
            prompt += """## Detailed Breakdown
Step-by-step walkthrough of how the code works. Include:
- What each major section does
- How data flows through the code
- Any notable techniques or patterns

"""
        
        if depth == "all" or depth == "deep":
            prompt += """## Deep Dive
Explain the computer science concepts and design decisions:
- Why is it structured this way?
- What design patterns or paradigms are used?
- What are the trade-offs in this approach?
- How does it relate to broader system architecture?

"""
        
        prompt += """---

Provide your response in JSON format:
```json
{
  "summary": "One crisp sentence summarizing the purpose",
  "simple_explanation": "ELI5 version in 2-3 sentences",
  "detailed_explanation": "Technical step-by-step breakdown (markdown formatted)",
  "deep_dive": "Conceptual analysis and design rationale (markdown formatted)",
  "key_concepts": [
    {
      "name": "Concept Name",
      "definition": "Clear definition with context",
      "related_topics": ["topic1", "topic2"]
    }
  ],
  "common_mistakes": ["Specific mistake with example", "Another mistake"],
  "best_practices": ["Concrete practice with reasoning", "Another practice"],
  "related_resources": ["Python docs: functools", "Design Patterns book"]
}
```
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
