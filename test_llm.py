"""Test LLM functionality directly."""

import asyncio
import sys

async def test_llm():
    try:
        from src.llm_client import llm_manager
        
        print("Testing LLM connection...")
        print("="*50)
        
        prompt = """Explain this Python code in simple terms:

```python
async def fetch_data(url):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()
```

Provide a brief, 2-3 sentence explanation."""
        
        print("\n📤 Sending prompt to LLM...")
        print("-"*50)
        
        response = await llm_manager.generate(prompt)
        
        print(f"\n📥 Response:")
        print("="*50)
        print(response)
        print("="*50)
        
        print("\n✅ LLM test completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(test_llm())
