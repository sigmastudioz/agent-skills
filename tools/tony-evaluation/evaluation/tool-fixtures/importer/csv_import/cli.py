import argparse
import json
from pathlib import Path
from .store import Store
from .runner import Runner
from .presenter import render


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", required=True)
    commands = parser.add_subparsers(dest="command", required=True)
    run = commands.add_parser("run")
    run.add_argument("tenant")
    run.add_argument("run_id")
    run.add_argument("source", type=Path)
    run.add_argument("--batch-size", type=int, default=2)
    show = commands.add_parser("show")
    show.add_argument("tenant")
    show.add_argument("run_id")
    args = parser.parse_args()
    store = Store(args.db)
    result = (Runner(store).run(args.tenant, args.run_id, args.source, args.batch_size)
              if args.command == "run" else store.get_run(args.tenant, args.run_id))
    print(json.dumps(render(result)))


if __name__ == "__main__":
    main()
