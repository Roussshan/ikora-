"""
Guidance Generation Service

Logic:
  - Short emotional state messages ("i am sad", "i am happy") → AI responds
    conversationally, with DB entries as context/inspiration
  - Specific problem messages ("i want to kill someone", "i feel hopeless") →
    DB answer used directly
  - Small-talk ("hi", "hello") → AI with no DB context
"""
import re
from services.knowledge_base_service import search_knowledge_base, search_multiple_references
from services.ai_service import generate_ai_response, is_ai_enabled
from utils.logger import logger

# ── Greeting / small-talk words ────────────────────────────────────────────── #
GREETING_WORDS = {
    'hi', 'hello', 'hey', 'hii', 'helo', 'howdy', 'sup', 'yo',
    'good morning', 'good evening', 'good afternoon', 'good night',
    'bye', 'ok', 'okay', 'thanks', 'thank you', 'great', 'cool', 'nice', 'wow'
}

# ── High-specificity phrases → always use DB answer directly ──────────────── #
# These phrases closely match what's actually in the knowledge base
SPECIFIC_PHRASES = [
    # Violence / self-harm
    'suicide', 'suicidal', 'kill myself', 'end my life', 'want to die',
    'kill someone', 'kill him', 'kill her', 'murder', 'hurt someone',
    'want to harm', 'revenge',
    # Emotional crises
    'hopeless', 'no point', 'give up', 'broken', 'worthless',
    'tired of fighting', 'want everything to stop', 'everything to stop',
    'no one understands', 'completely alone',
    # Personal struggles (match DB entries directly)
    'feel like a failure', 'am a failure', 'never enough', 'not enough',
    'mind is my enemy', 'overthink', 'enemy of my mind',
    'too weak to fight', 'weak to fight',
    # Philosophical / spiritual
    'bad people', 'why does god', 'why suffer', 'destiny',
    'why should i even try', 'what is the point of',
]


def _is_small_talk(message: str) -> bool:
    stripped = message.strip().lower().rstrip('!.,?')
    if stripped in GREETING_WORDS:
        return True
    words = stripped.split()
    emotional = {'sad', 'happy', 'angry', 'stressed', 'anxious', 'depressed',
                 'alone', 'lonely', 'tired', 'hopeless', 'afraid', 'scared',
                 'worried', 'pain', 'hurt', 'kill', 'suicide', 'die', 'hate',
                 'unhappy', 'upset', 'broken', 'empty', 'lost', 'confused'}
    if len(words) <= 2 and not any(w in emotional for w in words):
        return True
    return False


def _has_specific_phrase(message: str) -> bool:
    """Return True if the message contains a high-specificity phrase that maps to a DB entry."""
    msg_lower = message.lower()
    return any(phrase in msg_lower for phrase in SPECIFIC_PHRASES)


def _is_general_emotional_state(message: str) -> bool:
    """
    Return True for short general emotional statements like
    'i am sad', 'i feel happy', 'i am stressed' — where the user
    hasn't described a specific situation yet.
    """
    if _has_specific_phrase(message):
        return False
    words = message.strip().split()
    # Short message (≤ 5 words) AND no specific problem phrase
    return len(words) <= 5


def generate_guidance(user_message, emotion, conversation_history=None):
    """Generate guidance response based on user message and emotion."""
    try:
        dominant = emotion['dominant']

        # ── 1. Small-talk → AI only ───────────────────────────────────── #
        if _is_small_talk(user_message):
            logger.info(f'Small-talk: "{user_message}"')
            return _ai_or_fallback(user_message, emotion, [], conversation_history,
                                   fallback="Namaste! I'm here to listen. How are you feeling today?")

        # ── 2. Specific problem phrase → DB answer directly ───────────── #
        if _has_specific_phrase(user_message):
            logger.info(f'Specific phrase detected in: "{user_message}"')
            best = search_knowledge_base(user_message, dominant)
            if best and best.get('answer', '').strip():
                logger.info(f'✅ DB direct answer | Q: {best.get("question","")[:60]}')
                return best['answer'].strip()

        # ── 3. General emotional state ("i am sad") → AI with DB context ─ #
        if _is_general_emotional_state(user_message):
            logger.info(f'General emotional state: "{user_message}" ({dominant})')
            refs = search_multiple_references(user_message, dominant, limit=3)
            return _ai_or_fallback(user_message, emotion, refs, conversation_history,
                                   fallback=_emotion_fallback(dominant))

        # ── 4. Longer message – try DB first, then AI ─────────────────── #
        logger.info(f'Longer message – searching DB first')
        best  = search_knowledge_base(user_message, dominant)
        refs  = search_multiple_references(user_message, dominant, limit=5)

        if best and best.get('answer', '').strip():
            logger.info(f'✅ DB answer | Q: {best.get("question","")[:60]}')
            return best['answer'].strip()

        return _ai_or_fallback(user_message, emotion, refs, conversation_history,
                               fallback=_emotion_fallback(dominant))

    except Exception as e:
        logger.error(f'Guidance generation error: {e}')
        return ("I'm here for you. Take a deep breath — challenges are temporary. "
                "How can I support you right now?")


# ── Helpers ──────────────────────────────────────────────────────────────────── #

def _ai_or_fallback(user_message, emotion, refs, conversation_history, fallback):
    if is_ai_enabled():
        resp = generate_ai_response(user_message, emotion, refs, conversation_history)
        if resp:
            logger.info('✅ AI response')
            return resp
    logger.warning('AI unavailable – using fallback')
    return fallback


def _emotion_fallback(dominant: str) -> str:
    fallbacks = {
        'sad':       "I hear you. It's okay to feel sad — your feelings are valid. Would you like to share what's been weighing on you?",
        'happy':     "That's wonderful! Hold onto this feeling. What's bringing you joy right now?",
        'stressed':  "Stress can be really overwhelming. Remember — you can only control your effort, not every outcome. What's weighing on you most?",
        'depressed': "I hear you. Please know you're not alone. The darkness you feel right now is not permanent. I'm here — talk to me.",
        'anxious':   "It's okay to feel anxious. Take one breath at a time. What's on your mind?",
        'angry':     "I understand you're feeling intense emotions right now. Let's talk it through before acting. What happened?",
    }
    return fallbacks.get(dominant,
        "I'm here for you. Take a deep breath — you don't have to face this alone. How can I support you?")
