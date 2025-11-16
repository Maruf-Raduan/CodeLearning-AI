import os
import base64
import io
import requests

try:
    import google.generativeai as genai
except ImportError:
    genai = None

try:
    from PIL import Image
except ImportError:
    Image = None

class MultiAIAssistant:
    def __init__(self):
        self.gemini_key = os.environ.get('GEMINI_API_KEY')
        self.groq_key = os.environ.get('GROQ_API_KEY')
        self.cohere_key = os.environ.get('COHERE_API_KEY')
        self.hf_key = os.environ.get('HUGGINGFACE_API_KEY')
        self.deepseek_key = os.environ.get('DEEPSEEK_API_KEY')
        self.openai_key = os.environ.get('OPENAI_API_KEY')
        self.perplexity_key = os.environ.get('PERPLEXITY_API_KEY')
        
        self.active_ai = None
        self.model = None
        self._initialize_ai()
    
    def _initialize_ai(self):
        # Try Gemini first
        if self.gemini_key and genai:
            try:
                genai.configure(api_key=self.gemini_key)
                self.model = genai.GenerativeModel('gemini-2.5-flash')
                self.active_ai = 'gemini'
                print("[OK] Gemini AI ready")
                return
            except Exception as e:
                print(f"[WARNING] Gemini failed: {e}")
        
        # Try Groq (Free, very fast)
        if self.groq_key:
            try:
                response = requests.post(
                    'https://api.groq.com/openai/v1/chat/completions',
                    headers={'Authorization': f'Bearer {self.groq_key}'},
                    json={'model': 'llama-3.3-70b-versatile', 'messages': [{'role': 'user', 'content': 'Hi'}], 'max_tokens': 10}
                )
                if response.status_code == 200:
                    self.active_ai = 'groq'
                    print("[OK] Groq AI ready")
                    return
            except Exception as e:
                print(f"[WARNING] Groq failed: {e}")
        
        # Try Cohere (Free tier)
        if self.cohere_key:
            try:
                response = requests.post(
                    'https://api.cohere.ai/v1/generate',
                    headers={'Authorization': f'Bearer {self.cohere_key}'},
                    json={'model': 'command', 'prompt': 'Hi', 'max_tokens': 10}
                )
                if response.status_code == 200:
                    self.active_ai = 'cohere'
                    print("[OK] Cohere AI ready")
                    return
            except Exception as e:
                print(f"[WARNING] Cohere failed: {e}")
        
        # Try HuggingFace (Free)
        if self.hf_key:
            self.active_ai = 'huggingface'
            print("[OK] HuggingFace AI ready")
            return
        
        # Try DeepSeek
        if self.deepseek_key:
            self.active_ai = 'deepseek'
            print("[OK] DeepSeek AI ready")
            return
        
        # Try OpenAI
        if self.openai_key:
            self.active_ai = 'openai'
            print("[OK] OpenAI ready")
            return
        
        # Try Perplexity
        if self.perplexity_key:
            self.active_ai = 'perplexity'
            print("[OK] Perplexity AI ready")
            return
        
        print("[ERROR] No AI available")

    def chat(self, user_input, image_data=None, language="any", ai_model="auto"):
        if not user_input and not image_data:
            return "Please provide a question or upload an image."
        
        # If specific model selected, try that first
        if ai_model != "auto":
            try:
                if ai_model == 'gemini' and self.gemini_key:
                    return self._chat_gemini(user_input, image_data, language)
                elif ai_model == 'groq' and self.groq_key:
                    return self._chat_groq(user_input, language)
                elif ai_model == 'cohere' and self.cohere_key:
                    return self._chat_cohere(user_input, language)
                elif ai_model == 'huggingface' and self.hf_key:
                    return self._chat_huggingface(user_input, language)
                elif ai_model == 'deepseek' and self.deepseek_key:
                    return self._chat_deepseek(user_input, language)
                elif ai_model == 'openai' and self.openai_key:
                    return self._chat_openai(user_input, language)
                elif ai_model == 'perplexity' and self.perplexity_key:
                    return self._chat_perplexity(user_input, language)
                else:
                    return f"[ERROR] {ai_model.title()} not available. Please check API key."
            except Exception as e:
                return f"[ERROR] {ai_model.title()} error: {str(e)}"
        
        # Auto mode - try best available
        if not self.active_ai:
            return "[ERROR] No AI service available. Please add API keys."
        
        try:
            if self.active_ai == 'gemini':
                return self._chat_gemini(user_input, image_data, language)
            elif self.active_ai == 'groq':
                return self._chat_groq(user_input, language)
            elif self.active_ai == 'cohere':
                return self._chat_cohere(user_input, language)
            elif self.active_ai == 'huggingface':
                return self._chat_huggingface(user_input, language)
            elif self.active_ai == 'deepseek':
                return self._chat_deepseek(user_input, language)
            elif self.active_ai == 'openai':
                return self._chat_openai(user_input, language)
            elif self.active_ai == 'perplexity':
                return self._chat_perplexity(user_input, language)
        except Exception as e:
            return f"[ERROR] Error: {str(e)}"
    
    def _chat_gemini(self, user_input, image_data, language):
        if not self.model:
            genai.configure(api_key=self.gemini_key)
            self.model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Map language codes to full names
        lang_map = {
            'cpp': 'C++',
            'csharp': 'C#',
            'javascript': 'JavaScript',
            'typescript': 'TypeScript',
            'python': 'Python',
            'java': 'Java',
            'go': 'Go',
            'rust': 'Rust',
            'php': 'PHP',
            'ruby': 'Ruby',
            'swift': 'Swift',
            'kotlin': 'Kotlin',
            'c': 'C'
        }
        
        lang_name = lang_map.get(language.lower(), language)
        
        if language != "any":
            lang_context = f"Write code ONLY in {lang_name}. Provide complete working code with explanation."
        else:
            lang_context = "Provide complete working code with explanation."
        
        if image_data and Image:
            image_bytes = base64.b64decode(image_data.split(',')[1])
            image = Image.open(io.BytesIO(image_bytes))
            prompt = f"{lang_context}\n\nUser request: {user_input or 'Analyze this code'}"
            response = self.model.generate_content([prompt, image])
        else:
            prompt = f"{lang_context}\n\nUser request: {user_input}\n\nProvide complete code and explanation."
            response = self.model.generate_content(prompt)
        
        return response.text
    
    def _chat_groq(self, user_input, language):
        lang_map = {'cpp': 'C++', 'csharp': 'C#', 'javascript': 'JavaScript', 'typescript': 'TypeScript', 'python': 'Python', 'java': 'Java', 'go': 'Go', 'rust': 'Rust', 'php': 'PHP', 'ruby': 'Ruby', 'swift': 'Swift', 'kotlin': 'Kotlin', 'c': 'C'}
        lang_name = lang_map.get(language.lower(), language)
        
        if language != "any":
            prompt = f"You are a {lang_name} programming expert. Provide complete working code with explanation. User question: {user_input}"
        else:
            prompt = f"You are a programming expert. Provide complete working code with explanation. User question: {user_input}"
        
        try:
            response = requests.post(
                'https://api.groq.com/openai/v1/chat/completions',
                headers={'Authorization': f'Bearer {self.groq_key}', 'Content-Type': 'application/json'},
                json={
                    'model': 'llama-3.3-70b-versatile',
                    'messages': [{'role': 'user', 'content': prompt}],
                    'max_tokens': 2048,
                    'temperature': 0.7
                },
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']
            else:
                return f"[ERROR] Groq API error {response.status_code}: {response.text}"
        except Exception as e:
            return f"[ERROR] Groq connection error: {str(e)}"
    
    def _chat_cohere(self, user_input, language):
        lang_map = {'cpp': 'C++', 'csharp': 'C#', 'javascript': 'JavaScript', 'typescript': 'TypeScript', 'python': 'Python', 'java': 'Java', 'go': 'Go', 'rust': 'Rust', 'php': 'PHP', 'ruby': 'Ruby', 'swift': 'Swift', 'kotlin': 'Kotlin', 'c': 'C'}
        lang_name = lang_map.get(language.lower(), language)
        
        if language != "any":
            prompt = f"You are a {lang_name} programming expert. Provide complete working code with explanation. User question: {user_input}"
        else:
            prompt = f"You are a programming expert. Provide complete working code with explanation. User question: {user_input}"
        
        try:
            response = requests.post(
                'https://api.cohere.com/v1/chat',
                headers={'Authorization': f'Bearer {self.cohere_key}', 'Content-Type': 'application/json'},
                json={
                    'model': 'command',
                    'message': prompt,
                    'max_tokens': 2048,
                    'temperature': 0.7
                },
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()['text']
            else:
                return f"[ERROR] Cohere API error {response.status_code}: {response.text}"
        except Exception as e:
            return f"[ERROR] Cohere connection error: {str(e)}"
    
    def _chat_huggingface(self, user_input, language):
        lang_map = {'cpp': 'C++', 'csharp': 'C#', 'javascript': 'JavaScript', 'typescript': 'TypeScript', 'python': 'Python', 'java': 'Java', 'go': 'Go', 'rust': 'Rust', 'php': 'PHP', 'ruby': 'Ruby', 'swift': 'Swift', 'kotlin': 'Kotlin', 'c': 'C'}
        lang_name = lang_map.get(language.lower(), language)
        
        if language != "any":
            prompt = f"You are a {lang_name} programming expert. Provide complete working code with explanation. User question: {user_input}"
        else:
            prompt = f"You are a programming expert. Provide complete working code with explanation. User question: {user_input}"
        
        try:
            response = requests.post(
                'https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1',
                headers={'Authorization': f'Bearer {self.hf_key}', 'Content-Type': 'application/json'},
                json={'inputs': prompt, 'parameters': {'max_new_tokens': 2048, 'return_full_text': False}},
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    return result[0].get('generated_text', '').replace(prompt, '').strip()
                return str(result)
            else:
                return f"[ERROR] HuggingFace API error {response.status_code}: {response.text}"
        except Exception as e:
            return f"[ERROR] HuggingFace connection error: {str(e)}"
    
    def _chat_deepseek(self, user_input, language):
        lang_map = {'cpp': 'C++', 'csharp': 'C#', 'javascript': 'JavaScript', 'typescript': 'TypeScript', 'python': 'Python', 'java': 'Java', 'go': 'Go', 'rust': 'Rust', 'php': 'PHP', 'ruby': 'Ruby', 'swift': 'Swift', 'kotlin': 'Kotlin', 'c': 'C'}
        lang_name = lang_map.get(language.lower(), language)
        
        if language != "any":
            prompt = f"You are a {lang_name} programming expert. Provide complete working code with explanation. User question: {user_input}"
        else:
            prompt = f"You are a programming expert. Provide complete working code with explanation. User question: {user_input}"
        
        try:
            response = requests.post(
                'https://api.deepseek.com/chat/completions',
                headers={'Authorization': f'Bearer {self.deepseek_key}', 'Content-Type': 'application/json'},
                json={
                    'model': 'deepseek-chat',
                    'messages': [{'role': 'user', 'content': prompt}],
                    'max_tokens': 2048,
                    'temperature': 0.7
                },
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']
            else:
                return f"[ERROR] DeepSeek API error {response.status_code}: {response.text}"
        except Exception as e:
            return f"[ERROR] DeepSeek connection error: {str(e)}"
    
    def _chat_openai(self, user_input, language):
        lang_map = {'cpp': 'C++', 'csharp': 'C#', 'javascript': 'JavaScript', 'typescript': 'TypeScript', 'python': 'Python', 'java': 'Java', 'go': 'Go', 'rust': 'Rust', 'php': 'PHP', 'ruby': 'Ruby', 'swift': 'Swift', 'kotlin': 'Kotlin', 'c': 'C'}
        lang_name = lang_map.get(language.lower(), language)
        
        if language != "any":
            prompt = f"You are a {lang_name} programming expert. Provide complete working code with explanation. User question: {user_input}"
        else:
            prompt = f"You are a programming expert. Provide complete working code with explanation. User question: {user_input}"
        
        try:
            response = requests.post(
                'https://api.openai.com/v1/chat/completions',
                headers={'Authorization': f'Bearer {self.openai_key}', 'Content-Type': 'application/json'},
                json={
                    'model': 'gpt-4o-mini',
                    'messages': [{'role': 'user', 'content': prompt}],
                    'max_tokens': 2048,
                    'temperature': 0.7
                },
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']
            else:
                return f"[ERROR] OpenAI API error {response.status_code}: {response.text}"
        except Exception as e:
            return f"[ERROR] OpenAI connection error: {str(e)}"
    
    def _chat_perplexity(self, user_input, language):
        lang_map = {'cpp': 'C++', 'csharp': 'C#', 'javascript': 'JavaScript', 'typescript': 'TypeScript', 'python': 'Python', 'java': 'Java', 'go': 'Go', 'rust': 'Rust', 'php': 'PHP', 'ruby': 'Ruby', 'swift': 'Swift', 'kotlin': 'Kotlin', 'c': 'C'}
        lang_name = lang_map.get(language.lower(), language)
        
        if language != "any":
            prompt = f"You are a {lang_name} programming expert. Provide complete working code with explanation. User question: {user_input}"
        else:
            prompt = f"You are a programming expert. Provide complete working code with explanation. User question: {user_input}"
        
        try:
            response = requests.post(
                'https://api.perplexity.ai/chat/completions',
                headers={'Authorization': f'Bearer {self.perplexity_key}', 'Content-Type': 'application/json'},
                json={
                    'model': 'llama-3.1-sonar-small-128k-online',
                    'messages': [{'role': 'user', 'content': prompt}],
                    'max_tokens': 2048,
                    'temperature': 0.7
                },
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']
            else:
                return f"[ERROR] Perplexity API error {response.status_code}: {response.text}"
        except Exception as e:
            return f"[ERROR] Perplexity connection error: {str(e)}"
    
    def get_status(self):
        if self.active_ai == 'gemini':
            return "Gemini AI"
        elif self.active_ai == 'groq':
            return "Groq AI"
        elif self.active_ai == 'cohere':
            return "Cohere AI"
        elif self.active_ai == 'huggingface':
            return "HuggingFace AI"
        elif self.active_ai == 'deepseek':
            return "DeepSeek AI"
        elif self.active_ai == 'openai':
            return "OpenAI"
        elif self.active_ai == 'perplexity':
            return "Perplexity AI"
        else:
            return "Offline"
    
    @property
    def use_gemini(self):
        return self.active_ai is not None
