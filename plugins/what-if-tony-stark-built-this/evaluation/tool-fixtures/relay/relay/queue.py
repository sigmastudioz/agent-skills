import uuid
from .db import connect


class Queue:
    def __init__(self, path):
        self.db = connect(path)
        self.db.execute("""CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY, tenant TEXT NOT NULL, request_key TEXT NOT NULL,
            payload TEXT NOT NULL, state TEXT NOT NULL DEFAULT 'pending',
            lease_token TEXT, lease_until REAL, attempts INTEGER NOT NULL DEFAULT 0,
            UNIQUE(tenant, request_key))""")

    def enqueue(self, tenant, request_key, payload):
        row = self.db.execute("SELECT * FROM jobs WHERE tenant=? AND request_key=?",
                              (tenant, request_key)).fetchone()
        if row:
            if row["payload"] != payload:
                raise ValueError("conflicting request payload")
            return row["id"]
        return self.db.execute("INSERT INTO jobs(tenant,request_key,payload) VALUES(?,?,?)",
                               (tenant, request_key, payload)).lastrowid

    def claim(self, now, ttl):
        row = self.db.execute("SELECT * FROM jobs WHERE state='pending' OR "
                              "(state='leased' AND lease_until<=?) ORDER BY id LIMIT 1", (now,)).fetchone()
        if row is None:
            return None
        token = uuid.uuid4().hex
        self.db.execute("UPDATE jobs SET state='leased',lease_token=?,lease_until=?,"
                        "attempts=attempts+1 WHERE id=?", (token, now + ttl, row["id"]))
        return dict(self.db.execute("SELECT * FROM jobs WHERE id=?", (row["id"],)).fetchone())

    def ack(self, job_id, token, now):
        result = self.db.execute("UPDATE jobs SET state='done' WHERE id=?", (job_id,))
        return bool(result.rowcount)

    def release(self, job_id, token):
        result = self.db.execute("UPDATE jobs SET state='pending',lease_token=NULL,lease_until=NULL WHERE id=?", (job_id,))
        return bool(result.rowcount)

    def jobs(self):
        return [dict(row) for row in self.db.execute("SELECT * FROM jobs ORDER BY id")]
