# AI Model Comparison Web Application

A Flask-based web application that allows users to compare responses from multiple AI language models side by side. The application provides a modern, user-friendly interface with features like dark mode, model selection, and response sharing.

## Features

- Compare responses from multiple AI models simultaneously
- Modern UI with dark mode support
- Interactive model selection with checkboxes
- Grid/List view toggle for responses
- Share and export functionality
- Voting system for model responses
- History panel to review past comparisons
- Toast notifications for user feedback

## Supported AI Models

- FLAN-T5 (Google)
- GPT-2 (OpenAI)
- BLOOM (BigScience)
- DialoGPT (Microsoft)
- OPT (Meta)
- BART (Facebook)
- T0pp (Hugging Face)
- GPT-Neo (EleutherAI)
- Dolly (Databricks)
- Falcon (TII)
- MPT (MosaicML)
- Pythia (EleutherAI)

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Hugging Face API key

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd [repository-name]
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory with the following content:
```
FLASK_SECRET_KEY=your_secret_key_here
HUGGINGFACE_API_KEY=your_huggingface_api_key_here
MAX_TOKENS=512
TEMPERATURE=0.7
```

## Environment Variables

- `FLASK_SECRET_KEY`: Secret key for Flask session management
- `HUGGINGFACE_API_KEY`: Your Hugging Face API key (starts with 'hf_' or 'api_')
- `MAX_TOKENS`: Maximum number of tokens in model responses (default: 512)
- `TEMPERATURE`: Temperature parameter for response generation (default: 0.7)

## Running the Application

1. Ensure your virtual environment is activated
2. Start the Flask server:
```bash
python app.py
```
3. Open your browser and navigate to `http://localhost:5000`

## API Endpoints

- `GET /`: Main application interface
- `POST /`: Submit questions and get AI model responses
- `GET /test-connections`: Test AI model API connections
- `POST /vote`: Submit votes for model responses
- `POST /export`: Export response data
- `GET /share/<response_id>`: View shared responses
- `POST /api/save-history`: Save response history
- `GET /api/get-response-data/<session_id>`: Get specific response data
- `GET /api/get-history`: Get all history items
- `GET /view-responses/<session_id>`: View previous responses

## Development

To run the application in debug mode:
```bash
export FLASK_ENV=development
python app.py
```

## Testing

Run the tests using:
```bash
python -m pytest tests/
```

## Security Notes

- Never commit your `.env` file to version control
- Keep your API keys secure and rotate them regularly
- Use environment variables for all sensitive information

## Contributing

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request

## License

[Your chosen license]

## Support

For support, please [create an issue](your-issue-tracker-url) or contact [your-contact-info]. 