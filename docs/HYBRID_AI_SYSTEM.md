# Hybrid AI System Documentation

## Overview

The AI Tutor platform now uses a **Hybrid AI System** that intelligently combines both **Google Gemini** and **OpenAI GPT** models for optimal results.

## Architecture

### Components

1. **`gemini_service.py`** - Google Gemini AI integration
   - Model: `gemini-2.5-flash`
   - Strengths: Fast, free-tier available, excellent for educational content
   - Use cases: Lessons, explanations, quizzes

2. **`openai_service.py`** - OpenAI GPT integration
   - Model: `gpt-4o-mini` (configurable)
   - Strengths: Advanced reasoning, coding help, complex tasks
   - Use cases: Complex reasoning, code generation, detailed analysis

3. **`hybrid_ai_service.py`** - Intelligent orchestration layer
   - Automatically selects the best provider for each task
   - Implements fallback mechanism if one provider fails
   - Supports comparison mode (use both and compare results)

## Configuration

### Environment Variables (`.env`)

```bash
# Google Gemini API
GEMINI_API_KEY=your-gemini-api-key

# OpenAI API
OPENAI_API_KEY=your-openai-api-key

# Provider selection: 'gemini', 'openai', or 'hybrid'
DEFAULT_AI_PROVIDER=hybrid
```

### Provider Selection Strategy

The hybrid system uses intelligent routing based on task type:

| Task Type | Primary Provider | Reason |
|-----------|-----------------|--------|
| Lessons | Gemini | Optimized for educational content, faster |
| Quizzes | Gemini | Great at structured Q&A generation |
| Explanations | Gemini | Clear, concise explanations |
| Code Help | OpenAI | Superior coding assistance |
| Complex Reasoning | OpenAI | Advanced analytical capabilities |
| Chat (General) | Random/Configured | Load balancing |

## How It Works

### Automatic Fallback

If the primary provider fails (API error, quota exceeded, etc.), the system automatically falls back to the secondary provider:

```python
# Example: User sends a chat message
response = hybrid_ai_service.chat(messages)

# Behind the scenes:
# 1. Tries Gemini first (if configured for chat)
# 2. If Gemini fails → automatically tries OpenAI
# 3. Returns successful response with metadata
```

### Response Metadata

All responses include provider information:

```json
{
  "success": true,
  "content": "Response text...",
  "provider": "gemini",
  "model": "gemini-2.5-flash",
  "response_time": 2.5,
  "fallback": false
}
```

## Usage Examples

### Basic Chat

```python
from apps.ai_tutor.hybrid_ai_service import hybrid_ai_service

messages = [
    {'role': 'user', 'content': 'Explain Python functions'}
]

response = hybrid_ai_service.chat(messages)
```

### Task-Specific Routing

```python
# For coding help - use OpenAI
response = hybrid_ai_service.chat(
    messages,
    task_type='code'  # Routes to OpenAI
)

# For lesson generation - use Gemini
response = hybrid_ai_service.generate_lesson(
    topic='Python Basics',
    learning_style='visual',
    difficulty='beginner'
)
```

### Comparison Mode

Get responses from both providers to compare quality:

```python
response = hybrid_ai_service.generate_with_comparison(
    prompt="Explain object-oriented programming"
)

# Returns:
# {
#   'gemini': {...gemini response...},
#   'openai': {...openai response...},
#   'comparison_mode': True
# }
```

## API Endpoints

All existing AI endpoints now use the hybrid system:

### Chat Endpoints
- `POST /api/ai-tutor/chat/` - Create chat session
- `POST /api/ai-tutor/chat/{id}/message/` - Send message (uses hybrid AI)

### Content Generation
- `POST /api/ai-tutor/generate/lesson/` - Generate lesson (Gemini preferred)
- `POST /api/ai-tutor/generate/quiz/` - Generate quiz (Gemini preferred)
- `POST /api/ai-tutor/explain/` - Explain concept (Gemini preferred)

## Benefits

### 1. **Reliability**
- If one provider is down, the other takes over automatically
- No service interruption for users

### 2. **Cost Optimization**
- Uses free-tier Gemini for most educational tasks
- Reserves paid OpenAI credits for complex tasks

### 3. **Best-in-Class Performance**
- Leverages each provider's strengths
- Gemini: Fast educational content
- OpenAI: Advanced reasoning and coding

### 4. **Flexibility**
- Easy to switch providers via environment variable
- Can use both for comparison/validation

## Performance

### Response Times (Average)

| Task | Gemini | OpenAI |
|------|--------|--------|
| Simple Chat | 1-3s | 2-4s |
| Lesson Generation | 5-10s | 8-15s |
| Quiz Generation | 3-7s | 5-10s |
| Code Explanation | 2-5s | 3-6s |

### Token Usage

Gemini typically uses fewer tokens for the same task, making it more cost-effective for educational content.

## Monitoring

The system logs all AI interactions:

```python
INFO: Using gemini-2.5-flash for chat
INFO: Gemini cache hit: generate_lesson
WARNING: Primary provider failed, falling back to OpenAI
```

## Troubleshooting

### OpenAI Quota Exceeded

If you see `Error 429 - insufficient_quota`:
1. The system automatically falls back to Gemini
2. Add credits to your OpenAI account at https://platform.openai.com/account/billing
3. Or set `DEFAULT_AI_PROVIDER=gemini` to use only Gemini

### Gemini API Errors

If Gemini fails:
1. System automatically tries OpenAI
2. Check your Gemini API key at https://makersuite.google.com/app/apikey
3. Verify the key is in `.env` file

### Both Providers Failing

If both fail:
- Check internet connectivity
- Verify both API keys are valid
- Check provider status pages:
  - Gemini: https://status.cloud.google.com/
  - OpenAI: https://status.openai.com/

## Future Enhancements

Planned features:
- [ ] Response quality scoring to auto-select best provider
- [ ] Cost tracking and optimization
- [ ] A/B testing framework for provider comparison
- [ ] Custom model configuration per user
- [ ] Multi-provider consensus for critical tasks

## Security Notes

- API keys stored in `.env` (never commit to git)
- Keys loaded securely through Django settings
- All API calls use HTTPS
- User data never sent to multiple providers unless in comparison mode

---

**Current Status**: ✅ Fully Operational
- Gemini: Working
- OpenAI: API connected (requires billing setup for production use)
- Hybrid System: Active and routing intelligently
