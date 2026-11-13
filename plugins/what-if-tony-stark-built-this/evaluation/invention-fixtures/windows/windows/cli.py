import json
import sys
from .planner import plan


def main():
    with open(sys.argv[1], encoding="utf-8") as handle:
        request = json.load(handle)
    print(json.dumps(plan(request), sort_keys=True))


if __name__ == "__main__":
    main()
