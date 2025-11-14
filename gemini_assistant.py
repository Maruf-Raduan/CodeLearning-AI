import os
import google.generativeai as genai
from java_learning_assistant import JavaLearningAssistant

class GeminiJavaAssistant:
    def __init__(self):
        self.fallback_assistant = JavaLearningAssistant()
        self.api_key = os.environ.get('GEMINI_API_KEY')
        
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-pro')
            self.use_gemini = True
        else:
            self.use_gemini = False
            print("⚠️  No Gemini API key found. Using fallback assistant.")
    
    def chat(self, user_input):
        # Check if it's code validation
        if '{' in user_input and '}' in user_input:
            return ', '.join(self.fallback_assistant.check_code(user_input))
        
        # Use Gemini if available
        if self.use_gemini:
            try:
                prompt = f"""You are a Java learning assistant. Answer this question about Java programming:

Question: {user_input}

Rules:
- Keep answers concise and educational
- Include code examples when relevant
- Focus on Java programming concepts
- If asked for examples, provide working Java code
- Be friendly and encouraging
- If it's not Java-related, politely redirect to Java topics"""

                response = self.model.generate_content(prompt)
                return response.text
            
            except Exception as e:
                print(f"Gemini API error: {e}")
                return self.fallback_assistant.chat(user_input)
        
        # Fallback to rule-based assistant
        return self.fallback_assistant.chat(user_input)
