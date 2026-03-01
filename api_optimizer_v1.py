import sqlite3
import hashlib
import json
import time

class APICache:
    def __init__(self, db_path="memory/api_cache.sqlite"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS cache 
                            (query_hash TEXT PRIMARY KEY, response TEXT, timestamp REAL)''')
        self.conn.commit()

    def get_hash(self, text):
        return hashlib.sha256(text.encode()).hexdigest()

    def check(self, query):
        q_hash = self.get_hash(query)
        self.cursor.execute("SELECT response, timestamp FROM cache WHERE query_hash=?", (q_hash,))
        result = self.cursor.fetchone()
        if result and (time.time() - result[1] < 3600): # 1 hour cache
            return json.loads(result[0])
        return None

    def store(self, query, response):
        q_hash = self.get_hash(query)
        self.cursor.execute("REPLACE INTO cache VALUES (?, ?, ?)", 
                         (q_hash, json.dumps(response), time.time()))
        self.conn.commit()

# Example usage for JARVIS system optimization
# if __name__ == "__main__":
#     cache = APICache()
#     # logic for skipping redundant API calls...
