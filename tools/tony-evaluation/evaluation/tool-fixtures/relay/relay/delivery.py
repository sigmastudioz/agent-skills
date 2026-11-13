from .db import connect


class Sink:
    def __init__(self, path):
        self.db = connect(path)
        self.db.execute("""CREATE TABLE IF NOT EXISTS messages (
            delivery_key TEXT PRIMARY KEY, tenant TEXT NOT NULL,
            request_key TEXT NOT NULL, payload TEXT NOT NULL)""")

    def deliver(self, tenant, request_key, payload):
        key = tenant + ":" + request_key
        self.db.execute("INSERT OR IGNORE INTO messages VALUES(?,?,?,?)",
                        (key, tenant, request_key, payload))

    def messages(self):
        return [dict(row) for row in self.db.execute("SELECT * FROM messages ORDER BY rowid")]
