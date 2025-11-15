import os
import base64
import io

try:
    import google.generativeai as genai
except ImportError:
    genai = None

try:
    from PIL import Image
except ImportError:
    Image = None

class GeminiJavaAssistant:
    def __init__(self):
        self.api_key = os.environ.get('GEMINI_API_KEY')
        self.use_gemini = False
        self.model = None
        self._initialize_gemini()
    
    def _initialize_gemini(self):
        if not self.api_key or genai is None:
            print("⚠️ Gemini not available")
            return
            
        try:
            genai.configure(api_key=self.api_key)
            generation_config = {
                'temperature': 0.7,
                'top_p': 0.95,
                'top_k': 40,
                'max_output_tokens': 2048,
            }
            self.model = genai.GenerativeModel('gemini-2.5-flash', generation_config=generation_config)
            self.use_gemini = True
            print("✅ Gemini AI ready")
        except Exception as e:
            print(f"⚠️ Gemini failed: {e}")
            self.use_gemini = False

    def chat(self, user_input, image_data=None, language="any"):
        if not user_input and not image_data:
            return "Please provide a question or upload an image."
        
        if not self.use_gemini:
            return "❌ Gemini AI not available. Please check API key and internet connection."
        
        try:
            if image_data:
                return self._analyze_image(user_input, image_data, language)
            else:
                return self._process_text(user_input, language)
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    def _analyze_image(self, user_input, image_data, language="any"):
        if Image is None:
            return "📷 Image analysis requires Pillow library."
        
        try:
            image_bytes = base64.b64decode(image_data.split(',')[1])
            image = Image.open(io.BytesIO(image_bytes))
            
            lang_context = f"Focus on {language.upper()} programming" if language != "any" else "Identify the programming language and"
            
            prompt = f"""You are a programming learning assistant. {lang_context} analyze this image:

User question: {user_input or 'Analyze this code or diagram'}

Provide code explanation, error fixes, and clear educational explanations."""
            
            response = self.model.generate_content([prompt, image])
            return response.text
        except Exception as e:
            return f"❌ Image analysis failed: {e}"
    
    def _process_text(self, user_input, language="any"):
        lang_context = f"Focus on {language.upper()} programming" if language != "any" else "Identify the programming language from context or"
        
        prompt = f"""You are a programming learning assistant. {lang_context} answer concisely:

Question: {user_input}

Provide clear explanation with code example if needed. Keep it brief and focused."""
        
        response = self.model.generate_content(prompt)
        return response.text
    
    def get_status(self):
        return "🤖 Gemini AI" if self.use_gemini else "❌ Offline"