# 🤖 AI-Powered Ikora Setup Guide

Your chatbot has been upgraded from simple database lookups to a proper conversational AI that uses Google's Gemini to generate natural, contextual responses while referencing Bhagavad Gita teachings.

## What Changed?

### Before:
- ❌ Just searched database and pasted pre-written answers
- ❌ No conversation context
- ❌ Robotic, repetitive responses

### After:
- ✅ AI generates natural, contextual responses
- ✅ Uses Bhagavad Gita teachings as reference (not direct quotes)
- ✅ Maintains conversation context
- ✅ Adapts to user's emotional state
- ✅ Asks thoughtful follow-up questions

## Setup Instructions

### Step 1: Get Free Gemini API Key

1. Go to: https://makersuite.google.com/app/apikey
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated key

### Step 2: Configure Your Environment

1. Open `bot/backend_python/.env` file (create it if it doesn't exist)
2. Add your API key:

```env
GEMINI_API_KEY=your-actual-api-key-here
```

3. Copy all other settings from `.env.example` if you're creating a new `.env` file

### Step 3: Install New Dependencies

Open terminal in `bot/backend_python` folder and run:

```bash
pip install -r requirements.txt
```

This will install the Google Generative AI library.

### Step 4: Restart Your Backend

Stop your Python backend (if running) and start it again:

```bash
python app.py
```

## How It Works Now

1. **User sends message** → "I'm feeling stressed about my job"

2. **Emotion detection** → Detects "stressed" emotion

3. **Database search** → Finds 3-5 relevant Bhagavad Gita teachings about stress, work, duty

4. **AI generation** → Gemini creates a natural response that:
   - Acknowledges the user's stress empathetically
   - Weaves in Gita wisdom naturally (not as direct quotes)
   - Asks a thoughtful follow-up question
   - Keeps it conversational and supportive

5. **Response** → "I hear you - work stress can feel overwhelming. Remember, the Gita teaches us to focus on our actions, not the outcomes. You can only control your effort, not the results. What aspect of your job is weighing on you most right now?"

## Fallback Behavior

If Gemini API is not configured or fails:
- Falls back to direct database answers (your original system)
- Still works, just less conversational
- No errors or crashes

## Testing

Try these messages to see the difference:

1. "I'm feeling anxious about my future"
2. "I had a fight with my friend and feel guilty"
3. "I'm happy today but want to stay grounded"
4. "I don't know what my purpose is"

You should see natural, contextual responses that feel like talking to a real counselor, not a database.

## Cost & Limits

- **Free tier**: 60 requests per minute
- **Cost**: Free for moderate usage
- **Perfect for**: Personal projects, testing, small user base

## Alternative: OpenAI GPT

If you prefer ChatGPT-style responses, you can switch to OpenAI:

1. Get API key from: https://platform.openai.com/api-keys
2. Install: `pip install openai`
3. Modify `ai_service.py` to use OpenAI instead of Gemini

Let me know if you need help with OpenAI integration!

## Troubleshooting

### "AI responses disabled" in logs
- Check if `GEMINI_API_KEY` is set in `.env`
- Make sure it's not the placeholder value
- Restart the backend after adding the key

### API errors
- Check your API key is valid
- Verify you haven't exceeded free tier limits
- Check internet connection

### Responses still feel robotic
- Make sure the API key is properly configured
- Check logs to confirm "AI response generated successfully"
- Try clearing conversation history and starting fresh

## Need Help?

Check the logs - they'll tell you exactly what's happening:
- 🔍 Searching for Gita references
- 🤖 Generating AI response
- ✅ Success messages
- ⚠️  Warnings and fallbacks
