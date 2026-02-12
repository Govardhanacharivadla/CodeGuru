"""Simple test script to debug initialization."""

import sys
import traceback

try:
    print("Testing imports...")
    from src.config import settings
    print(f"✓ Config loaded: {settings.llm_provider}")
    
    from src.utils import logger
    print("✓ Logger initialized")
    
    from src.llm_client import OllamaClient
    print("✓ OllamaClient imported")
    
    print("\nInitializing Ollama client...")
    client = OllamaClient()
    print(f"✓ Client initialized with model: {client.model}")
    
    print("\n✅ All tests passed!")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\nFull traceback:")
    traceback.print_exc()
    sys.exit(1)
