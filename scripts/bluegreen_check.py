#!/usr/bin/env python3
"""Poll a URL for a fixed time and fail if the error rate is too high."""
import argparse
import sys
import time
import urllib.request


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--url", required=True)
    p.add_argument("--duration", type=int, default=30, help="seconds to keep polling")
    p.add_argument("--interval", type=float, default=1.0, help="seconds between requests")
    p.add_argument("--max-error-rate", type=float, default=0.0, help="0.05 = 5 percent")
    p.add_argument("--timeout", type=float, default=3.0)
    a = p.parse_args()

    total = 0
    failed = 0
    end = time.time() + a.duration
    while time.time() < end:
        total += 1
        try:
            with urllib.request.urlopen(a.url, timeout=a.timeout) as r:
                if r.status >= 400:
                    failed += 1
        except Exception:
            failed += 1
        print(f"requests={total} failed={failed} error_rate={failed / total:.1%}", flush=True)
        time.sleep(a.interval)

    rate = failed / total if total else 1.0
    if rate > a.max_error_rate:
        print(f"FAIL: error rate {rate:.1%} is above the limit of {a.max_error_rate:.1%}")
        sys.exit(1)
    print(f"PASS: error rate {rate:.1%} is within the limit of {a.max_error_rate:.1%}")


if __name__ == "__main__":
    main()