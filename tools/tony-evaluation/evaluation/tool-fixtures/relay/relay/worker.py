class Worker:
    def __init__(self, queue, sink):
        self.queue = queue
        self.sink = sink

    def tick(self, now, ttl=30, after_send=None):
        job = self.queue.claim(now, ttl)
        if job is None:
            return False
        self.queue.ack(job["id"], job["lease_token"], now)
        self.sink.deliver(job["tenant"], job["request_key"], job["payload"])
        if after_send:
            after_send(job)
        return True
