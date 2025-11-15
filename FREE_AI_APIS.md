# Free AI APIs Setup Guide

## 🆓 Available Free AI Services

### 1. **Google Gemini** (Currently Active)
- **Website**: https://aistudio.google.com/apikey
- **Free Tier**: 60 requests/minute
- **Model**: gemini-2.5-flash
- **Best For**: Fast, accurate responses with image support

### 2. **Groq** (Fastest!)
- **Website**: https://console.groq.com/keys
- **Free Tier**: 30 requests/minute, very fast inference
- **Model**: llama-3.3-70b-versatile
- **Best For**: Lightning-fast responses
- **Setup**: 
  1. Sign up at https://console.groq.com
  2. Get API key from Keys section
  3. Add to `.env`: `GROQ_API_KEY=your_key_here`

### 3. **Cohere**
- **Website**: https://dashboard.cohere.com/api-keys
- **Free Tier**: 100 requests/minute
- **Model**: command
- **Best For**: Natural language understanding
- **Setup**:
  1. Sign up at https://cohere.com
  2. Get API key from dashboard
  3. Add to `.env`: `COHERE_API_KEY=your_key_here`

### 4. **HuggingFace**
- **Website**: https://huggingface.co/settings/tokens
- **Free Tier**: Unlimited (rate limited)
- **Model**: Mixtral-8x7B-Instruct
- **Best For**: Open-source models
- **Setup**:
  1. Sign up at https://huggingface.co
  2. Create access token
  3. Add to `.env`: `HUGGINGFACE_API_KEY=your_key_here`

## 🔄 How It Works

The assistant automatically tries APIs in this order:
1. **Gemini** (if key available)
2. **Groq** (if Gemini fails)
3. **Cohere** (if Groq fails)
4. **HuggingFace** (if Cohere fails)

## 📝 Quick Setup

1. Get API keys from the websites above
2. Add them to `.env` file:
```env
GEMINI_API_KEY=your_gemini_key
GROQ_API_KEY=your_groq_key
COHERE_API_KEY=your_cohere_key
HUGGINGFACE_API_KEY=your_hf_key
```

3. Restart the server - it will automatically use the best available API!

## 💡 Recommendations

- **Best Overall**: Gemini (image support, accurate)
- **Fastest**: Groq (lightning fast responses)
- **Most Reliable**: Cohere (high rate limits)
- **Most Open**: HuggingFace (open-source models)

## 🚀 All APIs are 100% FREE!
