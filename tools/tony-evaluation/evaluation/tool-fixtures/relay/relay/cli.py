import argparse
import json
from .queue import Queue
from .delivery import Sink
from .worker import Worker


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--queue", required=True)
    parser.add_argument("--sink", required=True)
    commands = parser.add_subparsers(dest="command", required=True)
    add = commands.add_parser("enqueue")
    add.add_argument("tenant")
    add.add_argument("key")
    add.add_argument("payload")
    work = commands.add_parser("work")
    work.add_argument("--now", type=float, required=True)
    commands.add_parser("show")
    args = parser.parse_args()
    queue, sink = Queue(args.queue), Sink(args.sink)
    if args.command == "enqueue":
        print(json.dumps({"id": queue.enqueue(args.tenant, args.key, args.payload)}))
    elif args.command == "work":
        print(json.dumps({"attempted": Worker(queue, sink).tick(args.now), "jobs": queue.jobs()}))
    else:
        print(json.dumps({"jobs": queue.jobs(), "messages": sink.messages()}))


if __name__ == "__main__":
    main()
