import sqlite3


class Store:
    def __init__(self, path):
        self.db = sqlite3.connect(path, isolation_level=None)
        self.db.row_factory = sqlite3.Row
        self.db.executescript("""
            CREATE TABLE IF NOT EXISTS runs (
                tenant TEXT, run_id TEXT, source_key TEXT, next_row INTEGER DEFAULT 0,
                state TEXT DEFAULT 'running', PRIMARY KEY(tenant,run_id));
            CREATE TABLE IF NOT EXISTS records (
                tenant TEXT, record_id TEXT, value TEXT, PRIMARY KEY(tenant,record_id));
        """)

    def start(self, tenant, run_id, source_key):
        self.db.execute("INSERT OR IGNORE INTO runs(tenant,run_id,source_key) VALUES(?,?,?)",
                        (tenant, run_id, source_key))
        return self.get_run(tenant, run_id)

    def get_run(self, tenant, run_id):
        row = self.db.execute("SELECT * FROM runs WHERE run_id=?", (run_id,)).fetchone()
        return dict(row) if row else None

    def write_record(self, tenant, record_id, value):
        self.db.execute("INSERT OR REPLACE INTO records VALUES(?,?,?)", (tenant, record_id, value))

    def checkpoint(self, tenant, run_id, next_row):
        self.db.execute("UPDATE runs SET next_row=? WHERE tenant=? AND run_id=?", (next_row, tenant, run_id))

    def finish(self, tenant, run_id):
        self.db.execute("UPDATE runs SET state='complete' WHERE tenant=? AND run_id=?", (tenant, run_id))

    def records(self, tenant):
        return [dict(row) for row in self.db.execute("SELECT * FROM records WHERE tenant=? ORDER BY record_id", (tenant,))]
