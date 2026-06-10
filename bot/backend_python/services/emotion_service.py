"""
Emotion Detection Service
"""
from utils.logger import logger

EMOTION_TYPES = ['happy', 'sad', 'stressed', 'depressed', 'anxious', 'angry', 'neutral']

def detect_emotion(text):
    """Detect emotion from text using keyword-based analysis"""
    lower_text = text.lower()
    
    keywords = {
        'happy': {
            'words': ['happy', 'joy', 'joyful', 'excited', 'great', 'wonderful', 'amazing', 'blessed', 'grateful', 'thankful', 'fantastic', 'excellent', 'delighted', 'cheerful', 'pleased'],
            'weight': 1
        },
        'sad': {
            'words': ['sad', 'unhappy', 'down', 'depressing', 'crying', 'tears', 'heartbroken', 'hurt', 'pain', 'sorrow', 'grief', 'loss', 'lonely', 'alone', 'miss', 'disappointed'],
            'weight': 1
        },
        'stressed': {
            'words': ['stressed', 'stress', 'overwhelmed', 'pressure', 'busy', 'too much', 'deadline', 'exhausted', 'tired', 'overworked', 'burden', 'struggling', 'difficult', 'hard', 'challenging'],
            'weight': 1
        },
        'depressed': {
            'words': ['depressed', 'depression', 'hopeless', 'worthless', 'empty', 'numb', 'dark', 'meaningless', 'pointless', 'give up', 'no point', 'cant go on', 'end it', 'suicide', 'suicidal'],
            'weight': 1.5
        },
        'anxious': {
            'words': ['anxious', 'anxiety', 'worried', 'worry', 'nervous', 'scared', 'afraid', 'fear', 'panic', 'terrified', 'frightened', 'uneasy', 'tense', 'restless', 'concerned'],
            'weight': 1
        },
        'angry': {
            'words': ['kill', 'murder', 'hate', 'angry', 'anger', 'rage', 'furious', 'revenge', 'hurt someone', 'harm', 'attack', 'destroy', 'fight', 'violent', 'violence', 'scream'],
            'weight': 1.5
        },
        'neutral': {
            'words': ['okay', 'fine', 'alright', 'normal', 'usual', 'regular', 'average', 'so-so'],
            'weight': 0.5
        }
    }
    
    scores = {
        'happy': 0,
        'sad': 0,
        'stressed': 0,
        'depressed': 0,
        'anxious': 0,
        'angry': 0,
        'neutral': 0.2
    }
    
    # Count keyword matches with weights
    for emotion, data in keywords.items():
        count = 0
        for word in data['words']:
            if word in lower_text:
                count += 1
        scores[emotion] = min(1.0, count * 0.25 * data['weight'])
    
    # Analyze sentence structure
    question_count = text.count('?')
    if question_count > 0:
        scores['anxious'] += question_count * 0.1
        scores['neutral'] -= 0.1
    
    exclamation_count = text.count('!')
    if exclamation_count > 0:
        if scores['happy'] > scores['sad']:
            scores['happy'] += exclamation_count * 0.1
        else:
            scores['stressed'] += exclamation_count * 0.1
    
    # Normalize scores
    total = sum(scores.values())
    if total > 0:
        for key in scores:
            scores[key] = min(1.0, scores[key] / total * 2)
    
    # Phrase-level patterns for cases keyword scan misses
    phrase_patterns = {
        'depressed': ['feel like a failure', 'no reason to live',
                      'life is meaningless', 'what is the point', 'want to disappear',
                      'tired of everything', 'nothing matters', 'feel empty', 'feel numb'],
        'anxious':   ['overthink', 'overthinking', 'mind is my enemy', 'can\'t stop thinking', 'mind racing',
                      'keep worrying', 'so nervous', 'freaking out'],
        'stressed':  ['too much pressure', 'can\'t handle', 'breaking down', 'falling apart',
                      'tired of fighting', 'tired of trying', 'worn out'],
        'sad':       ['miss them', 'miss him', 'miss her', 'feel lost', 'feel broken',
                      'broken inside', 'so alone', 'no one cares',
                      'feel like a failure', 'am a failure', 'never enough', 'not enough'],
        'angry':     ['want to hurt', 'want to scream', 'so furious', 'boiling inside'],
    }
    for emotion_name, phrases in phrase_patterns.items():
        for phrase in phrases:
            if phrase in lower_text:
                scores[emotion_name] = max(scores[emotion_name], 0.5)

    # If all scores are still 0, default to neutral instead of happy
    if max(scores.values()) == 0:
        scores['neutral'] = 0.5

    # Find dominant emotion
    dominant = max(scores, key=scores.get)

    # Calculate confidence
    sorted_scores = sorted(scores.values(), reverse=True)
    confidence = min(0.95, (sorted_scores[0] - sorted_scores[1]) + 0.5) if sorted_scores[0] > 0 else 0.5

    emotion_data = {
        'dominant': dominant,
        'scores': scores,
        'confidence': confidence
    }

    logger.info(f'Detected emotion: {dominant} (confidence: {confidence:.2f})')
    return emotion_data
