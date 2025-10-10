"""
Configuration and fixtures for Concept Pitch Agent tests
"""

import os
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest


@pytest.fixture(scope="function")
def temp_concept_pitch_dir():
    """Create a temporary directory for Concept Pitch test files"""
    temp_dir = tempfile.mkdtemp(prefix="concept_pitch_test_")
    yield Path(temp_dir)
    # Cleanup is handled by the test itself


@pytest.fixture(scope="function")
def mock_concept_pitch_env():
    """Mock environment variables for Concept Pitch tests"""
    with patch.dict(os.environ, {
        "OPENAI_API_KEY": "test-key",
        "LANGCHAIN_API_KEY": "test-key",
        "LANGCHAIN_TRACING_V2": "false"
    }, clear=False):
        yield


@pytest.fixture(scope="function")
def concept_pitch_test_data():
    """Standard test data for Concept Pitch tests"""
    return {
        "icp": "startup founders",
        "pain": "burnout and lack of clarity",
        "gain": "strategic clarity and sustainable growth",
        "prize": "freedom to build what matters",
        "signature_method": "CAOS framework"
    }


@pytest.fixture(scope="function")
def mock_concept_pitch_llm():
    """Mock LLM for Concept Pitch tests"""
    with patch('src.agents.concept_pitch.agent.ChatOpenAI') as mock_chat:
        mock_instance = mock_chat.return_value
        mock_instance.invoke.return_value.content = "Mock LLM response for testing"
        yield mock_instance


@pytest.fixture(scope="function")
def mock_concept_pitch_refine_llm():
    """Mock LLM for Concept Pitch refinement tests"""
    with patch('src.agents.concept_pitch.refine.ChatOpenAI') as mock_chat:
        mock_instance = mock_chat.return_value
        mock_instance.invoke.return_value.content = "Mock refined response for testing"
        yield mock_instance


@pytest.fixture(scope="function")
def mock_llm():
    """Mock LLM for testing"""
    with patch('src.agents.concept_pitch.agent.ChatOpenAI') as mock_chat:
        mock_instance = MagicMock()
        mock_instance.invoke.return_value = MagicMock(content="Mock LLM response for testing")
        mock_chat.return_value = mock_instance
        yield mock_instance


@pytest.fixture(scope="function")
def mock_refine_llm():
    """Mock LLM for refinement testing"""
    with patch('src.agents.concept_pitch.refine.ChatOpenAI') as mock_chat:
        mock_instance = MagicMock()
        mock_instance.invoke.return_value = MagicMock(content="Mock refined response for testing")
        mock_chat.return_value = mock_instance
        yield mock_instance
