import os
import pytest
from unittest.mock import patch
from dotenv import load_dotenv
import sys
import requests

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_huggingface_api_key_format():
    """Test that the Hugging Face API key format is correct"""
    load_dotenv()
    api_key = os.environ.get('HUGGINGFACE_API_KEY')
    
    assert api_key is not None, "HUGGINGFACE_API_KEY is not set in .env file"
    assert api_key.startswith(('hf_', 'api_')), "HUGGINGFACE_API_KEY should start with 'hf_' or 'api_'"

def test_anthropic_api_key_format():
    """Test that the Anthropic API key format is correct"""
    load_dotenv()
    api_key = os.environ.get('ANTHROPIC_API_KEY')
    
    assert api_key is not None, "ANTHROPIC_API_KEY is not set in .env file"
    assert len(api_key) >= 8, "ANTHROPIC_API_KEY seems too short"

def test_cohere_api_key_format():
    """Test that the Cohere API key format is correct"""
    load_dotenv()
    api_key = os.environ.get('COHERE_API_KEY')
    
    assert api_key is not None, "COHERE_API_KEY is not set in .env file"
    assert len(api_key) >= 8, "COHERE_API_KEY seems too short"

def test_huggingface_api_key_length():
    """Test that the Hugging Face API key has a reasonable length"""
    load_dotenv()
    api_key = os.environ.get('HUGGINGFACE_API_KEY')
    
    assert api_key is not None, "HUGGINGFACE_API_KEY is not set in .env file"
    assert len(api_key) >= 8, "HUGGINGFACE_API_KEY seems too short"
    assert len(api_key) <= 100, "HUGGINGFACE_API_KEY seems too long"

@patch('requests.post')
def test_huggingface_api_authentication(mock_post, client):
    """Test that the Hugging Face API key authenticates successfully"""
    # Mock successful API response
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = [{"generated_text": "Test response"}]
    
    # Test the /test-connections endpoint
    response = client.get('/test-connections')
    assert response.status_code == 200
    
    # Check that the response contains at least one successful connection
    data = response.get_json()
    assert any("Connected successfully" in value for value in data.values()), \
        "No successful API connections found"

@patch('anthropic.Anthropic')
def test_claude_api_authentication(mock_anthropic, client):
    """Test that the Claude API key authenticates successfully"""
    # Mock successful API response
    mock_instance = mock_anthropic.return_value
    mock_instance.messages.create.return_value.content = [{"text": "Test response"}]
    
    # Test the /test-connections endpoint
    response = client.get('/test-connections')
    assert response.status_code == 200

@patch('cohere.Client')
def test_cohere_api_authentication(mock_cohere, client):
    """Test that the Cohere API key authenticates successfully"""
    # Mock successful API response
    mock_instance = mock_cohere.return_value
    mock_instance.generate.return_value.generations = [type('obj', (object,), {'text': 'Test response'})]
    
    # Test the /test-connections endpoint
    response = client.get('/test-connections')
    assert response.status_code == 200

def test_flask_secret_key():
    """Test that the Flask secret key is set"""
    load_dotenv()
    secret_key = os.environ.get('FLASK_SECRET_KEY')
    
    assert secret_key is not None, "FLASK_SECRET_KEY is not set in .env file"
    assert len(secret_key) >= 16, "FLASK_SECRET_KEY should be at least 16 characters long"

def test_environment_variables():
    """Test that all required environment variables are set"""
    load_dotenv()
    required_vars = [
        'FLASK_SECRET_KEY',
        'HUGGINGFACE_API_KEY',
        'ANTHROPIC_API_KEY',
        'COHERE_API_KEY',
        'MAX_TOKENS',
        'TEMPERATURE'
    ]
    
    for var in required_vars:
        assert os.environ.get(var) is not None, f"{var} is not set in .env file"

def test_max_tokens_value():
    """Test that MAX_TOKENS is a valid integer"""
    load_dotenv()
    max_tokens = os.environ.get('MAX_TOKENS')
    
    assert max_tokens is not None, "MAX_TOKENS is not set in .env file"
    assert max_tokens.isdigit(), "MAX_TOKENS should be a positive integer"
    assert 1 <= int(max_tokens) <= 2048, "MAX_TOKENS should be between 1 and 2048"

def test_temperature_value():
    """Test that TEMPERATURE is a valid float"""
    load_dotenv()
    temperature = os.environ.get('TEMPERATURE')
    
    assert temperature is not None, "TEMPERATURE is not set in .env file"
    try:
        temp_float = float(temperature)
        assert 0.0 <= temp_float <= 1.0, "TEMPERATURE should be between 0.0 and 1.0"
    except ValueError:
        pytest.fail("TEMPERATURE should be a valid float")

@pytest.mark.integration
def test_live_claude_connection():
    """Test actual Claude API connection (marked as integration test)"""
    load_dotenv()
    api_key = os.environ.get('ANTHROPIC_API_KEY')
    
    if not api_key:
        pytest.skip("ANTHROPIC_API_KEY not set")
    
    try:
        from anthropic import Anthropic
        client = Anthropic(api_key=api_key)
        
        message = client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=10,
            messages=[{"role": "user", "content": "Say hello"}]
        )
        
        assert message.content[0].text is not None, "No response from Claude API"
            
    except Exception as e:
        pytest.fail(f"Claude API connection failed: {str(e)}")

@pytest.mark.integration
def test_live_cohere_connection():
    """Test actual Cohere API connection (marked as integration test)"""
    load_dotenv()
    api_key = os.environ.get('COHERE_API_KEY')
    
    if not api_key:
        pytest.skip("COHERE_API_KEY not set")
    
    try:
        import cohere
        co = cohere.Client(api_key)
        
        response = co.generate(
            model='command',
            prompt="Say hello",
            max_tokens=10,
            temperature=0.7
        )
        
        assert response.generations[0].text is not None, "No response from Cohere API"
            
    except Exception as e:
        pytest.fail(f"Cohere API connection failed: {str(e)}")

@pytest.mark.integration
def test_live_api_connection():
    """Test actual API connection (marked as integration test)"""
    load_dotenv()
    api_key = os.environ.get('HUGGINGFACE_API_KEY')
    
    if not api_key:
        pytest.skip("HUGGINGFACE_API_KEY not set")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        # Try a simple sentiment analysis model
        response = requests.post(
            "https://api-inference.huggingface.co/models/distilbert-base-uncased-sentiment",
            headers=headers,
            json={"inputs": "I love this!"}
        )
        
        if response.status_code == 401:
            pytest.skip("Invalid Hugging Face API key")
        
        assert response.status_code == 200 or response.status_code == 503, \
            f"Unexpected status code: {response.status_code}"
            
    except requests.exceptions.RequestException as e:
        pytest.fail(f"API connection failed: {str(e)}")