"""
Tests for the Memos class.

This module contains unit tests for the Memos class and its functionality.

To run tests:
    1. Direct execution:
       python test_memos.py
    
    2. Using pytest:
       pytest tests/test_memos.py
       
    3. Verbose output:
       pytest tests/test_memos.py -v

The tests cover:
- Initialization
- Adding memories
- Searching memories
- Deleting memories
- Clearing all memories
"""

import pytest
from unittest.mock import Mock, patch
import sys
import os

# Add the project root directory to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from aios.memos.core import (
    Memos,
    MemoryConfig,
    VectorStoreConfig,
    LlmConfig,
    EmbedderConfig,
    MemoryItem
)

@pytest.fixture
def mock_vector_store():
    return Mock()

@pytest.fixture
def mock_llm():
    return Mock()

@pytest.fixture
def mock_embedder():
    return Mock()

@pytest.fixture
def memos_config():
    return MemoryConfig(
        vector_store=VectorStoreConfig(
            provider="qdrant",
            collection_name="test_memories"
        ),
        llm=LlmConfig(
            provider="openai",
            config={"model": "gpt-3.5-turbo"}
        ),
        embedder=EmbedderConfig(
            provider="openai",
            embedding_dims=1536
        )
    )

@pytest.fixture
def memos_with_mocks(memos_config, mock_vector_store, mock_llm, mock_embedder):
    with patch('aios.memos.core.factories.VectorStoreFactory.create') as mock_vs_create, \
         patch('aios.memos.core.factories.LlmFactory.create') as mock_llm_create, \
         patch('aios.memos.core.factories.EmbedderFactory.create') as mock_emb_create:
        
        mock_vs_create.return_value = mock_vector_store
        mock_llm_create.return_value = mock_llm
        mock_emb_create.return_value = mock_embedder
        
        memos = Memos(memos_config)
        return memos

class TestMemos:
    def test_initialization(self, memos_with_mocks, memos_config):
        """Test that Memos initializes correctly with the given config"""
        memos = memos_with_mocks
        assert memos.config == memos_config
        assert memos.vector_store is not None
        assert memos.llm is not None
        assert memos.embedder is not None

    def test_add_memory(self, memos_with_mocks, mock_embedder, mock_vector_store):
        """Test adding a new memory"""
        memos = memos_with_mocks
        test_text = "Test memory"
        test_metadata = {"tag": "test"}
        mock_embeddings = [0.1, 0.2, 0.3]
        
        # Setup mock
        mock_embedder.embed.return_value = mock_embeddings
        
        # Add memory
        memory_item = memos.add(test_text, test_metadata)
        
        # Verify
        assert isinstance(memory_item, MemoryItem)
        mock_embedder.embed.assert_called_once_with(test_text)
        mock_vector_store.add.assert_called_once()
        assert mock_vector_store.add.call_args[0][1] == mock_embeddings
        assert mock_vector_store.add.call_args[0][2] == test_metadata

    def test_search_memories(self, memos_with_mocks, mock_embedder, mock_vector_store):
        """Test searching memories"""
        memos = memos_with_mocks
        test_query = "Test search"
        mock_embeddings = [0.1, 0.2, 0.3]
        mock_results = [
            MemoryItem(id="1", memory="Result 1"),
            MemoryItem(id="2", memory="Result 2")
        ]
        
        # Setup mocks
        mock_embedder.embed.return_value = mock_embeddings
        mock_vector_store.search.return_value = mock_results
        
        # Search
        results = memos.search(test_query, limit=2)
        
        # Verify
        assert len(results) == 2
        mock_embedder.embed.assert_called_once_with(test_query)
        mock_vector_store.search.assert_called_once_with(mock_embeddings, limit=2)

    def test_delete_memory(self, memos_with_mocks, mock_vector_store):
        """Test deleting a memory"""
        memos = memos_with_mocks
        memory_id = "test_id"
        mock_vector_store.delete.return_value = True
        
        result = memos.delete(memory_id)
        
        assert result is True
        mock_vector_store.delete.assert_called_once_with(memory_id)

    def test_clear_memories(self, memos_with_mocks, mock_vector_store):
        """Test clearing all memories"""
        memos = memos_with_mocks
        mock_vector_store.clear.return_value = True
        
        result = memos.clear()
        
        assert result is True
        mock_vector_store.clear.assert_called_once() 

def run_tests():
    """Run all tests in this module"""
    pytest.main([__file__, '-v'])

if __name__ == '__main__':
    run_tests() 