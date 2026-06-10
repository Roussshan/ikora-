"""
AI Service - Google Gemini Integration for Conversational Responses
"""
import os
import json
import requests
from utils.logger import logger

# Configure Gemini API
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent"

def generate_ai_response(user_message, emotion, gita_references, conversation_history=None):
    """
    Generate AI response using Google Gemini with Bhagavad Gita context
    
    Args:
        user_message: User's current message
        emotion: Detected emotion (dominant emotion and scores)
        gita_references: List of relevant Bhagavad Gita teachings from database
        conversation_history: Recent conversation context
    
    Returns:
        AI-generated response string
    """
    if not GEMINI_API_KEY or GEMINI_API_KEY == 'your-gemini-api-key-here':
        logger.warning('⚠️  Gemini API key not configured')
        return None
    
    try:
        # Build the system context
        system_context = """You are Ikora, a warm and empathetic friend who happens to know the Bhagavad Gita well. You're having a real conversation with someone who needs support.

CRITICAL RULES:
1. Talk like a caring friend, NOT like a textbook or teacher
2. Keep responses SHORT - maximum 2-3 sentences
3. ALWAYS acknowledge their specific situation first
4. Ask ONE follow-up question to keep the conversation going
5. Weave in Gita wisdom SUBTLY - don't preach or quote directly
6. Be conversational - use contractions (I'm, you're, don't, can't)
7. Show empathy BEFORE giving advice

EXAMPLES OF GOOD RESPONSES:
User: "I'm stressed about work"
Good: "Work stress can feel overwhelming, I get it. The Gita reminds us we can only control our effort, not the results - so focus on doing your best right now. What's the biggest thing stressing you out?"

User: "I'm happy today"
Good: "That's wonderful to hear! Hold onto this feeling - it'll help you through tougher days. What's bringing you joy right now?"

AVOID:
- Long philosophical explanations
- Formal language like "beloved friend" or "dear one"
- Multiple pieces of advice in one response
- Sounding like a guru or teacher"""
        
        # Build context parts
        context_parts = [system_context]
        
        # Add emotion context
        context_parts.append(f"\n\nUser's emotional state: {emotion['dominant']} (confidence: {emotion['confidence']:.0%})")
        
        # Add Gita references if available
        if gita_references:
            context_parts.append("\n\nRelevant Bhagavad Gita wisdom to draw from (use naturally, don't quote directly):")
            for i, ref in enumerate(gita_references[:3], 1):
                context_parts.append(f"{i}. {ref.get('answer', '')}")
        
        # Add conversation history
        if conversation_history and len(conversation_history) > 1:
            context_parts.append("\n\nRecent conversation:")
            for msg in conversation_history[-4:]:
                role = "User" if msg['role'] == 'user' else "You (Ikora)"
                context_parts.append(f"{role}: {msg['content']}")
        
        # Add current user message
        context_parts.append(f"\n\nUser's current message: {user_message}")
        context_parts.append("\nRespond as Ikora with empathy and wisdom:")
        
        full_prompt = "\n".join(context_parts)
        
        # Generate response using Gemini API
        logger.info('🤖 Generating AI response with Gemini...')
        
        url = f"{GEMINI_API_URL}?key={GEMINI_API_KEY}"
        
        headers = {
            "Content-Type": "application/json"
        }
        
        data = {
            "contents": [{
                "parts": [{
                    "text": full_prompt
                }]
            }],
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 200
            }
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('candidates') and len(result['candidates']) > 0:
                candidate = result['candidates'][0]
                if candidate.get('content') and candidate['content'].get('parts'):
                    ai_response = candidate['content']['parts'][0]['text'].strip()
                    logger.info('✅ AI response generated successfully')
                    return ai_response
            logger.warning('⚠️  AI response was empty')
            return None
        else:
            logger.error(f'Gemini API error: {response.status_code} - {response.text}')
            return None
            
    except Exception as e:
        logger.error(f'Error generating AI response: {str(e)}')
        return None

def is_ai_enabled():
    """Check if AI service is properly configured"""
    return GEMINI_API_KEY and GEMINI_API_KEY != 'your-gemini-api-key-here'
