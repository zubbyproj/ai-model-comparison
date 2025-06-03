# AI Model Comparison Web Application

A Flask-based web application that allows users to compare responses from multiple AI language models side by side. The application provides a modern, user-friendly interface with features like dark mode, model selection, and response sharing.

## Live Demo
You can try the application at: [Your Render URL after deployment]

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
- Qwen3 (8B model)
- DeepSeek R1
- Qwen3 30B
- Claude-2 (Anthropic)
- Cohere Command

## Try It Yourself

1. Visit the live demo at: [Your Render URL after deployment]
2. Enter your question in the text area
3. Select one or more AI models to compare
4. Click "Get AI Answers" to see the responses

## Local Development

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

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

4. Create a `.env` file in the root directory:
```
FLASK_ENV=development
FLASK_SECRET_KEY=your_secret_key_here
HUGGINGFACE_API_KEY=your_huggingface_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
COHERE_API_KEY=your_cohere_api_key_here
MAX_TOKENS=512
TEMPERATURE=0.7
```

### Running Locally

```bash
python app.py
```

Visit `http://localhost:5000` in your browser.

## Deploy Your Own Instance

1. Fork this repository
2. Sign up for a free account at [Render.com](https://render.com)
3. Create a new Web Service and connect your forked repository
4. Add your API keys as environment variables:
   - `HUGGINGFACE_API_KEY`
   - `ANTHROPIC_API_KEY`
   - `COHERE_API_KEY`
5. Deploy!

## API Keys

To use all features, you'll need API keys from:
- [Hugging Face](https://huggingface.co/settings/tokens)
- [Anthropic](https://www.anthropic.com/product)
- [Cohere](https://dashboard.cohere.com/api-keys)

The application will work with any combination of API keys - models will be disabled if their corresponding API key is not provided.

## Contributing

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request

## License

[MIT License](LICENSE)

## Support

For support, please [create an issue](your-issue-tracker-url). 