"""
Chat Service
"""
from datetime import datetime
from models.conversation import Conversation
from services.emotion_service import detect_emotion
from services.guidance_service import generate_guidance
from utils.logger import logger

def save_message(user_id, content, sender, emotion=None):
    """Save a message to conversation history"""
    try:
        conversation = Conversation.create(user_id, content, sender, emotion)
        logger.info(f'Message saved to MongoDB: {sender} - {user_id}')
        return str(conversation['_id'])
    except Exception as e:
        logger.error('Error saving message', e)
        raise e

def get_conversation_history(user_id, limit=50):
    """Get conversation history for a user"""
    try:
        conversations = Conversation.find_by_user(user_id, limit)
        
        messages = []
        for conv in conversations:
            message = {
                'id': str(conv['_id']),
                'userId': str(conv['userId']),
                'content': conv['message'],
                'sender': conv['sender'],
                'timestamp': conv['createdAt'].isoformat() + 'Z'
            }
            
            if conv.get('emotion'):
                message['emotion'] = {
                    'dominant': conv['emotion']['dominant'],
                    'scores': conv['emotion']['scores'],
                    'confidence': conv['emotion']['confidence']
                }
            
            messages.append(message)
        
        return messages
    except Exception as e:
        logger.error('Error fetching conversation history', e)
        return []

def send_message(user_id, message):
    """Process user message and generate response"""
    try:
        # Detect emotion
        emotion = detect_emotion(message)
        
        # Save user message
        user_message_id = save_message(user_id, message, 'user', emotion)
        
        # Get recent conversation history for context
        history = get_conversation_history(user_id, 10)
        conversation_context = []
        for msg in history[-6:]:
            conversation_context.append({
                'role': 'user' if msg['sender'] == 'user' else 'assistant',
                'content': msg['content']
            })
        
        # Generate guidance
        response = generate_guidance(message, emotion, conversation_context)
        
        # Save Ikora's response
        ikora_message_id = save_message(user_id, response, 'ikora')
        
        logger.info(f'Chat exchange completed for user {user_id} (MongoDB)')
        
        return {
            'messageId': ikora_message_id,
            'response': response,
            'emotion': emotion,
            'timestamp': datetime.utcnow().isoformat() + 'Z'
        }
    except Exception as e:
        logger.error('Error in send_message', e)
        raise e

def clear_conversation(user_id):
    """Clear conversation history for a user"""
    try:
        count = Conversation.delete_by_user(user_id)
        logger.info(f'Cleared conversation history for user {user_id} (MongoDB)')
        return count
    except Exception as e:
        logger.error('Error clearing conversation', e)
        raise e
