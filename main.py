"""vacuum excuse, r19: closure-style one-shot publisher."""
import json
import os

ROOM_LIMIT = 140
RUN_ID = "vacuum-1125"
SIGNAL = "r19 sweep done"


def make_publisher(cap):
    def read_entry():
        spot = os.path.dirname(os.path.abspath(__file__))
        handle = open(os.path.join(spot, "entry.txt"), encoding="utf-8")
        try:
            return handle.read().replace("\r", "").strip()
        finally:
            handle.close()

    def acceptable(text):
        return 1 <= len(text) <= cap and len(text.split()) > 0

    def flush(text):
        zone = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
        os.makedirs(zone, exist_ok=True)
        where = os.path.join(zone, "entry.txt")
        handle = open(where, "w", encoding="utf-8", newline="\n")
        try:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        finally:
            handle.close()
        again = open(where, encoding="utf-8").read()
        if again != text:
            raise AssertionError("flush mismatch")
        return where

    return read_entry, acceptable, flush


def main():
    read_entry, acceptable, flush = make_publisher(ROOM_LIMIT)
    text = read_entry()
    if not acceptable(text):
        print(json.dumps({"run": RUN_ID, "ok": False,
                          "n": len(text), "cap": ROOM_LIMIT}))
        return 4
    where = flush(text)
    print(json.dumps({"run": RUN_ID, "ok": True, "signal": SIGNAL,
                      "where": where, "n": len(text)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
