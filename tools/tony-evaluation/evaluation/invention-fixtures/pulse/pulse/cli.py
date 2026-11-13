import json
import sys
from .report import build


def main():
    with open(sys.argv[1], encoding="utf-8") as handle:
        program = json.load(handle)
    print(json.dumps(build(program), sort_keys=True))


if __name__ == "__main__":
    main()
