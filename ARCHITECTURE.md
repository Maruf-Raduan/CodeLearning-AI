# 🏗️ CodeLearning-AI Architecture

## Table of Contents
- [Overview](#overview)
- [System Architecture](#system-architecture)
- [Component Details](#component-details)
- [Data Flow](#data-flow)
- [AI Integration](#ai-integration)
- [API Endpoints](#api-endpoints)
- [Frontend Architecture](#frontend-architecture)
- [Security](#security)
- [Scalability](#scalability)

---

## Overview

CodeLearning-AI is a multi-AI powered programming learning platform built with a modern, scalable architecture. The system integrates 7 different AI models to provide intelligent code assistance, explanations, and learning support across 13+ programming languages.

### Technology Stack

**Backend:**
- Python 3.8+
- Flask 3.0+ (Web Framework)
- python-dotenv (Environment Management)
- requests (HTTP Client)

**Frontend:**
- HTML5
- CSS3 (Modern Animations & Gradients)
- Vanilla JavaScript (ES6+)
- Marked.js (Markdown Rendering)
- Prism.js (Syntax Highlighting)

**AI Services:**
- Google Gemini API
- OpenAI API
- DeepSeek API
- Groq API
- Cohere API
- HuggingFace API
- Perplexity API

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Client Browser                        │
│  ┌────────────────┐  ┌──────────────┐  ┌─────────────────┐ │
│  │ Welcome Screen │  │ Chat Interface│  │ History Panel   │ │
│  └────────────────┘  └──────────────┘  └─────────────────┘ │
└───────────────────────────────┬─────────────────────────────┘
                                │ HTTP/HTTPS
                                ▼
┌─────────────────────────────────────────────────────────────┐
│                      Flask Application                       │
│  ┌────────────────────────────────────────────────────────┐ │
│  │                    app.py (Main)                       │ │
│  │  • Route Handlers (/chat, /status, /)                 │ │
│  │  • Request Validation                                  │ │
│  │  • Response Formatting                                 │ │
│  └──────────────────────┬─────────────────────────────────┘ │
│                         │                                    │
│  ┌──────────────────────▼─────────────────────────────────┐ │
│  │          MultiAIAssistant (Core Logic)                 │ │
│  │  • AI Model Selection                                  │ │
│  │  • Fallback Mechanism                                  │ │
│  │  • Error Handling                                      │ │
│  │  • Language Context Management                         │ │
│  └──────────────────────┬─────────────────────────────────┘ │
└────────────────────────┬┴─────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
        ▼                ▼                ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│   Gemini     │  │   OpenAI     │  │  DeepSeek    │
│     API      │  │     API      │  │     API      │
└──────────────┘  └──────────────┘  └──────────────┘
        │                │                │
        ▼                ▼                ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│    Groq      │  │   Cohere     │  │ HuggingFace  │
│     API      │  │     API      │  │     API      │
└──────────────┘  └──────────────┘  └──────────────┘
        │
        ▼
┌──────────────┐
│ Perplexity   │
│     API      │
└──────────────┘
```

---

## Component Details

### 1. Flask Application (`app.py`)

**Responsibilities:**
- HTTP request handling
- Route management
- Static file serving
- CORS configuration
- Environment variable loading

**Key Routes:**
```python
GET  /           # Serve index.html
POST /chat       # Handle chat requests
GET  /status     # Check AI service status
```

**Configuration:**
- Max content length: 16MB (for image uploads)
- Host: 0.0.0.0 (accessible from network)
- Port: 8080 (configurable via PORT env var)
- Debug mode: Enabled in development

---

### 2. MultiAIAssistant (`multi_ai_assistant.py`)

**Core Class Structure:**

```python
class MultiAIAssistant:
    def __init__(self):
        # Initialize API keys
        # Set up active AI model
        # Configure fallback chain
    
    def chat(user_input, image_data, language, ai_model):
        # Main chat interface
        # Route to specific AI model
        # Handle errors and fallbacks
    
    def _chat_gemini(user_input, image_data, language):
        # Gemini-specific implementation
    
    def _chat_openai(user_input, language):
        # OpenAI-specific implementation
    
    # ... other AI model methods
```

**Key Features:**
- **Auto-initialization**: Automatically detects available API keys
- **Priority-based fallback**: Tries AI models in order of preference
- **Error resilience**: Graceful degradation if models fail
- **Language context**: Adapts prompts based on selected language
- **Image support**: Handles image analysis (Gemini only)

---

### 3. Frontend (`index.html`)

**Architecture Layers:**

```
┌─────────────────────────────────────┐
│      Presentation Layer             │
│  • Welcome Screen                   │
│  • Chat Interface                   │
│  • History Panel                    │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│      Business Logic Layer           │
│  • Message Handling                 │
│  • API Communication                │
│  • State Management                 │
│  • History Management               │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│      Utility Layer                  │
│  • Markdown Rendering               │
│  • Syntax Highlighting              │
│  • Image Processing                 │
│  • LocalStorage Management          │
└─────────────────────────────────────┘
```

**Key Components:**

1. **Welcome Screen**
   - Animated gradient background
   - Feature showcase cards
   - Call-to-action button
   - Auto-skip for returning users

2. **Chat Interface**
   - Real-time message display
   - AI model selector
   - Language selector
   - Image upload capability
   - Loading indicators

3. **History Panel**
   - Persistent chat history
   - LocalStorage integration
   - Search and filter
   - Clear history option

---

## Data Flow

### Chat Request Flow

```
User Input
    │
    ▼
┌─────────────────────┐
│ Frontend Validation │
│ • Check input       │
│ • Prepare payload   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  POST /chat         │
│  {                  │
│    message: str,    │
│    language: str,   │
│    ai_model: str,   │
│    image: base64    │
│  }                  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Flask Route Handler │
│ • Parse JSON        │
│ • Extract params    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ MultiAIAssistant    │
│ • Select AI model   │
│ • Build prompt      │
│ • Add context       │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ AI API Call         │
│ • HTTP POST         │
│ • Timeout: 30s      │
│ • Retry on failure  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Response Processing │
│ • Parse JSON        │
│ • Extract text      │
│ • Error handling    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Return to Frontend  │
│ {                   │
│   response: str     │
│ }                   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Display Response    │
│ • Markdown render   │
│ • Syntax highlight  │
│ • Save to history   │
└─────────────────────┘
```

---

## AI Integration

### Model Selection Strategy

**Priority Order (Auto Mode):**
1. **Gemini** - Best overall, supports images
2. **Groq** - Fastest inference
3. **Cohere** - High rate limits
4. **HuggingFace** - Open source
5. **DeepSeek** - Powerful reasoning
6. **OpenAI** - Industry standard
7. **Perplexity** - Search-enhanced

### API Integration Details

#### 1. Google Gemini
```python
Endpoint: genai.GenerativeModel('gemini-2.5-flash')
Features: Text + Image analysis
Rate Limit: 60 req/min
Timeout: 30s
```

#### 2. OpenAI
```python
Endpoint: https://api.openai.com/v1/chat/completions
Model: gpt-4o-mini
Rate Limit: Varies by tier
Timeout: 30s
```

#### 3. DeepSeek
```python
Endpoint: https://api.deepseek.com/chat/completions
Model: deepseek-chat
Rate Limit: Varies
Timeout: 30s
```

#### 4. Groq
```python
Endpoint: https://api.groq.com/openai/v1/chat/completions
Model: llama-3.3-70b-versatile
Rate Limit: 30 req/min
Timeout: 30s
```

#### 5. Cohere
```python
Endpoint: https://api.cohere.com/v1/chat
Model: command
Rate Limit: 100 req/min
Timeout: 30s
```

#### 6. HuggingFace
```python
Endpoint: https://api-inference.huggingface.co/models/...
Model: Mixtral-8x7B-Instruct-v0.1
Rate Limit: Unlimited (throttled)
Timeout: 60s
```

#### 7. Perplexity
```python
Endpoint: https://api.perplexity.ai/chat/completions
Model: llama-3.1-sonar-small-128k-online
Rate Limit: Varies
Timeout: 30s
```

### Error Handling Strategy

```python
try:
    # Attempt primary AI model
    response = ai_model.generate(prompt)
except APIError as e:
    # Log error
    # Try fallback model
    response = fallback_model.generate(prompt)
except Timeout:
    # Return timeout error
    return "Request timed out. Please try again."
except Exception as e:
    # Generic error handling
    return f"Error: {str(e)}"
```

---

## API Endpoints

### POST /chat

**Request:**
```json
{
  "message": "Write a Python function to sort a list",
  "language": "python",
  "ai_model": "auto",
  "image": "data:image/png;base64,..." // optional
}
```

**Response:**
```json
{
  "response": "Here's a Python function to sort a list:\n\n```python\ndef sort_list(arr):\n    return sorted(arr)\n```"
}
```

**Status Codes:**
- 200: Success
- 400: Bad request
- 500: Server error

---

### GET /status

**Response:**
```json
{
  "status": "online",
  "assistant_type": "Gemini AI",
  "gemini_enabled": true
}
```

---

## Frontend Architecture

### State Management

```javascript
// Global State
let selectedImage = null;
let chatHistory = [];

// LocalStorage Keys
- 'javaAssistantHistory': Chat history
- 'visitedBefore': Welcome screen flag
```

### Event Handling

```javascript
// User Actions
- sendMessage()      // Send chat message
- handleImageSelect() // Upload image
- toggleHistory()    // Show/hide history
- clearHistory()     // Clear all history
- startLearning()    // Dismiss welcome screen
```

### Rendering Pipeline

```javascript
User Input
    ↓
addMessage(text, isUser)
    ↓
Markdown Parsing (marked.js)
    ↓
Syntax Highlighting (Prism.js)
    ↓
DOM Injection
    ↓
Scroll to Bottom
```

---

## Security

### API Key Protection
- ✅ `.env` file in `.gitignore`
- ✅ Environment variables only
- ✅ No client-side exposure
- ✅ `.env.example` for templates

### Input Validation
- ✅ Max content length: 16MB
- ✅ File type validation (images only)
- ✅ XSS prevention (sanitized rendering)
- ✅ CORS configuration

### Rate Limiting
- Handled by AI providers
- Client-side throttling recommended
- Error messages for rate limits

---

## Scalability

### Horizontal Scaling
```
Load Balancer
    │
    ├─── Flask Instance 1
    ├─── Flask Instance 2
    └─── Flask Instance 3
```

### Caching Strategy
- Response caching (future enhancement)
- Static asset caching
- Browser caching headers

### Performance Optimization
- Async AI calls (future)
- Request queuing
- Connection pooling
- Lazy loading

### Monitoring
- API response times
- Error rates
- Model availability
- User metrics

---

## Future Enhancements

### Planned Features
1. **User Authentication** - Save preferences and history
2. **Code Execution** - Run code in sandbox
3. **Collaborative Learning** - Share sessions
4. **Advanced Analytics** - Learning insights
5. **Mobile App** - Native iOS/Android
6. **Voice Input** - Speech-to-text
7. **Code Review** - AI-powered code analysis
8. **Project Templates** - Starter code

### Technical Improvements
1. **WebSocket Support** - Real-time streaming
2. **Database Integration** - PostgreSQL/MongoDB
3. **Redis Caching** - Response caching
4. **Docker Deployment** - Containerization
5. **CI/CD Pipeline** - Automated testing
6. **API Rate Limiting** - Server-side throttling
7. **Logging System** - Structured logging
8. **Metrics Dashboard** - Real-time monitoring

---

## Deployment Architecture

### Production Setup

```
┌─────────────────────────────────────────┐
│           CDN (Static Assets)           │
└──────────────────┬──────────────────────┘
                   │
┌──────────────────▼──────────────────────┐
│         Load Balancer (Nginx)           │
└──────────────────┬──────────────────────┘
                   │
        ┌──────────┼──────────┐
        │          │          │
        ▼          ▼          ▼
┌──────────┐ ┌──────────┐ ┌──────────┐
│ Flask 1  │ │ Flask 2  │ │ Flask 3  │
└──────────┘ └──────────┘ └──────────┘
        │          │          │
        └──────────┼──────────┘
                   │
        ┌──────────▼──────────┐
        │   AI API Services   │
        └─────────────────────┘
```

---

## Contributing to Architecture

When contributing, please:
1. Follow existing patterns
2. Document new components
3. Update this architecture doc
4. Add tests for new features
5. Consider scalability

---

<div align="center">

**📚 For more information, see [README.md](README.md)**

Made with ❤️ by Maruf Raduan

</div>
