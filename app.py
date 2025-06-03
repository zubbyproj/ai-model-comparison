from flask import Flask, request, render_template, jsonify, session
import time
import json
from datetime import datetime
import requests
import os
from dotenv import load_dotenv
import anthropic
import cohere  # Add this import

# Remove debug prints
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'default_secret_key_for_development')

# Verify API keys
HUGGINGFACE_API_KEY = os.environ.get('HUGGINGFACE_API_KEY')
ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY')
COHERE_API_KEY = os.environ.get('COHERE_API_KEY')

# Store API key status
api_key_status = {
    'huggingface': bool(HUGGINGFACE_API_KEY),
    'anthropic': bool(ANTHROPIC_API_KEY),
    'cohere': bool(COHERE_API_KEY)
}

# Request timeout in seconds
REQUEST_TIMEOUT = 30

# AI Model information
ai_model_info = {
    "Cohere-Command": {  # Add Cohere information
        "description": "Cohere's Command model, excellent for understanding context and generating relevant responses.",
        "avg_response_time": "2s",
        "specialties": ["Text Generation", "Analysis", "Classification"],
        "max_tokens": int(os.environ.get('MAX_TOKENS', 512))
    },
    "Claude-2": {
        "description": "Anthropic's Claude-2 model, known for thoughtful and nuanced responses.",
        "avg_response_time": "3s",
        "specialties": ["Analysis", "Writing", "Problem Solving"],
        "max_tokens": int(os.environ.get('MAX_TOKENS', 512))
    },
    "FLAN-T5": {
        "description": "Google's FLAN-T5-Base model, great for various text generation tasks.",
        "avg_response_time": "2s",
        "specialties": ["Question Answering", "Text Generation", "Translation"],
        "max_tokens": int(os.environ.get('MAX_TOKENS', 512))
    },
    "GPT-2": {
        "description": "OpenAI's GPT-2 model (free version), good for creative writing.",
        "avg_response_time": "2s",
        "specialties": ["Creative Writing", "Text Completion", "Story Generation"],
        "max_tokens": int(os.environ.get('MAX_TOKENS', 512))
    },
    "BLOOM": {
        "description": "BigScience's BLOOM model, multilingual text generation.",
        "avg_response_time": "3s",
        "specialties": ["Multilingual Generation", "Code Generation", "Analysis"],
        "max_tokens": int(os.environ.get('MAX_TOKENS', 512))
    },
    "DialoGPT": {
        "description": "Microsoft's DialoGPT, specialized in conversational responses.",
        "avg_response_time": "2s",
        "specialties": ["Conversation", "Chat", "Response Generation"],
        "max_tokens": int(os.environ.get('MAX_TOKENS', 512))
    },
    "OPT": {
        "description": "Meta's OPT model, alternative to GPT-3 with similar capabilities.",
        "avg_response_time": "2s",
        "specialties": ["Text Generation", "Analysis", "Question Answering"],
        "max_tokens": int(os.environ.get('MAX_TOKENS', 512))
    },
    "BART": {
        "description": "Facebook's BART model, excellent for summarization and generation.",
        "avg_response_time": "2s",
        "specialties": ["Summarization", "Text Generation", "Translation"],
        "max_tokens": int(os.environ.get('MAX_TOKENS', 512))
    },
    "T0pp": {
        "description": "Hugging Face's T0++ model, trained on diverse tasks.",
        "avg_response_time": "3s",
        "specialties": ["Zero-shot Learning", "Task Understanding", "General Knowledge"],
        "max_tokens": int(os.environ.get('MAX_TOKENS', 512))
    },
    "GPT-Neo": {
        "description": "EleutherAI's GPT-Neo, open-source alternative to GPT-3.",
        "avg_response_time": "3s",
        "specialties": ["Text Generation", "Code Completion", "Analysis"],
        "max_tokens": int(os.environ.get('MAX_TOKENS', 512))
    },
    "Dolly": {
        "description": "Databricks' Dolly model, instruction-following specialist.",
        "avg_response_time": "2s",
        "specialties": ["Instruction Following", "Task Completion", "Explanation"],
        "max_tokens": int(os.environ.get('MAX_TOKENS', 512))
    },
    "Falcon": {
        "description": "TII's Falcon model, powerful open-source language model.",
        "avg_response_time": "3s",
        "specialties": ["Text Generation", "Analysis", "Problem Solving"],
        "max_tokens": int(os.environ.get('MAX_TOKENS', 512))
    },
    "MPT": {
        "description": "MosaicML's MPT model, efficient and powerful language model.",
        "avg_response_time": "2s",
        "specialties": ["Text Generation", "Chat", "Analysis"],
        "max_tokens": int(os.environ.get('MAX_TOKENS', 512))
    },
    "Pythia": {
        "description": "EleutherAI's Pythia model, trained on code and text.",
        "avg_response_time": "2s",
        "specialties": ["Code Generation", "Technical Writing", "Analysis"],
        "max_tokens": int(os.environ.get('MAX_TOKENS', 512))
    },
    "Qwen3": {
        "description": "Qwen3 8B model, excellent for reasoning, coding, and multilingual tasks.",
        "avg_response_time": "2s",
        "specialties": ["Reasoning", "Coding", "Multilingual Support"],
        "max_tokens": int(os.environ.get('MAX_TOKENS', 512))
    },
    "DeepSeek R1": {
        "description": "DeepSeek R1 is a powerful open-source model with MIT license, excellent for complex reasoning and coding tasks.",
        "avg_response_time": "2s",
        "specialties": ["Complex Reasoning", "Coding", "Technical Analysis"],
        "max_tokens": int(os.environ.get('MAX_TOKENS', 512))
    },
    "Qwen3 30B": {
        "description": "Qwen3 30B A3B is a large model with 30.5B parameters, excellent for mathematics, coding, and creative tasks.",
        "avg_response_time": "3s",
        "specialties": ["Mathematics", "Advanced Coding", "Creative Writing"],
        "max_tokens": int(os.environ.get('MAX_TOKENS', 512))
    }
}

def get_cohere_response(question):
    """Get response from Cohere Command"""
    try:
        if not COHERE_API_KEY:
            return {
                "response": "Error: Cohere API key is not configured. Please set up your API key in the .env file.",
                "confidence": 0,
                "response_time": 0
            }

        start_time = time.time()
        
        co = cohere.Client(COHERE_API_KEY)
        
        response = co.generate(
            model='command',
            prompt=question,
            max_tokens=int(os.environ.get('MAX_TOKENS', 512)),
            temperature=float(os.environ.get('TEMPERATURE', 0.7)),
            k=0,
            stop_sequences=[],
            return_likelihoods='NONE'
        )
        
        response_time = time.time() - start_time
        
        return {
            "response": response.generations[0].text.strip(),
            "confidence": 0.9,
            "response_time": response_time
        }
            
    except Exception as e:
        return get_fallback_response("Cohere-Command", str(e))

def get_huggingface_response(model_id, question):
    """Generic function to get response from Hugging Face's inference API"""
    try:
        if not HUGGINGFACE_API_KEY:
            return {
                "response": "Error: Hugging Face API key is not configured. Please set up your API key in the .env file.",
                "confidence": 0,
                "response_time": 0
            }

        start_time = time.time()
        API_URL = f"https://api-inference.huggingface.co/models/{model_id}"
        headers = {
            "Authorization": f"Bearer {HUGGINGFACE_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "inputs": question,
            "parameters": {
                "max_length": int(os.environ.get('MAX_TOKENS', 512)),
                "temperature": float(os.environ.get('TEMPERATURE', 0.7)),
                "num_return_sequences": 1,
                "do_sample": True,
                "top_p": 0.9,
                "top_k": 50
            }
        }

        response = requests.post(
            API_URL,
            headers=headers,
            json=data,
            timeout=REQUEST_TIMEOUT
        )
        response_time = time.time() - start_time

        if response.status_code == 401:
            return {
                "response": "Error: Invalid or missing API key. Please check your Hugging Face API key configuration.",
                "confidence": 0,
                "response_time": response_time
            }
        elif response.status_code == 503:
            return {
                "response": "The model is currently loading. Please try again in a few minutes.",
                "confidence": 0,
                "response_time": response_time
            }
        elif response.status_code != 200:
            return {
                "response": f"API Error: {response.status_code}. {response.text}",
                "confidence": 0,
                "response_time": response_time
            }

        result = response.json()
        # Handle different response formats
        if isinstance(result, list) and len(result) > 0:
            if isinstance(result[0], dict) and "generated_text" in result[0]:
                text = result[0]["generated_text"]
            else:
                text = result[0]
        else:
            text = str(result)
            
        # Clean up the response
        text = text.replace(question, "", 1).strip()  # Remove the input question if it's repeated
        if len(text) == 0:
            text = "I apologize, but I couldn't generate a meaningful response. Please try rephrasing your question."
            
        return {
            "response": text,
            "confidence": 0.85,
            "response_time": response_time
        }
            
    except requests.exceptions.Timeout:
        return get_fallback_response(model_id, "Request timed out")
    except Exception as e:
        return get_fallback_response(model_id, str(e))

def get_flan_response(question):
    """Get response from FLAN-T5"""
    return get_huggingface_response("google/flan-t5-base", question)

def get_gpt2_response(question):
    """Get response from GPT-2"""
    return get_huggingface_response("gpt2", question)

def get_bloom_response(question):
    """Get response from BLOOM"""
    return get_huggingface_response("bigscience/bloom", question)

def get_dialogpt_response(question):
    """Get response from DialoGPT"""
    return get_huggingface_response("microsoft/DialoGPT-medium", question)

def get_opt_response(question):
    """Get response from OPT"""
    return get_huggingface_response("facebook/opt-1.3b", question)

def get_bart_response(question):
    """Get response from BART"""
    return get_huggingface_response("facebook/bart-large", question)

def get_t0pp_response(question):
    """Get response from T0++"""
    return get_huggingface_response("bigscience/T0pp", question)

def get_gpt_neo_response(question):
    """Get response from GPT-Neo"""
    return get_huggingface_response("EleutherAI/gpt-neo-1.3B", question)

def get_dolly_response(question):
    """Get response from Dolly"""
    return get_huggingface_response("databricks/dolly-v2-3b", question)

def get_falcon_response(question):
    """Get response from Falcon"""
    return get_huggingface_response("tiiuae/falcon-7b", question)

def get_mpt_response(question):
    """Get response from MPT"""
    return get_huggingface_response("mosaicml/mpt-7b", question)

def get_pythia_response(question):
    """Get response from Pythia"""
    return get_huggingface_response("EleutherAI/pythia-1.4b", question)

def get_claude_response(question):
    """Get response from Claude-2"""
    try:
        if not ANTHROPIC_API_KEY:
            return {
                "response": "Error: Anthropic API key is not configured. Please set up your API key in the .env file.",
                "confidence": 0,
                "response_time": 0
            }

        start_time = time.time()
        
        # Initialize the Anthropic client
        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        
        # Create a message using the latest format
        message = client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=int(os.environ.get('MAX_TOKENS', 512)),
            messages=[
                {"role": "user", "content": question}
            ]
        )
        
        response_time = time.time() - start_time
        
        # Handle the response in the latest format
        return {
            "response": message.content[0].text,
            "confidence": 0.95,
            "response_time": response_time
        }
            
    except Exception as e:
        return get_fallback_response("Claude-2", str(e))

def get_qwen3_response(question):
    """Get response from Qwen3 8B"""
    try:
        if not HUGGINGFACE_API_KEY:
            return {
                "response": "Error: Hugging Face API key is not configured. Please set up your API key in the .env file.",
                "confidence": 0,
                "response_time": 0
            }

        start_time = time.time()
        API_URL = "https://api-inference.huggingface.co/models/Qwen/Qwen1.5-7B-Chat"
        headers = {
            "Authorization": f"Bearer {HUGGINGFACE_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "inputs": question,
            "parameters": {
                "max_length": int(os.environ.get('MAX_TOKENS', 512)),
                "temperature": float(os.environ.get('TEMPERATURE', 0.7)),
                "num_return_sequences": 1,
                "do_sample": True,
                "top_p": 0.9,
                "top_k": 50
            }
        }

        response = requests.post(
            API_URL,
            headers=headers,
            json=data,
            timeout=REQUEST_TIMEOUT
        )
        response_time = time.time() - start_time

        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                if isinstance(result[0], dict) and "generated_text" in result[0]:
                    text = result[0]["generated_text"]
                else:
                    text = result[0]
            else:
                text = str(result)
                
            # Clean up the response
            text = text.replace(question, "", 1).strip()
            if len(text) == 0:
                text = "I apologize, but I couldn't generate a meaningful response. Please try rephrasing your question."
                
            return {
                "response": text,
                "confidence": 0.9,
                "response_time": response_time
            }
        else:
            return get_fallback_response("Qwen3", f"API Error: {response.status_code}. {response.text}")
            
    except Exception as e:
        return get_fallback_response("Qwen3", str(e))

def get_deepseek_response(question):
    """Get response from DeepSeek R1"""
    try:
        if not HUGGINGFACE_API_KEY:
            return {
                "response": "Error: Hugging Face API key is not configured. Please set up your API key in the .env file.",
                "confidence": 0,
                "response_time": 0
            }

        start_time = time.time()
        API_URL = "https://api-inference.huggingface.co/models/deepseek-ai/deepseek-coder-6.7b-base"
        headers = {
            "Authorization": f"Bearer {HUGGINGFACE_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "inputs": question,
            "parameters": {
                "max_length": int(os.environ.get('MAX_TOKENS', 512)),
                "temperature": float(os.environ.get('TEMPERATURE', 0.7)),
                "num_return_sequences": 1,
                "do_sample": True,
                "top_p": 0.9,
                "top_k": 50
            }
        }

        response = requests.post(
            API_URL,
            headers=headers,
            json=data,
            timeout=REQUEST_TIMEOUT
        )
        response_time = time.time() - start_time

        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                if isinstance(result[0], dict) and "generated_text" in result[0]:
                    text = result[0]["generated_text"]
                else:
                    text = result[0]
            else:
                text = str(result)
                
            # Clean up the response
            text = text.replace(question, "", 1).strip()
            if len(text) == 0:
                text = "I apologize, but I couldn't generate a meaningful response. Please try rephrasing your question."
                
            return {
                "response": text,
                "confidence": 0.95,
                "response_time": response_time
            }
        else:
            return get_fallback_response("DeepSeek R1", f"API Error: {response.status_code}. {response.text}")
            
    except Exception as e:
        return get_fallback_response("DeepSeek R1", str(e))

def get_qwen30b_response(question):
    """Get response from Qwen3 30B A3B"""
    try:
        if not HUGGINGFACE_API_KEY:
            return {
                "response": "Error: Hugging Face API key is not configured. Please set up your API key in the .env file.",
                "confidence": 0,
                "response_time": 0
            }

        start_time = time.time()
        API_URL = "https://api-inference.huggingface.co/models/Qwen/Qwen1.5-14B-Chat"
        headers = {
            "Authorization": f"Bearer {HUGGINGFACE_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "inputs": question,
            "parameters": {
                "max_length": int(os.environ.get('MAX_TOKENS', 512)),
                "temperature": float(os.environ.get('TEMPERATURE', 0.7)),
                "num_return_sequences": 1,
                "do_sample": True,
                "top_p": 0.9,
                "top_k": 50
            }
        }

        response = requests.post(
            API_URL,
            headers=headers,
            json=data,
            timeout=REQUEST_TIMEOUT
        )
        response_time = time.time() - start_time

        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                if isinstance(result[0], dict) and "generated_text" in result[0]:
                    text = result[0]["generated_text"]
                else:
                    text = result[0]
            else:
                text = str(result)
                
            # Clean up the response
            text = text.replace(question, "", 1).strip()
            if len(text) == 0:
                text = "I apologize, but I couldn't generate a meaningful response. Please try rephrasing your question."
                
            return {
                "response": text,
                "confidence": 0.92,
                "response_time": response_time
            }
        else:
            return get_fallback_response("Qwen3 30B", f"API Error: {response.status_code}. {response.text}")
            
    except Exception as e:
        return get_fallback_response("Qwen3 30B", str(e))

def get_fallback_response(model_name, error_message=None):
    """Enhanced fallback response with optional error message"""
    message = error_message or f"I apologize, but {model_name} is currently unavailable. Please try again later or select a different AI model."
    return {
        "response": message,
        "confidence": 0,
        "response_time": 0
    }

# Map model names to their functions
ai_models = {
    "Cohere-Command": get_cohere_response,  # Add Cohere to the models
    "Claude-2": get_claude_response,
    "FLAN-T5": get_flan_response,
    "GPT-2": get_gpt2_response,
    "BLOOM": get_bloom_response,
    "DialoGPT": get_dialogpt_response,
    "OPT": get_opt_response,
    "BART": get_bart_response,
    "T0pp": get_t0pp_response,
    "GPT-Neo": get_gpt_neo_response,
    "Dolly": get_dolly_response,
    "Falcon": get_falcon_response,
    "MPT": get_mpt_response,
    "Pythia": get_pythia_response,
    "Qwen3": get_qwen3_response,
    "DeepSeek R1": get_deepseek_response,
    "Qwen3 30B": get_qwen30b_response
}

# Store votes (in-memory storage - replace with database in production)
model_votes = {}

@app.context_processor
def utility_processor():
    return {
        'now': datetime.now
    }

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user_question = request.form["question"]
        selected_models = request.form.getlist("ai_models")
        
        if not selected_models:
            return render_template("index.html", 
                                error="Please select at least one AI model",
                                ai_models=ai_models,
                                model_info=ai_model_info,
                                api_key_status=api_key_status)
        
        # Get responses only from selected models
        ai_responses = {}
        errors = []
        
        for model_name in selected_models:
            if model_name in ai_models:
                # Check if required API key is available
                if model_name.startswith("Cohere") and not COHERE_API_KEY:
                    errors.append(f"{model_name} requires Cohere API key")
                    continue
                elif model_name == "Claude-2" and not ANTHROPIC_API_KEY:
                    errors.append(f"{model_name} requires Anthropic API key")
                    continue
                elif not model_name.startswith("Cohere") and model_name != "Claude-2" and not HUGGINGFACE_API_KEY:
                    errors.append(f"{model_name} requires Hugging Face API key")
                    continue
                
                try:
                    response_data = ai_models[model_name](user_question)
                    ai_responses[model_name] = response_data
                except Exception as e:
                    errors.append(f"Error with {model_name}: {str(e)}")
        
        session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        session['last_question'] = user_question
        session['last_responses'] = ai_responses
        
        return render_template("results.html", 
                             question=user_question, 
                             responses=ai_responses,
                             model_info=ai_model_info,
                             session_id=session_id,
                             errors=errors if errors else None)
    
    return render_template("index.html", 
                         ai_models=ai_models, 
                         model_info=ai_model_info,
                         api_key_status=api_key_status)

@app.route("/test-connections")
def test_connections():
    results = {}
    
    for model_name, model_func in ai_models.items():
        try:
            response = model_func("Hello, this is a test.")
            if response.get("confidence", 0) > 0:
                results[model_name] = "Connected successfully"
            else:
                results[model_name] = "Connection failed"
        except Exception as e:
            results[model_name] = f"Error: {str(e)}"
    
    return jsonify(results)

@app.route("/vote", methods=["POST"])
def vote():
    try:
        data = request.json
        model_name = data.get("model")
        vote_type = data.get("vote")
        
        if not model_name or not vote_type:
            return jsonify({"error": "Missing required data"}), 400
        
        if model_name not in model_votes:
            model_votes[model_name] = {"up": 0, "down": 0}
        
        model_votes[model_name][vote_type] += 1
        return jsonify(model_votes[model_name])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/export", methods=["POST"])
def export():
    try:
        data = request.json
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"ai_responses_{timestamp}.json"
        
        # In a production environment, you would save this file and provide a download link
        return jsonify({"filename": filename, "data": data})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/share/<response_id>")
def share(response_id):
    try:
        # In a production environment, implement proper response sharing
        return render_template("shared_response.html", response_id=response_id)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/save-history", methods=["POST"])
def save_history():
    """API endpoint to save question and responses to history"""
    try:
        data = request.json
        session_id = data.get('session_id')
        question = data.get('question')
        responses = data.get('responses')
        
        if not all([session_id, question, responses]):
            return jsonify({
                'success': False,
                'error': 'Missing required data'
            }), 400
            
        # Here you would typically save to a database
        # For now, we'll store in session
        if 'history' not in session:
            session['history'] = []
            
        session['history'].append({
            'session_id': session_id,
            'question': question,
            'responses': responses,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        
        return jsonify({
            'success': True,
            'message': 'History saved successfully'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route("/api/get-response-data/<session_id>")
def get_response_data(session_id):
    """API endpoint to get response data for a specific session"""
    try:
        if not session_id:
            return jsonify({
                'success': False,
                'error': 'Session ID required'
            }), 400
            
        # Get data from session
        history = session.get('history', [])
        response_data = next(
            (item for item in history if item['session_id'] == session_id),
            None
        )
        
        if not response_data:
            return jsonify({
                'success': False,
                'error': 'Response data not found'
            }), 404
            
        return jsonify({
            'success': True,
            'data': response_data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route("/api/get-history")
def get_history():
    """API endpoint to get all history items"""
    try:
        history = session.get('history', [])
        return jsonify({
            'success': True,
            'history': history
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route("/view-responses/<session_id>")
def view_responses(session_id):
    """Route to view previous responses"""
    return render_template("results.html", 
                         from_history=True,
                         session_id=session_id,
                         model_info=ai_model_info)

if __name__ == "__main__":
    # Only use debug mode in development
    debug_mode = os.environ.get('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', debug=debug_mode)