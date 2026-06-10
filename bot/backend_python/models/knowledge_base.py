"""
Knowledge Base Model
"""
from datetime import datetime
from bson import ObjectId
from config.mongodb import get_db

class KnowledgeBase:
    collection_name = 'knowledgebases'
    
    @staticmethod
    def create(question, answer, category=None, tags=None, emotion=None, keywords=None, priority=1):
        """Create a new knowledge base entry"""
        db = get_db()
        if db is None:
            raise Exception('Database not connected')
        
        entry_data = {
            'question': question,
            'answer': answer,
            'priority': priority,
            'createdAt': datetime.utcnow(),
            'updatedAt': datetime.utcnow()
        }
        
        if category:
            entry_data['category'] = category
        if tags:
            entry_data['tags'] = tags
        if emotion:
            entry_data['emotion'] = emotion
        if keywords:
            entry_data['keywords'] = keywords
        
        result = db[KnowledgeBase.collection_name].insert_one(entry_data)
        entry_data['_id'] = result.inserted_id
        return entry_data
    
    @staticmethod
    def text_search(query, emotion=None, limit=5):
        """Search knowledge base using text search"""
        db = get_db()
        if db is None:
            return []
        
        try:
            search_filter = {'$text': {'$search': query}}
            
            if emotion:
                search_filter['$or'] = [
                    {'emotion': emotion},
                    {'emotion': 'neutral'},
                    {'emotion': {'$exists': False}}
                ]
            
            results = list(db[KnowledgeBase.collection_name].find(
                search_filter,
                {'score': {'$meta': 'textScore'}}
            ).sort([('priority', -1), ('score', {'$meta': 'textScore'})]).limit(limit))
            
            return results
        except Exception as e:
            # If text index doesn't exist, fall back to regex search
            try:
                query_words = query.lower().split()
                regex_patterns = [{'question': {'$regex': word, '$options': 'i'}} for word in query_words if len(word) > 3]
                
                if not regex_patterns:
                    return []
                
                search_filter = {'$or': regex_patterns}
                
                if emotion:
                    search_filter = {
                        '$and': [
                            {'$or': regex_patterns},
                            {
                                '$or': [
                                    {'emotion': emotion},
                                    {'emotion': 'neutral'},
                                    {'emotion': {'$exists': False}}
                                ]
                            }
                        ]
                    }
                
                results = list(db[KnowledgeBase.collection_name].find(
                    search_filter
                ).sort('priority', -1).limit(limit))
                
                return results
            except:
                return []
    
    @staticmethod
    def keyword_search(keywords, emotion=None, limit=5):
        """Search knowledge base using keywords"""
        db = get_db()
        if db is None:
            return []
        
        try:
            search_filter = {
                '$and': [
                    {
                        '$or': [
                            {'keywords': {'$in': keywords}},
                            {'tags': {'$in': keywords}}
                        ]
                    }
                ]
            }
            
            if emotion:
                search_filter['$and'].append({
                    '$or': [
                        {'emotion': emotion},
                        {'emotion': 'neutral'},
                        {'emotion': {'$exists': False}}
                    ]
                })
            
            results = list(db[KnowledgeBase.collection_name].find(
                search_filter
            ).sort('priority', -1).limit(limit))
            
            return results
        except:
            return []
    
    @staticmethod
    def find_by_emotion(emotion, limit=5):
        """Find entries by emotion"""
        db = get_db()
        if db is None:
            return []
        
        try:
            results = list(db[KnowledgeBase.collection_name].find(
                {'emotion': emotion}
            ).sort('priority', -1).limit(limit))
            return results
        except:
            return []
    
    @staticmethod
    def count():
        """Count total entries"""
        db = get_db()
        if db is None:
            return 0
        
        try:
            return db[KnowledgeBase.collection_name].count_documents({})
        except:
            return 0
    
    @staticmethod
    def bulk_insert(entries):
        """Bulk insert entries"""
        db = get_db()
        if db is None:
            raise Exception('Database not connected')
        
        try:
            result = db[KnowledgeBase.collection_name].insert_many(entries, ordered=False)
            return len(result.inserted_ids)
        except Exception as e:
            # Handle partial success
            return 0
