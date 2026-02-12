"""Simple test of the explainer with sample code."""

import asyncio
import sys

async def test_explain():
    try:
        from src.explainer import explainer_engine
        
        print("Testing code explanation...")
        print("="*50)
        
        # Test explaining the sample function
        file_path = "tests/fixtures/sample.py"
        function_name = "fetch_user_data"
        
        print(f"\nAnalyzing: {function_name}() in {file_path}")
        print("-"*50)
        
        explanation = await explainer_engine.explain_function(
            file_path,
            function_name,
            depth="simple"  # Start with simple
        )
        
        print(f"\n📝 Summary:")
        print(explanation.summary)
        
        print(f"\n🔹 Simple Explanation:")
        print(explanation.simple_explanation)
        
        print("\n✅ Test completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(test_explain())
