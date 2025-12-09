import os
import sys

# Ensure we can import from the source root
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from aios.memos.core import (
    Memos, 
    MemoryConfig, 
    VectorStoreConfig, 
    LlmConfig, 
    EmbedderConfig
)

def main():
    print("🧠 Initializing Sovereign Memory System (Local Only)...")
    
    # Configuration for a fully local stack
    # 1. Vector Store: ChromaDB (Local file storage)
    # 2. LLM: Ollama (Running locally)
    # 3. Embedder: Ollama (Running locally)
    
    config = MemoryConfig(
        vector_store=VectorStoreConfig(
            provider="chroma",
            collection_name="sovereign_memories",
            config={"path": "./sovereign_db"} 
        ),
        llm=LlmConfig(
            provider="ollama",
            config={
                "model": "llama3",  # Change to your preferred local model
                "temperature": 0.1
            }
        ),
        embedder=EmbedderConfig(
            provider="ollama",
            config={
                "model": "nomic-embed-text" # Standard local embedding model
            }
        )
    )

    # Initialize the system
    try:
        memos = Memos(config)
        print("✅ System initialized successfully.")
    except Exception as e:
        print(f"❌ Initialization failed. Ensure Ollama is running (http://localhost:11434). Error: {e}")
        return

    # 1. Add a Memory
    print("\n📝 Adding memory...")
    memory_text = "The user prefers strictly local processing for privacy and autonomy."
    try:
        res = memos.add(memory_text, {"tag": "preference", "priority": "high"})
        print(f"   Saved memory ID: {res.id}")
    except Exception as e:
        print(f"   Failed to add memory: {e}")

    # 2. Search Memory
    print("\n🔍 Searching memory...")
    query = "What are the user's privacy preferences?"
    results = memos.search(query, limit=1)
    
    if results:
        for item in results:
            print(f"   Found: '{item.memory}' (Score: {item.score})")
    else:
        print("   No results found.")

if __name__ == "__main__":
    main()
