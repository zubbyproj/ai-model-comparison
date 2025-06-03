import pytest
import os
from dotenv import load_dotenv

@pytest.fixture(autouse=True)
def load_env():
    """Automatically load environment variables before each test"""
    load_dotenv()

@pytest.fixture
def mock_env_vars(monkeypatch):
    """Fixture to set mock environment variables"""
    mock_vars = {
        'FLASK_SECRET_KEY': 'test_secret_key_123456',
        'HUGGINGFACE_API_KEY': 'hf_test_key_123456789',
        'MAX_TOKENS': '512',
        'TEMPERATURE': '0.7'
    }
    
    for key, value in mock_vars.items():
        monkeypatch.setenv(key, value)
    
    return mock_vars

@pytest.fixture
def test_env_file(tmp_path):
    """Create a temporary .env file for testing"""
    env_content = """
FLASK_SECRET_KEY=test_secret_key_123456
HUGGINGFACE_API_KEY=hf_test_key_123456789
MAX_TOKENS=512
TEMPERATURE=0.7
"""
    env_file = tmp_path / ".env"
    env_file.write_text(env_content)
    return env_file 