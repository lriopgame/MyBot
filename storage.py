import sqlite3, os, json, time
DB = 'data/app.db'; os.makedirs('data', exist_ok=True)

def init_db():
    with sqlite3.connect(DB) as c:
        c.execute('''CREATE TABLE IF NOT EXISTS users(
            user_id INTEGER PRIMARY KEY,
            username TEXT, first_name TEXT, lang TEXT DEFAULT 'ru',
            consent INTEGER DEFAULT 0, created_at INTEGER)''')
        c.execute('''CREATE TABLE IF NOT EXISTS queries(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER, text TEXT, source TEXT, params TEXT, ts INTEGER)''')
        c.execute('''CREATE TABLE IF NOT EXISTS reports(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER, query_id INTEGER, title TEXT, body TEXT, fmt TEXT, ts INTEGER)''')
def upsert_user(u):
    import time, sqlite3
    with sqlite3.connect(DB) as c:
        c.execute("""INSERT INTO users(user_id, username, first_name, created_at)
                 VALUES(?,?,?,?) ON CONFLICT(user_id) DO UPDATE SET
                 username=excluded.username, first_name=excluded.first_name""",
                 "(u.id, u.username, u.first_name, int(time.time()))")
def log_query(user_id, text, source, params):
    with sqlite3.connect(DB) as c:
        c.execute('INSERT INTO queries(user_id,text,source,params,ts) VALUES(?,?,?,?,?)',
                  (user_id, text, source, json.dumps(params, ensure_ascii=False), int(time.time())))
        return c.execute('SELECT last_insert_rowid()').fetchone()[0]
def save_report(user_id, query_id, title, body, fmt='md'):
    with sqlite3.connect(DB) as c:
        c.execute('INSERT INTO reports(user_id,query_id,title,body,fmt,ts) VALUES(?,?,?,?,?,?)',
                  (user_id, query_id, title, body, fmt, int(time.time())))
