import csv


class Runner:
    def __init__(self, store):
        self.store = store

    def run(self, tenant, run_id, source, batch_size=2, after_row=None):
        run = self.store.start(tenant, run_id, str(source.resolve()))
        rows = list(csv.DictReader(source.read_text(encoding="utf-8").splitlines()))
        position = run["next_row"]
        while position < len(rows):
            batch = rows[position:position + batch_size]
            self.store.checkpoint(tenant, run_id, position + len(batch))
            for row in batch:
                self.store.write_record(tenant, row["record_id"], row["value"])
                if after_row:
                    after_row(row)
            position += len(batch)
        self.store.finish(tenant, run_id)
        return self.store.get_run(tenant, run_id)
