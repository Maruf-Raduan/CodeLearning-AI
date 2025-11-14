# 🚀 Gemini API Setup Guide

## Get FREE Gemini API Key

1. **Go to Google AI Studio**
   - Visit: https://makersuite.google.com/app/apikey
   - Sign in with your Google account

2. **Create API Key**
   - Click "Create API Key"
   - Copy your API key

3. **Add to Your Project**

### For Local Development:
```bash
# Create .env file
echo "GEMINI_API_KEY=your_api_key_here" > .env

# Run the app
python app.py
```

### For Replit:
1. Click "Secrets" (🔒 icon in left sidebar)
2. Add new secret:
   - Key: `GEMINI_API_KEY`
   - Value: `your_api_key_here`
3. Click "Run"

### For Render.com:
1. Go to your service dashboard
2. Click "Environment"
3. Add environment variable:
   - Key: `GEMINI_API_KEY`
   - Value: `your_api_key_here`
4. Save and redeploy

## Free Tier Limits
- ✅ **60 requests per minute**
- ✅ **1,500 requests per day**
- ✅ **100% FREE** (no credit card required)

## Features with Gemini
- 🤖 **Natural language understanding** - Ask anything about Java
- 💡 **Intelligent explanations** - Get detailed, context-aware answers
- 📝 **Dynamic code generation** - Generate custom Java code examples
- 🎯 **Personalized learning** - Adaptive responses based on your questions
- 🔄 **Fallback system** - Works without API key using built-in knowledge

## Test It
```bash
# Install dependencies
pip install -r requirements.txt

# Set API key
export GEMINI_API_KEY="your_api_key_here"

# Run
python app.py
```

Visit: http://localhost:8080

## Without API Key
The app still works! It uses the comprehensive built-in Java knowledge base (50+ topics, 60+ concepts).
