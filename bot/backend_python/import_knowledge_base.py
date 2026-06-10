"""
Import Knowledge Base from CSV into MongoDB
Run: python3 import_knowledge_base.py
"""
import os
import csv
import sys
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Must be run from bot/backend_python directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config.mongodb import connect_mongodb, get_db

# Emotion keyword mapping to auto-tag entries
EMOTION_KEYWORDS = {
    'depressed': ['suicide', 'sucide', 'end it', 'kill myself', 'broken', 'hopeless', 'stop', 'abandon', 'tired of fighting'],
    'anxious':   ['overthink', 'overthinking', 'mind', 'enemy', 'worry', 'nervous', 'scared'],
    'sad':       ['alone', 'no one understands', 'failure', 'not enough', 'hurt', 'deeply', 'lonely', 'cry'],
    'stressed':  ['tired', 'exhausted', 'fighting', 'weak', 'can\'t', 'too much', 'burden'],
    'angry':     ['murder', 'mudder', 'kill someone', 'anger', 'revenge', 'rage'],
    'spiritual': ['god', 'destiny', 'dharma', 'suffering', 'why', 'suffer', 'bad people'],
    'neutral':   []
}

def detect_emotion_for_entry(question, answer):
    """Detect the best emotion tag for a knowledge base entry"""
    combined = (question + ' ' + answer).lower()
    for emotion, keywords in EMOTION_KEYWORDS.items():
        for kw in keywords:
            if kw in combined:
                return emotion
    return 'neutral'

def extract_keywords(text):
    """Extract meaningful keywords from text"""
    import re
    words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
    stopwords = {'that', 'this', 'with', 'from', 'they', 'have', 'been', 'will',
                 'your', 'their', 'what', 'when', 'where', 'which', 'also', 'just',
                 'more', 'some', 'then', 'than', 'into', 'only', 'very', 'such',
                 'even', 'back', 'does', 'over', 'like', 'same', 'each', 'most'}
    return list(set(w for w in words if w not in stopwords))[:10]

def import_from_csv(csv_path):
    """Import Q&A entries from CSV file into MongoDB"""
    print(f'\nReading CSV: {csv_path}')

    entries = []
    try:
        with open(csv_path, newline='', encoding='utf-8-sig', errors='replace') as f:
            reader = csv.DictReader(f)
            for row in reader:
                question = row.get('question', '').strip()
                answer   = row.get('answer', '').strip()
                # Strip surrounding quotes/special chars
                question = question.strip('\u201c\u201d\u2018\u2019\u00e2\u0080\u009c\u00e2\u0080\u009d\u00ef\u00bf\u00bd\ufffd')
                if not question or not answer:
                    continue
                emotion  = detect_emotion_for_entry(question, answer)
                keywords = extract_keywords(question + ' ' + answer)
                entries.append({
                    'question': question,
                    'answer':   answer,
                    'emotion':  emotion,
                    'keywords': keywords,
                    'tags':     [emotion, 'gita', 'wisdom'],
                    'category': emotion,
                    'priority': 2 if emotion in ('depressed', 'angry') else 1,
                    'source':   'csv_import',
                    'createdAt': datetime.utcnow(),
                    'updatedAt': datetime.utcnow()
                })
    except Exception as e:
        print(f'ERROR reading CSV: {e}')
        sys.exit(1)

    print(f'Found {len(entries)} valid entries in CSV')
    return entries

def run_import():
    print('=' * 50)
    print('  IKORA - Knowledge Base Import')
    print('=' * 50)

    # Connect to MongoDB
    db = connect_mongodb()
    if db is None:
        print('\nERROR: Could not connect to MongoDB.')
        print('Make sure MongoDB is running: sudo systemctl start mongod')
        sys.exit(1)

    # Locate the CSV  (two levels up from this file)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, '..', '..'))
    csv_path = os.path.join(project_root, 'Book1.csv')

    if not os.path.exists(csv_path):
        print(f'\nERROR: CSV not found at {csv_path}')
        print('Please make sure Book1.csv is in the project root.')
        sys.exit(1)

    entries = import_from_csv(csv_path)

    if not entries:
        print('No entries to import.')
        sys.exit(0)

    # Clear existing entries to avoid duplicates
    existing = db.knowledgebases.count_documents({})
    if existing > 0:
        print(f'\nFound {existing} existing entries.')
        ans = input('Clear existing entries before importing? [y/N]: ').strip().lower()
        if ans == 'y':
            db.knowledgebases.delete_many({})
            print('Cleared existing entries.')

    # Insert
    print(f'\nInserting {len(entries)} entries...')
    result = db.knowledgebases.insert_many(entries)
    inserted = len(result.inserted_ids)

    # Recreate text index
    try:
        db.knowledgebases.drop_index('question_text_answer_text_keywords_text_tags_text')
    except Exception:
        pass
    db.knowledgebases.create_index(
        [('question', 'text'), ('answer', 'text'), ('keywords', 'text'), ('tags', 'text')]
    )

    print(f'\n✅ Successfully imported {inserted} entries!')
    print('\nBreakdown by emotion:')
    for doc in db.knowledgebases.aggregate([{'$group': {'_id': '$emotion', 'count': {'$sum': 1}}}]):
        print(f"  {doc['_id']:12s}: {doc['count']} entries")

    print('\nYour chatbot will now use these answers from the database.')
    print('=' * 50)

if __name__ == '__main__':
    run_import()
