"""
Import Knowledge Base from CSV files into MongoDB.
Imports both:
  - Book1.csv          (12 handcrafted crisis Q&A entries)
  - data/merged_questions_answers.csv  (693 Bhagavad Gita wellness entries)
Run: python3 import_knowledge_base.py
"""
import os
import csv
import sys
import io
import re
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dotenv import load_dotenv
load_dotenv()

from config.mongodb import connect_mongodb, get_db

# ── Emotion keyword mapping ────────────────────────────────────────────────── #
EMOTION_MAP = {
    'depressed': [
        'suicide', 'suicidal', 'end my life', 'kill myself', 'broken', 'hopeless',
        'meaningless', 'worthless', 'no point', 'want to die', 'tired of living',
        'empty inside', 'numb', 'dark place', 'chronic pain', 'unbearable',
    ],
    'angry': [
        'murder', 'kill someone', 'hurt someone', 'revenge', 'rage', 'furious',
        'betrayed', 'betrayal', 'anger', 'violent',
    ],
    'anxious': [
        'overthink', 'overthinking', 'worry', 'worried', 'anxiety', 'anxious',
        'nervous', 'fear', 'scared', 'panic', 'racing mind', 'mental noise',
        'public speaking', 'crippling fear', 'replaying',
    ],
    'sad': [
        'alone', 'lonely', 'no one understands', 'failure', 'not enough',
        'grief', 'loss', 'heartbroken', 'passed away', 'died', 'miss',
        'abandoned', 'rejected', 'disappointment', 'crying', 'tears',
        'broken trust', 'betrayed by',
    ],
    'stressed': [
        'stressed', 'overwhelmed', 'pressure', 'deadline', 'exhausted',
        'burnout', 'overworked', 'too much', 'tired of fighting', 'lost identity',
        'retired', 'life transition', 'starting over', 'disoriented',
    ],
    'spiritual': [
        'god', 'destiny', 'dharma', 'why suffer', 'bad people', 'purpose',
        'meaning of life', 'soul', 'karma', 'true self', 'inner peace',
        'universe', 'divine', 'enlightenment', 'detachment',
    ],
    'happy': [
        'happy', 'joy', 'grateful', 'thankful', 'blessed', 'content',
        'peaceful', 'hopeful', 'excited', 'wonderful',
    ],
}


def detect_emotion(question, answer):
    combined = (question + ' ' + answer).lower()
    scores = {e: 0 for e in EMOTION_MAP}
    for emotion, keywords in EMOTION_MAP.items():
        for kw in keywords:
            if kw in combined:
                scores[emotion] += 1
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else 'neutral'


def extract_keywords(text):
    words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
    stop = {
        'that', 'this', 'with', 'from', 'they', 'have', 'been', 'will',
        'your', 'their', 'what', 'when', 'where', 'which', 'also', 'just',
        'more', 'some', 'then', 'than', 'into', 'only', 'very', 'such',
        'even', 'back', 'does', 'over', 'like', 'same', 'each', 'most',
        'feel', 'know', 'think', 'want', 'need', 'make', 'take', 'come',
        'true', 'self', 'inside', 'inner', 'body', 'mind', 'life', 'real',
    }
    return list(set(w for w in words if w not in stop))[:12]


def clean_text(text):
    """Fix encoding artifacts from Windows CSV exports."""
    if not text:
        return ''
    # Fix common Windows-1252 → UTF-8 garbling
    fixes = {
        'â€™': "'", 'â€œ': '"', 'â€': '"', 'â€"': '—', 'â€"': '-',
        'Ã©': 'é', 'Ã ': 'à', 'Ã¨': 'è',
        '\u2018': "'", '\u2019': "'", '\u201c': '"', '\u201d': '"',
        '\u2013': '-', '\u2014': '—',
    }
    for bad, good in fixes.items():
        text = text.replace(bad, good)
    return text.strip().strip('"').strip("'")


def read_csv(path):
    """Read a CSV file trying multiple encodings."""
    for enc in ('utf-8-sig', 'cp1252', 'latin-1', 'utf-8'):
        try:
            with open(path, encoding=enc) as f:
                raw = f.read()
            entries = []
            reader = csv.DictReader(io.StringIO(raw))
            for row in reader:
                q = clean_text(row.get('question', ''))
                a = clean_text(row.get('answer', ''))
                if q and a and len(q) > 5 and len(a) > 5:
                    entries.append((q, a))
            print(f'  Read {len(entries)} entries (encoding: {enc})')
            return entries
        except (UnicodeDecodeError, LookupError):
            continue
    print(f'  ERROR: Could not read {path}')
    return []


def build_document(question, answer, source, priority=1):
    emotion = detect_emotion(question, answer)
    # Crisis entries get higher priority
    crisis_keywords = ['suicide', 'suicidal', 'kill', 'murder', 'hopeless', 'worthless']
    if any(kw in (question + answer).lower() for kw in crisis_keywords):
        priority = 3
    elif emotion in ('depressed', 'angry', 'anxious'):
        priority = 2

    return {
        'question': question,
        'answer': answer,
        'emotion': emotion,
        'keywords': extract_keywords(question + ' ' + answer),
        'tags': [emotion, 'wisdom', 'gita'],
        'category': emotion,
        'priority': priority,
        'source': source,
        'createdAt': datetime.now(timezone.utc),
        'updatedAt': datetime.now(timezone.utc),
    }


def run_import():
    print('=' * 55)
    print('  IKORA - Full Knowledge Base Import')
    print('=' * 55)

    # Connect
    db_conn = connect_mongodb()
    db = get_db()
    if db is None:
        print('\nERROR: Could not connect to MongoDB.')
        print('Make sure MONGODB_URI is set in .env and MongoDB is running.')
        sys.exit(1)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, '..', '..'))

    # ── Locate CSV files ──────────────────────────────────────────────── #
    csv_files = [
        (os.path.join(project_root, 'Book1.csv'), 'book1_crisis', 2),
        (os.path.join(project_root, 'data', 'merged_questions_answers.csv'), 'merged_gita', 1),
    ]

    all_entries = []
    for path, source, base_priority in csv_files:
        if not os.path.exists(path):
            print(f'\n⚠️  Not found: {path} — skipping')
            continue
        print(f'\nReading: {os.path.basename(path)}')
        rows = read_csv(path)
        for q, a in rows:
            all_entries.append(build_document(q, a, source, base_priority))

    if not all_entries:
        print('\nNo entries to import.')
        sys.exit(0)

    print(f'\nTotal entries to import: {len(all_entries)}')

    # ── Clear existing ────────────────────────────────────────────────── #
    existing = db.knowledgebases.count_documents({})
    if existing > 0:
        print(f'Found {existing} existing entries — clearing...')
        db.knowledgebases.delete_many({})

    # ── Insert in batches ─────────────────────────────────────────────── #
    BATCH = 100
    inserted = 0
    for i in range(0, len(all_entries), BATCH):
        batch = all_entries[i:i + BATCH]
        try:
            result = db.knowledgebases.insert_many(batch, ordered=False)
            inserted += len(result.inserted_ids)
        except Exception as e:
            print(f'  Batch {i//BATCH + 1} partial error: {e}')
        print(f'  Inserted {min(i + BATCH, len(all_entries))}/{len(all_entries)}...', end='\r')

    print(f'\n\n✅ Successfully imported {inserted} entries!')

    # ── Recreate text index ───────────────────────────────────────────── #
    print('\nCreating text search index...')
    try:
        # Drop old index if exists
        db.knowledgebases.drop_index('question_text_answer_text_keywords_text_tags_text')
    except Exception:
        pass
    db.knowledgebases.create_index(
        [('question', 'text'), ('answer', 'text'), ('keywords', 'text'), ('tags', 'text')],
        weights={'question': 10, 'keywords': 5, 'answer': 3, 'tags': 1},
        name='kb_text_search'
    )
    print('✅ Text index created')

    # ── Summary ───────────────────────────────────────────────────────── #
    print('\nBreakdown by emotion:')
    for doc in db.knowledgebases.aggregate([
        {'$group': {'_id': '$emotion', 'count': {'$sum': 1}}},
        {'$sort': {'count': -1}}
    ]):
        bar = '█' * (doc['count'] // 10)
        print(f"  {doc['_id']:12s}: {doc['count']:3d}  {bar}")

    print('\nBreakdown by source:')
    for doc in db.knowledgebases.aggregate([
        {'$group': {'_id': '$source', 'count': {'$sum': 1}}}
    ]):
        print(f"  {doc['_id']:20s}: {doc['count']}")

    print('\n' + '=' * 55)
    print('  Import Complete! Bot is now fully loaded.')
    print('=' * 55)


if __name__ == '__main__':
    run_import()
