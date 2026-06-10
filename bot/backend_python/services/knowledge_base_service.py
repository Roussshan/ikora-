"""
Knowledge Base Service
"""
import re
import random
from models.knowledge_base import KnowledgeBase
from utils.logger import logger

def search_knowledge_base(user_message, emotion, limit=5):
    """Search knowledge base using multiple strategies"""
    try:
        message_lower = user_message.lower()
        # Extract keywords (words longer than 3 characters)
        keywords = [word for word in re.findall(r'\w+', message_lower) if len(word) > 3]
        
        logger.info(f'Searching knowledge base for: "{user_message}" with emotion: {emotion}')
        logger.info(f'Extracted keywords: {", ".join(keywords)}')
        
        # Strategy 1: Full-text search
        text_results = KnowledgeBase.text_search(user_message, emotion, limit)
        if text_results:
            logger.info(f'Found {len(text_results)} results via text search')
            return text_results[0]
        
        # Strategy 2: Keyword matching
        if keywords:
            keyword_results = KnowledgeBase.keyword_search(keywords, emotion, limit)
            if keyword_results:
                logger.info(f'Found {len(keyword_results)} results via keyword matching')
                return keyword_results[0]
        
        # Strategy 3: Emotion-based fallback
        emotion_results = KnowledgeBase.find_by_emotion(emotion, limit)
        if emotion_results:
            random_index = random.randint(0, min(2, len(emotion_results) - 1))
            logger.info(f'Using emotion-based fallback ({emotion})')
            return emotion_results[random_index]
        
        # Strategy 4: Retry text search WITHOUT emotion filter
        text_results_any = KnowledgeBase.text_search(user_message, None, limit)
        if text_results_any:
            logger.info('Found result via text search (no emotion filter)')
            return text_results_any[0]

        # Strategy 5: Neutral fallback
        neutral_results = KnowledgeBase.find_by_emotion('neutral', limit)
        if neutral_results:
            random_index = random.randint(0, min(2, len(neutral_results) - 1))
            logger.info('Using neutral fallback response')
            return neutral_results[random_index]
        
        logger.warning('No matching entries found in knowledge base')
        return None
        
    except Exception as e:
        logger.error('Error searching knowledge base', e)
        return None

def search_multiple_references(user_message, emotion, limit=5):
    """Search knowledge base and return multiple relevant references for AI context"""
    try:
        message_lower = user_message.lower()
        keywords = [word for word in re.findall(r'\w+', message_lower) if len(word) > 3]
        
        results = []
        
        # Try text search first
        text_results = KnowledgeBase.text_search(user_message, emotion, limit)
        if text_results:
            results.extend(text_results)
        
        # Add keyword results if we need more
        if len(results) < limit and keywords:
            keyword_results = KnowledgeBase.keyword_search(keywords, emotion, limit)
            if keyword_results:
                # Avoid duplicates
                existing_ids = {str(r.get('_id')) for r in results}
                for kr in keyword_results:
                    if str(kr.get('_id')) not in existing_ids:
                        results.append(kr)
                        if len(results) >= limit:
                            break
        
        # Add emotion-based if still need more
        if len(results) < limit:
            emotion_results = KnowledgeBase.find_by_emotion(emotion, limit)
            if emotion_results:
                existing_ids = {str(r.get('_id')) for r in results}
                for er in emotion_results:
                    if str(er.get('_id')) not in existing_ids:
                        results.append(er)
                        if len(results) >= limit:
                            break
        
        logger.info(f'Found {len(results)} total references for AI context')
        return results[:limit]
        
    except Exception as e:
        logger.error('Error searching multiple references', e)
        return []

def get_random_wisdom(emotion=None):
    """Get random wisdom from knowledge base"""
    try:
        if emotion:
            results = KnowledgeBase.find_by_emotion(emotion, 10)
        else:
            # This would need a different implementation for truly random
            results = KnowledgeBase.find_by_emotion('neutral', 10)
        
        if results:
            return random.choice(results)
        return None
    except Exception as e:
        logger.error('Error getting random wisdom', e)
        return None

def get_knowledge_base_stats():
    """Get knowledge base statistics"""
    try:
        from config.mongodb import get_db
        db = get_db()
        
        if db is None:
            return {'connected': False}
        
        total = KnowledgeBase.count()
        
        # Get counts by emotion
        by_emotion = list(db.knowledgebases.aggregate([
            {'$group': {'_id': '$emotion', 'count': {'$sum': 1}}}
        ]))
        
        # Get counts by category
        by_category = list(db.knowledgebases.aggregate([
            {'$group': {'_id': '$category', 'count': {'$sum': 1}}}
        ]))
        
        return {
            'connected': True,
            'total': total,
            'byEmotion': by_emotion,
            'byCategory': by_category
        }
    except Exception as e:
        logger.error('Error getting knowledge base stats', e)
        return {'connected': False, 'error': str(e)}
