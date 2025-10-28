#!/usr/bin/env python3
"""
Network Explorer Dashboard
- Shows hostname, local IP, public IP
- Checks a few URLs (status + latency)
Usage:
  python3 net_explorer.py
  python3 net_explorer.py https://weber.edu https://www.python.org
"""

import argparse
import socket
import time
from typing import List, Tuple
from urllib.parse import urlparse

import requests


def get_hostname_local_ip() -> Tuple[str, str]:
    hostname = socket.gethostname()
    # Robust local IP: open a dummy UDP socket (no packets actually sent)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
    except Exception:
        # Fallback if socket trick fails
        try:
            local_ip = socket.gethostbyname(hostname)
        except Exception:
            local_ip = "unknown"
    finally:
        try:
            s.close()
        except Exception:
            pass
    return hostname, local_ip


def get_public_ip(timeout: int = 5) -> str:
    try:
        r = requests.get("https://api.ipify.org?format=json", timeout=timeout)
        return r.json().get("ip", "unknown")
    except Exception:
        return "unknown"


def normalize_urls(urls: List[str]) -> List[str]:
    normed = []
    for u in urls:
        if u.startswith("http://") or u.startswith("https://"):
            normed.append(u)
        else:
            normed.append("https://" + u)
    return normed


def quick_check(url: str, timeout: int = 5) -> Tuple[str, float, bool]:
    start = time.time()
    try:
        resp = requests.head(url, timeout=timeout, allow_redirects=True)
        elapsed = time.time() - start
        return f"{resp.status_code}", elapsed, (200 <= resp.status_code < 400)
    except requests.exceptions.Timeout:
        return "Timeout", 0.0, False
    except requests.exceptions.ConnectionError:
        return "ConnError", 0.0, False
    except Exception:
        return "Error", 0.0, False


def domain_of(url: str) -> str:
    try:
        return urlparse(url).hostname or url
    except Exception:
        return url


def main():
    parser = argparse.ArgumentParser(
        description="Network Explorer Dashboard: host/IP info + quick URL checks"
    )
    parser.add_argument(
        "urls",
        nargs="*",
        help="Optional URLs to check; if omitted, defaults are used",
    )
    parser.add_argument(
        "-t", "--timeout", type=int, default=5, help="HTTP timeout per URL (sec)"
    )
    args = parser.parse_args()

    defaults = ["https://weber.edu", "https://github.com", "https://www.python.org"]
    urls = normalize_urls(args.urls if args.urls else defaults)

    hostname, local_ip = get_hostname_local_ip()
    public_ip = get_public_ip(timeout=args.timeout)

    print("\n=== Network Explorer Dashboard ===")
    print(f"Hostname : {hostname}")
    print(f"Local IP : {local_ip}")
    print(f"Public IP: {public_ip}")
    print("\nURL Checks (HEAD requests):")
    print(f"{'Domain':35} {'Status':>10} {'Elapsed(s)':>12} {'OK':>5}")
    print("-" * 66)

    for u in urls:
        status, elapsed, ok = quick_check(u, timeout=args.timeout)
        print(f"{domain_of(u):35} {status:>10} {elapsed:12.2f} {str(ok):>5}")

    print("\nTip: pass your own URLs, e.g.:")
    print("  python3 net_explorer.py https://weber.edu https://www.python.org\n")


if __name__ == "__main__":
    main()

