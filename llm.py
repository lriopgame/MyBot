import os, requests

API_URL = os.getenv('LLM_API_URL', 'https://api.example.com/v1/chat/completions')
API_KEY = os.getenv('LLM_API_KEY')
MODEL = os.getenv('LLM_MODEL', 'gpt-4o-mini')
DEFAULTS = {'temperature': 0.2, 'max_tokens': 600}

class LLMError(Exception): pass

def llm_complete(user_prompt: str, system_prompt: str = '', **params) -> str:
    if not API_KEY:
        raise LLMError('Нет API ключа')
    payload = {
        'model': params.get('model', MODEL),
        'messages': [
            {'role': 'system', 'content': system_prompt or ''},
            {'role': 'user', 'content': user_prompt.strip()[:4000]}
        ],
        'temperature': params.get('temperature', DEFAULTS['temperature']),
        'max_tokens': params.get('max_tokens', DEFAULTS['max_tokens'])
    }
    headers = {'Authorization': f'Bearer {API_KEY}', 'Content-Type': 'application/json'}
    try:
        r = requests.post(API_URL, json=payload, headers=headers, timeout=30)
        r.raise_for_status()
        data = r.json()
        return data['choices'][0]['message']['content'].strip()
    except Exception as e:
        raise LLMError(str(e))
import os, requests

API_URL = os.getenv('LLM_API_URL', 'https://api.example.com/v1/chat/completions')
API_KEY = os.getenv('LLM_API_KEY')
MODEL = os.getenv('LLM_MODEL', 'gpt-4o-mini')
DEFAULTS = {'temperature': 0.2, 'max_tokens': 600}

class LLMError(Exception): pass

def llm_complete(user_prompt: str, system_prompt: str = '', **params) -> str:
    if not API_KEY:
        raise LLMError('Нет API ключа')
    payload = {
        'model': params.get('model', MODEL),
        'messages': [
            {'role': 'system', 'content': system_prompt or ''},
            {'role': 'user', 'content': user_prompt.strip()[:4000]}
        ],
        'temperature': params.get('temperature', DEFAULTS['temperature']),
        'max_tokens': params.get('max_tokens', DEFAULTS['max_tokens'])
    }
    headers = {'Authorization': f'Bearer {API_KEY}', 'Content-Type': 'application/json'}
    try:
        r = requests.post(API_URL, json=payload, headers=headers, timeout=30)
        r.raise_for_status()
        data = r.json()
        return data['choices'][0]['message']['content'].strip()
    except Exception as e:
        raise LLMError(str(e))
